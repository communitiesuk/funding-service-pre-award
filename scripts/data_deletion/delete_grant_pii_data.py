#!/usr/bin/env python3
from datetime import timedelta
from typing import NamedTuple

import boto3
import click
from sqlalchemy.orm.attributes import flag_modified

from app import create_app
from common.utils.date_time_utils import get_now_UK_time_without_tzinfo
from data.crud.fund_round_queries import get_round
from data.models import PiiDeletionLog
from pre_award.application_store.db.models import Applications
from pre_award.application_store.db.models.application.enums import ApplicationsWithPiiDeleted, PiiDeletionScope, Status
from pre_award.assess.services.aws import delete_file_from_aws, list_files_in_folder
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.queries.assessment_records._helpers import NO_LOCATION_DATA
from pre_award.assessment_store.db.queries.assessment_records.queries import get_assessment_record
from pre_award.db import db
from scripts.data_deletion.data_retention_config import get_retention_config

app = create_app()

ENVIRONMENTS = ["local", "dev", "test", "uat", "production"]

SUBMITTED_STATUSES = [
    Status.SUBMITTED,
    Status.CHANGE_REQUESTED,
    Status.CHANGE_RECEIVED,
]

UNSUBMITTED_STATUSES = [
    Status.NOT_STARTED,
    Status.IN_PROGRESS,
    Status.COMPLETED,
]


class ApplicationToDelete(NamedTuple):
    """
    One application queued for deletion, plus metadata captured once up front - see the comment where
    this is built, in delete_pii. `application_id`/`status_name`/`is_unsubmitted` mean the loop's
    print statements and bookkeeping never need to re-read those attributes off the ORM object (which
    risks a DB round-trip on an object expired by an earlier commit/rollback). `application` itself is
    still the live ORM object, and delete_application_pii(application) does read/mutate its attributes
    on every iteration - that's fine because it happens inside the loop's try/except, so an expiry
    refresh failing there is caught and recorded as that one application's failure, not a crash.
    """

    application: Applications
    application_id: str
    status_name: str
    is_unsubmitted: bool


def get_run_by() -> str | None:
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        return identity.get("Arn")
    except Exception:
        return None


def _org_name(application: Applications) -> str:
    return application.project_name or "(no organisation name recorded)"


def print_deletion_plan(to_delete: list[Applications], retained: list[Applications]) -> None:
    """Print the explicit set of applications that would be deleted and those being retained, so an
    operator can eyeball "deleting these N, keeping these M" before anything irreversible happens."""
    print(f"\n{'=' * 60}")
    print(f"APPLICATIONS THAT WOULD BE DELETED ({len(to_delete)}):")
    print(f"{'=' * 60}")
    if to_delete:
        for application in to_delete:
            print(f"  DELETE  {application.id}  [{application.status.name}]  {_org_name(application)}")
    else:
        print("  (none)")

    print(f"\n{'=' * 60}")
    print(f"APPLICATIONS BEING RETAINED / EXCLUDED ({len(retained)}):")
    print(f"{'=' * 60}")
    if retained:
        for application in retained:
            print(f"  RETAIN  {application.id}  [{application.status.name}]  {_org_name(application)}")
    else:
        print("  (none)")

    print(f"\nSUMMARY: deleting {len(to_delete)} application(s), retaining {len(retained)}.")
    print(f"{'=' * 60}")


def delete_application_pii(application: Applications) -> str:
    """
    Delete every row of PII linked to this application (forms, feedback, eligibility answers,
    research/end-of-application survey responses), then mark the application record itself as
    deleted. Returns a one-line summary of what was removed, for the operator's log.

    None of these child collections cascade automatically: the FKs are configured with
    ondelete="CASCADE" at the DB level, but the relationships use passive_deletes=True, so the
    cascade only fires on a real row delete of the parent - which we deliberately never do (the
    Applications row itself is kept, scrubbed, and marked is_deleted). Each collection must
    therefore be deleted explicitly here.
    """
    counts = {"forms": 0, "feedback": 0, "eligibility": 0, "research_surveys": 0, "end_of_application_survey": 0}

    for form in application.forms:
        db.session.delete(form)
        counts["forms"] += 1
    for feedback in application.feedbacks:
        db.session.delete(feedback)
        counts["feedback"] += 1
    for eligibility in application.eligibility:
        db.session.delete(eligibility)
        counts["eligibility"] += 1
    for survey in application.research_surveys:
        db.session.delete(survey)
        counts["research_surveys"] += 1
    for eoas in application.end_of_application_survey:
        db.session.delete(eoas)
        counts["end_of_application_survey"] += 1

    application.is_deleted = True
    application.project_name = ""
    # application is already persistent (loaded via a query), so no need to re-add it - and doing so
    # would be actively harmful here: the default relationship cascade includes "save-update", so
    # db.session.add(application) would cascade through the (still Python-side-populated) child
    # collections above and try to re-attach the rows just marked for deletion, raising
    # "Instance has been deleted".

    return ", ".join(f"{count} {label}" for label, count in counts.items() if count)


