#!/usr/bin/env python3
"""
Script: update_scoring_system_for_round.py

This script associates an existing scoring system with a round.
It supports:
  1. Non-interactive (command-line) mode: Required arguments are supplied via flags.
  2. Interactive mode: The user is prompted for input if arguments are missing.

Usage example (non-interactive):
  python -m pre_award.assessment_store.scripts.update_scoring_system_for_round \
    --round_id "99308c73-f721-44d0-9df5-c87b15efcab3" \
    --system_name "ExistingSystemName"
"""

import argparse
import sys
from typing import Optional, Tuple

from app import create_app
from pre_award.assessment_store.db.models.score import ScoringSystem
from pre_award.assessment_store.db.queries.scores.queries import (
    get_scoring_info_by_round,
    list_existing_scoring_systems,
    lookup_scoring_system_id,
    update_scoring_system_for_round_id,
)
from pre_award.db import db
from pre_award.fund_store.db.queries import get_fund_short_name

try:
    from data.models import Fund, Round
except ImportError:
    print("Error: Unable to import Round and Fund from data.models.")
    sys.exit(1)


def print_fund_round_scoringsystem() -> None:
    """Print a list of available rounds along with fund and scoring system info."""
    rounds = db.session.query(Round).all()
    if not rounds:
        print("No rounds found in the database.")
    else:
        print("\nAvailable Rounds:")
        for idx, rnd in enumerate(rounds, start=1):
            fund_name = get_fund_short_name(rnd.fund_id)
            short_name = getattr(rnd, "short_name", "N/A")
            scoring_system = get_scoring_info_by_round(rnd.id)
            if scoring_system:
                scoring_system_info = f"{scoring_system.scoring_system_name.name}, "
            else:
                scoring_system_info = "N/A"
            print(
                f"  [{idx}] | Fund: {fund_name} | Round: {short_name} | "
                f"Scoring System: {scoring_system_info} | Round ID: {rnd.id}"
            )


def print_scoring_systems():
    systems = list_existing_scoring_systems()
    if not systems:
        print("No existing scoring systems found in the database.")
    else:
        print("\nExisting Scoring Systems:")
        for system in systems:
            system_name = system.scoring_system_name.name
            print(
                f" Name: {system_name} | Range: {system.minimum_score}-{system.maximum_score} | "
                f"Scoring System ID: {system.id}"
            )


def get_round_id(interactive: bool = True, provided_round_id: Optional[str] = None) -> Optional[str]:
    if not interactive:
        return provided_round_id
    print_fund_round_scoringsystem()
    selection = input(
        "\nEnter the number corresponding to the round you want to associate, or type the round ID directly: "
    ).strip()
    try:
        idx = int(selection)
        rounds = db.session.query(Round).all()
        if 1 <= idx <= len(rounds):
            return rounds[idx - 1].id
        print("Invalid selection number.")
        return None
    except ValueError:
        return selection


def interactive_mode() -> Tuple[str, str]:
    print("\n=== Interactive Mode ===")
    print_scoring_systems()
    system_name = input("\nEnter the name of the scoring system you want to use: ").strip()
    scoring_system_id = lookup_scoring_system_id(system_name)
    if not scoring_system_id:
        print(f"Scoring system '{system_name}' not found. Exiting.")
        sys.exit(1)
    print(f"\nUsing scoring system '{system_name}' with ID: {scoring_system_id}")
    round_id = None
    while not round_id:
        round_id = get_round_id(interactive=True)
        if not round_id:
            print("Please try again to select a valid round.")
    return scoring_system_id, round_id


def final_display(scoring_system_id: str, round_id: str) -> None:
    """Perform a final lookup and display scoring system, round, and fund details."""
    scoring_system = db.session.query(ScoringSystem).filter(ScoringSystem.id == scoring_system_id).one_or_none()
    round_obj = db.session.query(Round).filter(Round.id == round_id).one_or_none()
    fund_obj = None
    if round_obj and getattr(round_obj, "fund_id", None):
        fund_obj = db.session.query(Fund).filter(Fund.id == round_obj.fund_id).first()

    if scoring_system:
        system_name = scoring_system.scoring_system_name.name
    else:
        system_name = "N/A"
    round_short = getattr(round_obj, "short_name", "N/A") if round_obj else "N/A"
    fund_short = fund_obj.short_name if fund_obj else "N/A"

    print(
        (
            f"\nSuccessfully associated scoring system [{system_name}, {scoring_system_id}] "
            f"with Round [{round_short}, id: {round_id}] from Fund {fund_short}."
        )
    )


def main():
    app = create_app()
    with app.app_context():
        parser = argparse.ArgumentParser(
            description="Associate an existing scoring system with a round. "
            "Provide parameters for non-interactive mode, or run interactively."
        )
        parser.add_argument("--round_id", help="Round ID to associate with the scoring system.")
        parser.add_argument("--system_name", help="Existing scoring system name to use.")
        args = parser.parse_args()

        if args.round_id and args.system_name:
            scoring_system_id = lookup_scoring_system_id(args.system_name)
            if not scoring_system_id:
                print(f"Scoring system '{args.system_name}' not found in the database.")
                sys.exit(1)
            round_id = args.round_id
        else:
            scoring_system_id, round_id = interactive_mode()

        update_scoring_system_for_round_id(round_id, scoring_system_id)
        final_display(scoring_system_id, round_id)


if __name__ == "__main__":
    main()
