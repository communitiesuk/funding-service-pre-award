#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone

import boto3
import click
from sqlalchemy.orm.attributes import flag_modified

from app import create_app
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
def delete_pii(fund_short_name: str, round_short_name: str, dry_run: bool, env: str) -> None:  # noqa: C901
    # get identity from aws for audit trail
    run_by = get_run_by()
    if not run_by:
        run_by = click.prompt("No AWS identity found. Enter your email to continue")
    print(f"\nRunning as: {run_by}")
    print(f"Environment: {env}")

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
    if datetime.now(timezone.utc) > round_obj.deadline:
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

    now = datetime.now(timezone.utc)
    submitted_cutoff = round_obj.deadline.replace(tzinfo=timezone.utc) + timedelta(days=submitted_days)
    unsubmitted_cutoff = round_obj.deadline.replace(tzinfo=timezone.utc) + timedelta(days=unsubmitted_days)

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

    # step 7 — confirmation
    if not dry_run:
        print(f"You are about to delete PII for {fund_short_name}-{round_short_name}.")
        confirmation = input(f"Type '{fund_short_name}-{round_short_name}' to confirm: ")
        if confirmation != f"{fund_short_name}-{round_short_name}":
            print("\nERROR: Confirmation did not match. Aborting.")
            return
        print("\nConfirmed. Proceeding with deletion...")
    else:
        print("\nDRY RUN — no data will be deleted")
        print("Run with --no-dry-run to execute")

    print(f"\n\nFinal decision — delete unsubmitted: {delete_unsubmitted}")
    print(f"Final decision — delete submitted:   {delete_submitted}")

    # step 8 — deleting data
    if dry_run:
        print("\nDRY RUN — no data will be deleted. Skipping deletion step.")
    else:
        deletion_successful = True
        for application in applications_to_delete:
            try:
                for form in application.forms:
                    db.session.delete(form)
                application.is_deleted = True
                application.project_name = ""
                db.session.add(application)

                db.session.commit()
                print("\n")
                print(f"Application marked as deleted and application ID is:   {application.id}")
                assessment_record: AssessmentRecord = get_assessment_record(application.id)
                if assessment_record:
                    assessment_record.is_deleted = True
                    assessment_record.project_name = "deleted"
                    assessment_record.jsonb_blob["forms"] = []
                    assessment_record.jsonb_blob["is_deleted"] = True
                    assessment_record.jsonb_blob["project_name"] = "deleted"
                    flag_modified(assessment_record, "jsonb_blob")
                    db.session.add(assessment_record)
                    db.session.commit()
                    print(f"Assessment Record marked as deleted and application ID is:   {application.id}")

            except Exception as e:
                db.session.rollback()
                deletion_successful = False
                print(f"An error occurred: {e}")

    # step 9 — delete s3 files
    if dry_run:
        print("\nDRY RUN — would delete S3 files associated with applications; skipping actual deletion.")
    else:
        if deletion_successful:
            print("\nData deletion successful for applications. Proceeding to delete S3 files...")
            for application in applications_to_delete:
                try:
                    s3_files_list = list_files_in_folder(f"{application.id}/")
                    print(f"Found {len(s3_files_list)} files in {application.id}")
                    for file_key in s3_files_list:
                        full_key = f"{application.id}/{file_key}"
                        delete_file_from_aws(full_key)
                except Exception as e:
                    print(f"An error occurred while deleting S3 files for application id {application.id}: {e}")

    # step 10 — create PiiDeletionLog instance for audit and set pii_deleted_for_applications on Round
    # to prevent double deletion attempts in the future
    if dry_run:
        print("\nDRY RUN — would create PiiDeletionLog entry; skipping actual log creation.")
    else:
        print("\nCreating PiiDeletionLog entry for audit trail...")
        if delete_unsubmitted and delete_submitted:
            applications_scope = ApplicationsWithPiiDeleted.ALL
            total_deleted = submitted_count + unsubmitted_count
        elif delete_unsubmitted and not delete_submitted:
            applications_scope = ApplicationsWithPiiDeleted.UN_SUBMITTED
            total_deleted = unsubmitted_count
        elif delete_submitted and not delete_unsubmitted:
            applications_scope = ApplicationsWithPiiDeleted.SUBMITTED
            total_deleted = submitted_count
        else:
            # Nothing was selected for deletion; do not log
            print("\nNo applications selected for deletion; skipping PiiDeletionLog entry")
            return

        log_entry = PiiDeletionLog(
            round_id=round_obj.id,
            deleted_by=run_by,
            applications_with_pii_deleted=applications_scope,
            applications_with_pii_deleted_count=total_deleted,
        )

        # save what has been deleted on the Round object to prevent double deletion attempts in the future
        # combine the scope from this run with any existing scope on the round
        existing_scope = round_obj.pii_deleted_for_applications
        if delete_unsubmitted and delete_submitted:
            new_scope = PiiDeletionScope.ALL
        elif delete_unsubmitted and not delete_submitted:
            if existing_scope == PiiDeletionScope.SUBMITTED:
                new_scope = PiiDeletionScope.ALL
            else:
                new_scope = PiiDeletionScope.UN_SUBMITTED
        elif delete_submitted and not delete_unsubmitted:
            if existing_scope == PiiDeletionScope.UN_SUBMITTED:
                new_scope = PiiDeletionScope.ALL
            else:
                new_scope = PiiDeletionScope.SUBMITTED

        round_obj.pii_deleted_for_applications = new_scope
        status = new_scope.name
        db.session.add(log_entry)
        db.session.add(round_obj)
        db.session.commit()

        print(f"\nPiiDeletionLog entry created and round pii_deleted_for_applications field marked as: {status}")


if __name__ == "__main__":
    with app.app_context():
        delete_pii()
