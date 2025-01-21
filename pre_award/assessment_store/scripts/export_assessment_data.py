#!/usr/bin/env python3
import csv
import sys

sys.path.insert(1, ".")

import argparse  # noqa: E402
from distutils.util import strtobool  # noqa: E402

from pre_award.assessment_store.db.queries.assessment_records.queries import (  # noqa: E402
    get_assessment_records_score_data_by_round_id,
)


def export_assessment_data_to_csv(output, filename):
    """Exports assessment data to a CSV file, splitting the 'Score Date Created'
    column into separate 'Date Created' and 'Time Created' columns for improved
    readability.

    Parameters:
    - output: List of dictionaries representing the assessment data.
    - filename: Name of the output CSV file.

    """
    fieldnames = [
        "Short id",
        "Application ID",
        "Score Subcriteria",
        "Score",
        "Score Justification",
        "Date Created",
        "Time Created",
    ]

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in output:
            score_date_created = row["Score Date Created"]
            row["Date Created"] = score_date_created.strftime("%d/%m/%Y")
            row["Time Created"] = score_date_created.strftime("%H:%M:%S")
            del row["Score Date Created"]

            writer.writerow(row)

    print(f"Successfully exported to {filename}")


def process_assessment_data(round_id, write_csv: bool, csv_location):
    """Processes assessment data for a given fund round.

    Parameters:
    - round_id: UUID round_id for the fund.
    - write_csv: Boolean indicating whether to export the data to a CSV file.
    - csv_location: Location to save the CSV file (optional if write_csv is False).

    Processed Data Fields:
    - Short id: Short identification of the application.
    - Application ID: Identification of the application.
    - Score Subcriteria: Subcriteria for scoring the application.
    - Score: Score assigned to the application.
    - Score Justification: Justification for the assigned score.
    - Date Created: Date when the score was created.
    - Time Created: Time when the score was created.

    """

    assessment_data = get_assessment_records_score_data_by_round_id(round_id)
    print(f"Extracting requested data for {round_id}")

    if write_csv:
        print(f"Writing {round_id} data to csv file")
        export_assessment_data_to_csv(assessment_data, csv_location)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--round_id",
        help="Provide UUID round_id for the fund",
        required=True,
    )
    parser.add_argument(
        "--write_csv",
        help="Whether to write location data to a CSV - " + "if yes, include param --csv_location",
        required=True,
    )
    parser.add_argument(
        "--csv_location",
        help="Absolute path to write CSV file to",
        required=False,
    )
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    process_assessment_data(
        round_id=args.round_id,
        csv_location=args.csv_location,
        write_csv=strtobool(args.write_csv),
    )


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