def scrub_assessment_record(assessment_record: AssessmentRecord) -> None:
    # assessment_record is already persistent (loaded via get_assessment_record), so no need to
    # re-add it to the session - mutating its attributes is enough for the unit of work to pick up.
    assessment_record.is_deleted = True
    assessment_record.project_name = "deleted"
    assessment_record.jsonb_blob["forms"] = []
    assessment_record.jsonb_blob["is_deleted"] = True
    assessment_record.jsonb_blob["project_name"] = "deleted"
    flag_modified(assessment_record, "jsonb_blob")
    # Several assessment templates and sort lambdas read location_json_blob assuming it's always a dict with
    # these exact keys (e.g. `overview.location_json_blob.get('country')`, and a raw
    # `x["location_json_blob"]["country"]` subscript in a table-sort lambda) - setting it to None or
    # {} would 500 those call sites and prevent key assessment templates (eg dashboard) from loading. Reuse the same
    # "no location data available" shape the app already produces when a postcode lookup fails or a fund has no location
    # mapping (NO_LOCATION_DATA - a single shared definition, so this stays in sync with that shape rather than
    # drifting as a second hand-copied literal), so every downstream consumer sees an already-handled state instead
    # of a novel one. It's worth us clearing out this data as for smaller orgs that may have applied for funding this
    # could conceivably contain PII (eg. a home address postcode).
    assessment_record.location_json_blob = NO_LOCATION_DATA.copy()


