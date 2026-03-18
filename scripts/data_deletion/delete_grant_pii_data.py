#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone

import boto3
import click

from app import create_app
from data.crud.fund_round_queries import get_round
from pre_award.application_store.db.models import Applications
from pre_award.application_store.db.models.application.enums import Status
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
@click.option("--fund", required=True, help="Fund short name e.g. COF")
@click.option("--round", "round_short_name", required=True, help="Round short name e.g. R2W2")
@click.option("--dry-run", is_flag=True, default=True, help="Print what would be deleted without executing")
@click.option(
    "--env",
    required=True,
    type=click.Choice(ENVIRONMENTS, case_sensitive=False),
    help="Environment to run against e.g. local, dev, test, uat, production",
)
def delete_pii(fund: str, round_short_name: str, dry_run: bool, env: str) -> None:
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
    round_obj = get_round(fund, round_short_name)
    if not round_obj:
        print(f"\nERROR: No round found for {fund}-{round_short_name}. Check the short names and try again.")
        return
    print(f"\nRound found: {round_obj.title_json.get('en')} | deadline: {round_obj.deadline}")

    # step 2 — check round is closed
    if datetime.utcnow() > round_obj.deadline:
        print(f" Round is closed. Deadline was {round_obj.deadline}")
    else:
        print(f"ERROR: Round {fund}-{round_short_name} is still open. Deadline is {round_obj.deadline}")
        return

    # step 3 — check not already deleted
    if round_obj.pii_deletion_completed:
        print(f"ERROR: PII deletion already completed for {fund}-{round_short_name}. Cannot run twice.")
        return
    print(" PII deletion not yet completed for this round")

    # step 4 — check retention period
    submitted_days, unsubmitted_days, source = get_retention_config(fund, round_short_name)

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

    if not unsubmitted_eligible and not submitted_eligible:
        print("\nERROR: Retention period has not passed. Nothing to delete.")
        print(f"Come back after {unsubmitted_cutoff.date()}")
        return

    if not submitted_eligible:
        print(f"\n Submitted applications not yet eligible until {submitted_cutoff.date()}")
        print("Will only delete unsubmitted applications")

    # step 5 — inventory
    print(f"\n{'─' * 50}")
    print(f"INVENTORY — {fund}-{round_short_name}")
    print(f"{'─' * 50}")

    submitted_count = (
        db.session.query(Applications)
        .filter(
            Applications.fund_id == str(round_obj.fund_id),
            Applications.round_id == str(round_obj.id),
            Applications.status.in_(SUBMITTED_STATUSES),
            Applications.is_deleted.is_(False),
        )
        .count()
    )

    unsubmitted_count = (
        db.session.query(Applications)
        .filter(
            Applications.fund_id == str(round_obj.fund_id),
            Applications.round_id == str(round_obj.id),
            Applications.status.in_(UNSUBMITTED_STATUSES),
            Applications.is_deleted.is_(False),
        )
        .count()
    )

    print(f"  Submitted applications:    {submitted_count}")
    print(f"  Unsubmitted applications:  {unsubmitted_count}")
    print(f"  Total:                     {submitted_count + unsubmitted_count}")
    print(f"\n  Will delete unsubmitted:   {unsubmitted_eligible}")
    print(f"  Will delete submitted:     {submitted_eligible}")
    print(f"{'─' * 50}\n")

    # step 6 — confirmation
    if not dry_run:
        print(f"You are about to delete PII for {fund}-{round_short_name}.")
        confirmation = input(f"Type '{fund}-{round_short_name}' to confirm: ")
        if confirmation != f"{fund}-{round_short_name}":
            print("ERROR: Confirmation did not match. Aborting.")
            return
        print(" Confirmed. Proceeding with deletion...")
    else:
        print("DRY RUN — no data will be deleted")
        print("Run with --no-dry-run to execute")

    # step 7 — deleting data
    # step 8 — delete s3 files
    # step 9 — write into PiiDeletionLog for audit


if __name__ == "__main__":
    with app.app_context():
        delete_pii()
