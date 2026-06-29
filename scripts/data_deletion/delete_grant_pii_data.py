#!/usr/bin/env python3
from datetime import timedelta
from uuid import UUID

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


def get_run_by() -> str | None:
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        return identity.get("Arn")
    except Exception:
        return None


def _org_name(application: Applications) -> str:
    # For these funds the organisation/applicant name is stored on the application's project_name
    # (it is the configured project_name field). Fall back gracefully if it is blank.
    return application.project_name or "(no organisation name recorded)"


def _print_deletion_plan(to_delete: list[Applications], retained: list[Applications]) -> None:
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
    help=(
        "Application ID to EXCLUDE from deletion. Repeatable. Excluded applications are never "
        "touched: not deleted, their S3 files are kept, and their assessment records are not "
        "scrubbed. Use to retain specific applicants, e.g. a successful applicant."
    ),
)
def delete_pii(  # noqa: C901
    fund_short_name: str,
    round_short_name: str,
    dry_run: bool,
    env: str,
    exclude_application_ids: tuple[str, ...],
) -> None:
    # get identity from aws for audit trail
    run_by = get_run_by()
    if not run_by:
        run_by = click.prompt("No AWS identity found. Enter your email to continue")
    print(f"\nRunning as: {run_by}")
    print(f"Environment: {env}")

    # validate any excluded application IDs up front so a typo aborts before anything happens.
    # These applications will be retained (never deleted) — see step 6b.
    excluded_ids: set[str] = set()
    for raw_id in exclude_application_ids:
        try:
            excluded_ids.add(str(UUID(raw_id.strip())))
        except ValueError:
            print(f"\nERROR: --exclude-application value '{raw_id}' is not a valid application UUID. Aborting.")
            return
    if excluded_ids:
        print(f"Excluding {len(excluded_ids)} application(s) from deletion: {', '.join(sorted(excluded_ids))}")

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
    print(f"\nRound found: {round_obj.title_json.get('en')} | deadline: {round_obj.deadline}")

    # exit if PII deletion already completed for all applications in this round
    if round_obj.pii_deleted_for_applications == PiiDeletionScope.ALL:
        print(
            f"\nPII deletion already completed for ALL applications in {fund_short_name}-{round_short_name}. "
            "Nothing to do."
        )
        return

    # step 2 — check round is closed
    # round_obj.deadline is a naive timestamp in Europe/London local time, so we compare against
    # "now" in the same naive Europe/London representation. (Previously this compared a tz-aware UTC
    # now against the naive deadline, which raises TypeError and meant the script never got past here.)
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
    # (Previously the deadline was relabelled as UTC via replace(tzinfo=utc), which is incorrect.)
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
    elif round_obj.pii_deleted_for_applications == PiiDeletionScope.ALL:
        # Both submitted and unsubmitted applications were already processed
        submitted_eligible = False
        unsubmitted_eligible = False

    # If only unsubmitted are eligible, make that clear before inventory
    if not submitted_eligible and unsubmitted_eligible:
        print(f"\nSubmitted applications not yet eligible until {submitted_cutoff.date()}")
        print("Only unsubmitted applications can be deleted at this time.")

    # step 4 — check not already deleted
    if round_obj.pii_deleted_for_applications == PiiDeletionScope.ALL:
        print(
            f"\nERROR: Either retention period has not passed or PII deletion already completed "
            f"for ALL applications in {fund_short_name}-{round_short_name}.\n"
        )
        return
    elif round_obj.pii_deleted_for_applications == PiiDeletionScope.SUBMITTED:
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

    if submitted_eligible:
        submitted_applications = all_applications.filter(
            Applications.status.in_(SUBMITTED_STATUSES),
        )
        submitted_count = submitted_applications.count()

    print(f"  Unsubmitted applications:  {unsubmitted_count}")
    if submitted_eligible:
        print(f"  Submitted applications:    {submitted_count}")
        print(f"  Total:                     {submitted_count + unsubmitted_count}")

    print(f"\n  Can delete unsubmitted:   {unsubmitted_eligible}")
    if submitted_eligible:
        print(f"  Can delete submitted:     {submitted_eligible}")
    print(f"{'─' * 50}\n")

    # Guard: if nothing is eligible (retention not yet passed, or this scope already processed) then
    # there is no scope to delete. Without this, the branches below would leave applications_to_delete
    # undefined and a real run would crash with NameError.
    if not submitted_eligible and not unsubmitted_eligible:
        print(
            "No applications are currently eligible for deletion (retention period has not passed, "
            "or all eligible scopes have already been processed). Nothing to do."
        )
        return

    # step 6 — Confirm whether to delete data for SUBMITTED applications or only UNSUBMITTED applications
    delete_unsubmitted = False
    delete_submitted = False

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

    # step 6b — apply exclusions (retain specific applications), then show the explicit plan.
    # Filtering here, at the single point where applications_to_delete is finalised, guarantees that
    # excluded applications are never deleted, never have their S3 files removed, and never have their
    # assessment records scrubbed — without touching the retention-gating or scope logic above.
    retained_applications = [a for a in applications_to_delete if str(a.id) in excluded_ids]
    applications_to_delete = [a for a in applications_to_delete if str(a.id) not in excluded_ids]

    # Warn about excluded IDs that aren't in the current deletion scope (typo, wrong round, already
    # deleted, or a status outside the chosen scope). They simply have no effect here.
    retained_ids = {str(a.id) for a in retained_applications}
    for missing_id in sorted(excluded_ids - retained_ids):
        print(
            f"\nWARNING: excluded application {missing_id} is not in the deletion scope for "
            f"{fund_short_name}-{round_short_name} (wrong round, already deleted, or a status outside "
            "the chosen scope). It has no effect on this run."
        )

    _print_deletion_plan(applications_to_delete, retained_applications)

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
    # Each application is fully processed and counted only if every step for it succeeds, so a
    # failure on one application never affects the others, and never leaves DB rows deleted while the
    # application's S3 files (PII) remain. Counts below reflect what was ACTUALLY deleted.
    if dry_run:
        print("\nDRY RUN — no data will be deleted. Skipping deletion step.")
        return

    deleted_unsubmitted = 0
    deleted_submitted = 0
    failed_unsubmitted = 0
    failed_submitted = 0

    for application in applications_to_delete:
        is_unsubmitted = application.status in UNSUBMITTED_STATUSES
        try:
            for form in application.forms:
                db.session.delete(form)
            application.is_deleted = True
            application.project_name = ""
            db.session.add(application)
            db.session.commit()
            print(f"\nApplication marked as deleted: {application.id} [{application.status.name}]")

            assessment_record: AssessmentRecord = get_assessment_record(application.id)
            if assessment_record:
                assessment_record.is_deleted = True
                assessment_record.project_name = "deleted"
                assessment_record.jsonb_blob["forms"] = []
                assessment_record.jsonb_blob["is_deleted"] = True
                assessment_record.jsonb_blob["project_name"] = "deleted"
                flag_modified(assessment_record, "jsonb_blob")
                # location_json_blob can also hold applicant-derived location data, so clear it too.
                assessment_record.location_json_blob = None
                db.session.add(assessment_record)
                db.session.commit()
                print(f"Assessment record scrubbed: {application.id}")

            # Delete S3 files for THIS application now its DB rows are committed.
            s3_files_list = list_files_in_folder(f"{application.id}/")
            for file_key in s3_files_list:
                delete_file_from_aws(f"{application.id}/{file_key}")
            print(f"Deleted {len(s3_files_list)} S3 file(s) for {application.id}")

            if is_unsubmitted:
                deleted_unsubmitted += 1
            else:
                deleted_submitted += 1
        except Exception as e:
            db.session.rollback()
            if is_unsubmitted:
                failed_unsubmitted += 1
            else:
                failed_submitted += 1
            print(f"ERROR: failed to fully delete application {application.id}: {e}")

    total_deleted = deleted_unsubmitted + deleted_submitted
    total_failed = failed_unsubmitted + failed_submitted
    print(
        f"\nDeletion complete. Deleted {total_deleted} application(s) "
        f"(unsubmitted: {deleted_unsubmitted}, submitted: {deleted_submitted}); "
        f"failed: {total_failed}; retained: {len(retained_applications)}."
    )

    # step 9 — audit log + round completion flag, reflecting what ACTUALLY happened (not intent).
    if total_deleted == 0:
        print("\nNo applications were successfully deleted; skipping PiiDeletionLog entry and round flag update.")
        return

    print("\nCreating PiiDeletionLog entry for audit trail...")
    if deleted_unsubmitted and deleted_submitted:
        applications_scope = ApplicationsWithPiiDeleted.ALL
    elif deleted_unsubmitted:
        applications_scope = ApplicationsWithPiiDeleted.UN_SUBMITTED
    else:
        applications_scope = ApplicationsWithPiiDeleted.SUBMITTED

    log_entry = PiiDeletionLog(
        round_id=round_obj.id,
        deleted_by=run_by,
        applications_with_pii_deleted=applications_scope,
        applications_with_pii_deleted_count=total_deleted,
        applications_retained_count=len(retained_applications),
    )
    db.session.add(log_entry)

    # Only advance the round completion flag for a scope deleted IN FULL — i.e. it was in scope this
    # run, nothing in it was retained, and nothing in it failed. This keeps the flag (and therefore
    # the audit trail and future gating) honest: it never claims a retained/failed application was
    # deleted, and never blocks a future run from finishing the job.
    unsubmitted_complete = (
        delete_unsubmitted
        and failed_unsubmitted == 0
        and not any(a.status in UNSUBMITTED_STATUSES for a in retained_applications)
    )
    submitted_complete = (
        delete_submitted
        and failed_submitted == 0
        and not any(a.status in SUBMITTED_STATUSES for a in retained_applications)
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