@click.command()
@click.option("--fund", "fund_short_name", required=True, help="Fund short name e.g. COF")
@click.option("--round", "round_short_name", required=True, help="Round short name e.g. R2W2")
@click.option(
    "--dry-run/--no-dry-run",
    default=True,
    show_default=True,
    help="Print what would be deleted without executing",
)
@click.option(
    "--env",
    required=True,
    type=click.Choice(ENVIRONMENTS, case_sensitive=False),
    help="Environment to run against e.g. local, dev, test, uat, production",
)
@click.option(
    "--exclude-application",
    "exclude_application_ids",
    multiple=True,
    type=click.UUID,
    help=(
        "Application ID to EXCLUDE from deletion. Repeatable. Excluded applications are never "
        "touched: not deleted, their S3 files are kept, and their assessment records are not "
        "scrubbed. Use to retain specific applicants, e.g. a successful applicant. Pass multiple IDs as "
        "repeated --exclude-application flags."
    ),
)
def delete_pii(  # noqa: C901
    fund_short_name: str,
    round_short_name: str,
    dry_run: bool,
    env: str,
    exclude_application_ids: tuple,
) -> None:
    # get identity from aws for audit trail
    run_by = get_run_by()
    if not run_by:
        run_by = click.prompt("No AWS identity found. Enter your email to continue")
    print(f"\nRunning as: {run_by}")
    print(f"Environment: {env}")

    # type=click.UUID on the option above already validated every value at argument-parsing time
    # (before this function ran at all), so we just need the canonical string form here.
    excluded_ids = {str(u) for u in exclude_application_ids}
    if excluded_ids:
        print(f"\nExcluding {len(excluded_ids)} application(s) from deletion: {', '.join(sorted(excluded_ids))}")

    # prod pairing check
    if env == "production":
        print("\n You are running this against PRODUCTION.")
        print("This requires a second developer to be present.")
        pair_confirmation = click.prompt("Enter your colleague's name to confirm they are pairing with you")
        if not pair_confirmation.strip():
            print("ERROR: A pairing developer must be confirmed for production runs.")
            return
        print(f" Pairing confirmed with: {pair_confirmation}")

    # step 1 — look up round
    round_obj = get_round(fund_short_name, round_short_name)
    if not round_obj:
        print(f"\nERROR: No round found for {fund_short_name}-{round_short_name}. Check the short names and try again.")
        return
    # Fund.short_name/Round.short_name are CITEXT but get_retention_config() below does a
    # plain, case-sensitive dict lookup keyed on "{fund}-{round}" - use the DB values from here on out so every
    # subsequent use (retention lookup, prints, confirmation string) is consistent regardless
    fund_short_name = round_obj.fund.short_name
    round_short_name = round_obj.short_name
    print(f"\nRound found: {round_obj.title_json.get('en')} | deadline: {round_obj.deadline}")

    if round_obj.deadline is None:
        print(f"\nERROR: Round {fund_short_name}-{round_short_name} has no deadline set.")
        print("Cannot determine if it is closed.")
        return

    # exit if PII deletion already completed for all applications in this round
    if round_obj.pii_deleted_for_applications == PiiDeletionScope.ALL:
        print(
            f"\nPII deletion already completed for ALL applications in {fund_short_name}-{round_short_name}. "
            "Nothing to do."
        )
        return

    # step 2 — check round is closed
    # round_obj.deadline is a naive timestamp in Europe/London local time, so "now" must be compared
    # in the same naive Europe/London representation.
    now = get_now_UK_time_without_tzinfo()
    if now > round_obj.deadline:
        print(f"Round is closed. Deadline was {round_obj.deadline}")
    else:
        print(f"ERROR: Round {fund_short_name}-{round_short_name} is still open. Deadline is {round_obj.deadline}")
        return

    # step 3 — check retention period
    submitted_days, unsubmitted_days, source = get_retention_config(fund_short_name, round_short_name)

    print("\nRetention config:")
    print(f"  Source:              {source}")
    print(f"  Submitted:           {submitted_days} days ({submitted_days // 365} years)")
    print(f"  Unsubmitted:         {unsubmitted_days} days ({unsubmitted_days // 365} years)")

    # Cutoffs are computed in the same naive Europe/London space as the deadline and `now` above.
    submitted_cutoff = round_obj.deadline + timedelta(days=submitted_days)
    unsubmitted_cutoff = round_obj.deadline + timedelta(days=unsubmitted_days)

    print(f"\n  Submitted eligible after:   {submitted_cutoff.date()}")
    print(f"  Unsubmitted eligible after: {unsubmitted_cutoff.date()}")

    submitted_eligible = now >= submitted_cutoff
    unsubmitted_eligible = now >= unsubmitted_cutoff

    # Adjust eligibility based on what has already been deleted for this round
    if round_obj.pii_deleted_for_applications == PiiDeletionScope.UN_SUBMITTED:
        # Unsubmitted applications were already processed in a previous run
        unsubmitted_eligible = False
    elif round_obj.pii_deleted_for_applications == PiiDeletionScope.SUBMITTED:
        # Submitted applications were already processed in a previous run
        submitted_eligible = False

    # Bail out here, before printing anything about what's "eligible", if nothing actually is - the
    # step 4 messaging below assumes at least one scope is eligible, and printing e.g. "All
    # applications are eligible for deletion" immediately followed by "No applications are currently
    # eligible" is contradictory, confusing output for the operator.
    if not submitted_eligible and not unsubmitted_eligible:
        print(
            "\nNo applications are currently eligible for deletion (retention period has not passed, "
            "or all eligible scopes have already been processed). Nothing to do."
        )
        return

    # If only unsubmitted are eligible, make that clear before inventory
    if not submitted_eligible and unsubmitted_eligible:
        print(f"\nSubmitted applications not yet eligible until {submitted_cutoff.date()}")
        print("Only unsubmitted applications can be deleted at this time.")

    # step 4 — check not already deleted
    if round_obj.pii_deleted_for_applications == PiiDeletionScope.SUBMITTED:
        print(f"\nPII deletion already completed for SUBMITTED applications in {fund_short_name}-{round_short_name}.")
        print("Only unsubmitted applications will be eligible for deletion.")
    elif round_obj.pii_deleted_for_applications == PiiDeletionScope.UN_SUBMITTED:
        print(f"\nPII deletion already completed for UNSUBMITTED applications in {fund_short_name}-{round_short_name}.")
        print("Only submitted applications will be eligible for deletion.")
    else:
        print("\nPII deletion has not been completed for this round. ")
        print("All applications are eligible for deletion based on retention period.")

    # step 5 — inventory
    print(f"\n{'─' * 50}")
    print(f"INVENTORY — {fund_short_name}-{round_short_name}")
    print(f"{'─' * 50}")

    all_applications = db.session.query(Applications).filter(
        Applications.fund_id == str(round_obj.fund_id),
        Applications.round_id == str(round_obj.id),
        Applications.is_deleted.is_(False),
    )
    if all_applications.count() == 0:
        print("No applications found for this round. Nothing to delete.")
        return

    unsubmitted_applications = all_applications.filter(
        Applications.status.in_(UNSUBMITTED_STATUSES),
    )
    unsubmitted_count = unsubmitted_applications.count()
    unsubmitted_excluded_count = (
        unsubmitted_applications.filter(Applications.id.in_(excluded_ids)).count() if excluded_ids else 0
    )

    submitted_count = 0
    submitted_excluded_count = 0
    if submitted_eligible:
        submitted_applications = all_applications.filter(
            Applications.status.in_(SUBMITTED_STATUSES),
        )
        submitted_count = submitted_applications.count()
        submitted_excluded_count = (
            submitted_applications.filter(Applications.id.in_(excluded_ids)).count() if excluded_ids else 0
        )

    def _count_display(count: int, excluded_count: int) -> str:
        return f"{count} ({excluded_count} excluded)" if excluded_count else str(count)

    print(f"  Unsubmitted applications:  {_count_display(unsubmitted_count, unsubmitted_excluded_count)}")
    if submitted_eligible:
        print(f"  Submitted applications:    {_count_display(submitted_count, submitted_excluded_count)}")
        print(f"  Total:                     {submitted_count + unsubmitted_count}")

    print(f"\n  Can delete unsubmitted:   {unsubmitted_eligible}")
    if submitted_eligible:
        print(f"  Can delete submitted:     {submitted_eligible}")
    print(f"{'─' * 50}\n")

    # step 6 — Confirm whether to delete data for SUBMITTED applications or only UNSUBMITTED applications
    delete_unsubmitted = False
    delete_submitted = False
    applications_to_delete: list[Applications] = []

    if submitted_eligible and unsubmitted_eligible:
        # Both categories are eligible; let the user choose the scope
        choice = click.prompt(
            "Delete PII for (S)UBMITTED applications, (U)NSUBMITTED applications, or (B)OTH? [S/U/B]",
            type=click.Choice(["S", "U", "B", "s", "u", "b"], case_sensitive=False),
        )
        if choice.lower() == "b":
            delete_unsubmitted = True
            delete_submitted = True
            applications_to_delete = all_applications.all()
            print("\nChosen scope: ALL applications (submitted and unsubmitted)")
        elif choice.lower() == "s":
            if submitted_count == 0:
                print("No submitted applications found for this round.")
                return
            delete_submitted = True
            applications_to_delete = submitted_applications.all()
            print("\nChosen scope: ONLY SUBMITTED applications")
        elif choice.lower() == "u":
            if unsubmitted_count == 0:
                print("No unsubmitted applications found for this round.")
                return
            delete_unsubmitted = True
            applications_to_delete = unsubmitted_applications.all()
            print("\nChosen scope: ONLY UNSUBMITTED applications")
    elif submitted_eligible and not unsubmitted_eligible:
        delete_submitted = True
        applications_to_delete = submitted_applications.all()
        print("\nChosen scope: ONLY submitted applications")
    elif unsubmitted_eligible and not submitted_eligible:
        delete_unsubmitted = True
        applications_to_delete = unsubmitted_applications.all()
        print("\nChosen scope: ONLY unsubmitted applications")

    # step 6b — apply exclusions (retain specific applications). Filtering here, at the single point
    # where applications_to_delete is finalised, guarantees excluded applications are never deleted,
    # never have their S3 files removed, and never have their assessment records scrubbed.
    retained_applications = [a for a in applications_to_delete if str(a.id) in excluded_ids]
    applications_to_delete = [a for a in applications_to_delete if str(a.id) not in excluded_ids]

    # Captured now, before the deletion loop runs any commit/rollback that would expire these
    # objects' attributes (see the comment on applications_to_delete_with_metadata below for why that
    # matters).
    retained_ids = {str(a.id) for a in retained_applications}
    retained_has_unsubmitted = any(a.status in UNSUBMITTED_STATUSES for a in retained_applications)
    retained_has_submitted = any(a.status in SUBMITTED_STATUSES for a in retained_applications)

    for missing_id in sorted(excluded_ids - retained_ids):
        print(
            f"\nWARNING: excluded application {missing_id} is not in the deletion scope for "
            f"{fund_short_name}-{round_short_name} (wrong round, already deleted, or a status outside "
            "the chosen scope). It has no effect on this run."
        )

    print_deletion_plan(applications_to_delete, retained_applications)

    if not applications_to_delete:
        print("\nAfter exclusions there are no applications left to delete. Nothing to do.")
        return

    # step 7 — confirmation
    if not dry_run:
        print(f"\nYou are about to delete PII for {fund_short_name}-{round_short_name}.")
        confirmation = input(f"Type '{fund_short_name}-{round_short_name}' to confirm: ")
        if confirmation != f"{fund_short_name}-{round_short_name}":
            print("\nERROR: Confirmation did not match. Aborting.")
            return
        print("\nConfirmed. Proceeding with deletion...")
    else:
        print("\nDRY RUN — no data will be deleted")
        print("Run with --no-dry-run to execute")

    print(f"\nFinal decision — delete unsubmitted: {delete_unsubmitted}")
    print(f"Final decision — delete submitted:   {delete_submitted}")

    # step 8 — delete data (DB rows + assessment record + S3 files), one application at a time.
    # Each application only gets ONE commit, issued after every step for it has succeeded — including
    # S3 cleanup. If anything fails before that commit, db.session.rollback() discards all of this
    # application's pending DB changes, leaving it exactly as it was (still is_deleted=False, still
    # picked up by a future run's inventory query). This matters because is_deleted=True is what makes
    # an application invisible to future runs: committing it before S3 cleanup has actually finished
    # would risk permanently orphaning S3 files that no future run would ever revisit. A failure on
    # one application never affects the others — each iteration is fully independent.
    if dry_run:
        print("\nDRY RUN — no data will be deleted. Skipping deletion step.")
        return

    # Capture the id/status we need for logging up front, while every object here is still freshly
    # loaded (nothing in this run has committed or rolled back yet). Flask-SQLAlchemy's session
    # expires ALL tracked objects' attributes after any commit/rollback, not just the one just
    # touched - so reading application.id/application.status again later (e.g. in a print statement
    # after that application's own commit, or for the *next* application at the top of the loop)
    # would trigger a fresh DB query outside of any try/except. During a sustained DB outage that
    # query could itself raise, crashing the whole loop (and skipping step 9's audit log entirely)
    # instead of being caught and recorded as a single application's failure.
    applications_to_delete_with_metadata = [
        ApplicationToDelete(
            application=application,
            application_id=str(application.id),
            status_name=application.status.name,
            is_unsubmitted=application.status in UNSUBMITTED_STATUSES,
        )
        for application in applications_to_delete
    ]

    unsubmitted_deleted_count = 0
    submitted_deleted_count = 0
    unsubmitted_failed_count = 0
    submitted_failed_count = 0
    deleted_ids: list[str] = []
    failed_ids: list[str] = []

    for application, application_id, status_name, is_unsubmitted in applications_to_delete_with_metadata:
        try:
            deleted_summary = delete_application_pii(application)

            # Suppress autoflush for this lookup: AssessmentRecord has no FK/join relationship to
            # Applications (a leftover of the pre-merge separate databases), so it doesn't need the
            # pending Applications/Forms/etc changes above flushed first. Without this, the implicit
            # flush sends those DELETE/UPDATE statements early and holds their row locks open for the
            # rest of this iteration - including the slow, serial S3 network calls below - for no
            # benefit.
            with db.session.no_autoflush:
                assessment_record: AssessmentRecord = get_assessment_record(application_id)
            if assessment_record:
                scrub_assessment_record(assessment_record)

            # S3 deletion happens before the commit below, on purpose: it's the step most likely to
            # fail (network/permissions), and if it does, rolling back the DB session must still be
            # possible - which it wouldn't be if the DB changes above were already committed.
            s3_files_list = list_files_in_folder(f"{application_id}/")
            for file_key in s3_files_list:
                delete_file_from_aws(f"{application_id}/{file_key}")

            db.session.commit()

            print(f"\nApplication fully deleted: {application_id} [{status_name}]")
            if deleted_summary:
                print(f"  Deleted: {deleted_summary}")
            if assessment_record:
                print(f"  Assessment record scrubbed for {application_id}")
            print(f"  Deleted {len(s3_files_list)} S3 file(s) for {application_id}")

            deleted_ids.append(application_id)
            if is_unsubmitted:
                unsubmitted_deleted_count += 1
            else:
                submitted_deleted_count += 1
        except Exception as e:
            db.session.rollback()
            failed_ids.append(application_id)
            if is_unsubmitted:
                unsubmitted_failed_count += 1
            else:
                submitted_failed_count += 1
            print(f"\nERROR: failed to fully delete application {application_id}: {e}")

    total_deleted = unsubmitted_deleted_count + submitted_deleted_count
    total_failed = unsubmitted_failed_count + submitted_failed_count
    print(
        f"\nDeletion complete. Deleted {total_deleted} application(s) "
        f"(unsubmitted: {unsubmitted_deleted_count}, submitted: {submitted_deleted_count}); "
        f"failed: {total_failed}; retained: {len(retained_applications)}."
    )

    # step 9 — create PiiDeletionLog instance for audit and set pii_deleted_for_applications on Round,
    # reflecting what was ACTUALLY deleted, not what was intended. The id lists let anyone reading
    # this row later see exactly what changed/stayed/needs retrying, without needing the console
    # output. Always write this entry when applications were attempted this run - including when
    # every single one failed.
    print("\nCreating PiiDeletionLog entry for audit trail...")
    if unsubmitted_deleted_count and submitted_deleted_count:
        applications_scope = ApplicationsWithPiiDeleted.ALL
    elif unsubmitted_deleted_count:
        applications_scope = ApplicationsWithPiiDeleted.UN_SUBMITTED
    elif submitted_deleted_count:
        applications_scope = ApplicationsWithPiiDeleted.SUBMITTED
    elif delete_unsubmitted and delete_submitted:
        # Nothing succeeded this run - fall back to the scope that was attempted so the (required,
        # non-nullable) enum still reflects something meaningful. applications_with_pii_deleted_count
        # is 0 and failed_application_ids is populated, so the row is still honest about the outcome.
        applications_scope = ApplicationsWithPiiDeleted.ALL
    elif delete_unsubmitted:
        applications_scope = ApplicationsWithPiiDeleted.UN_SUBMITTED
    else:
        applications_scope = ApplicationsWithPiiDeleted.SUBMITTED

    log_entry = PiiDeletionLog(
        round_id=round_obj.id,
        deleted_by=run_by,
        applications_with_pii_deleted=applications_scope,
        applications_with_pii_deleted_count=total_deleted,
        deleted_application_ids=deleted_ids,
        retained_application_ids=sorted(retained_ids),
        failed_application_ids=failed_ids,
    )
    db.session.add(log_entry)

    # Only advance the round completion flag for a scope deleted IN FULL — i.e. it was in scope this
    # run, it actually contained applications, nothing in it was retained, and nothing in it failed.
    # This keeps the flag (and therefore future gating) honest: it never claims a retained/failed
    # application was deleted, and a scope with zero applications is left untouched rather than
    # vacuously marked complete (which would otherwise mask a genuine failure/retention in the other
    # scope when both are selected in the same run).
    unsubmitted_complete = (
        delete_unsubmitted and unsubmitted_count > 0 and unsubmitted_failed_count == 0 and not retained_has_unsubmitted
    )
    submitted_complete = (
        delete_submitted and submitted_count > 0 and submitted_failed_count == 0 and not retained_has_submitted
    )

    existing_scope = round_obj.pii_deleted_for_applications
    completed_scopes: set[str] = set()
    if existing_scope == PiiDeletionScope.UN_SUBMITTED:
        completed_scopes.add("unsubmitted")
    elif existing_scope == PiiDeletionScope.SUBMITTED:
        completed_scopes.add("submitted")
    elif existing_scope == PiiDeletionScope.ALL:
        completed_scopes.update({"unsubmitted", "submitted"})
    if unsubmitted_complete:
        completed_scopes.add("unsubmitted")
    if submitted_complete:
        completed_scopes.add("submitted")

    if completed_scopes == {"unsubmitted", "submitted"}:
        new_scope = PiiDeletionScope.ALL
    elif completed_scopes == {"unsubmitted"}:
        new_scope = PiiDeletionScope.UN_SUBMITTED
    elif completed_scopes == {"submitted"}:
        new_scope = PiiDeletionScope.SUBMITTED
    else:
        new_scope = existing_scope  # unchanged (may be None)

    if new_scope != existing_scope:
        round_obj.pii_deleted_for_applications = new_scope
        db.session.add(round_obj)

    db.session.commit()

    flag_status = new_scope.name if new_scope is not None else "unchanged (scope not fully completed)"
    print(f"\nPiiDeletionLog entry created. Round pii_deleted_for_applications: {flag_status}")
    if retained_applications or total_failed:
        print(
            "Note: the round was NOT marked fully complete for the retained/failed scope(s), so those "
            "applications remain and can be handled in a future run."
        )


if __name__ == "__main__":
    with app.app_context():
        delete_pii()
