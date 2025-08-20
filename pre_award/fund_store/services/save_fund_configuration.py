"""
Service for handling fund configuration data from FAB.
This service contains the core business logic for processing fund store config data.
"""

from flask import current_app

from pre_award.db import db
from pre_award.fund_store.db.queries import (
    insert_base_sections,
    insert_fund_data,
    insert_or_update_application_sections,
    upsert_round_data,
)


def process_fund_config(converted_config):
    """
    Process fund configuration data and save to database.
    Extracted from load_fund_round_from_fab script.
    Args:
        converted_config (dict): Fund configuration dictionary from FAB
    Returns:
        dict: Result of the operation with success status and any error messages
    """
    try:
        print(f"Preparing fund data for the {converted_config['short_name']} fund.")

        # Add required default values if missing or None from FAB
        if not converted_config.get("owner_organisation_name"):
            converted_config["owner_organisation_name"] = ""
        if not converted_config.get("owner_organisation_shortname"):
            converted_config["owner_organisation_shortname"] = ""
        if not converted_config.get("owner_organisation_logo_uri"):
            converted_config["owner_organisation_logo_uri"] = ""

        insert_fund_data(converted_config, commit=False)

        for round_short_name, round in converted_config["rounds"].items():
            round_base_path = round["base_path"]

            APPLICATION_BASE_PATH = ".".join([str(round_base_path), str(1)])
            ASSESSMENT_BASE_PATH = ".".join([str(round_base_path), str(2)])

            print(f"Preparing round data for the '{round_short_name}' round.")
            upsert_round_data([round], commit=False)

            # Section config is per round, not per fund
            print(f"Preparing base sections for {round_short_name}.")
            insert_base_sections(APPLICATION_BASE_PATH, ASSESSMENT_BASE_PATH, round["id"])

            print(f"Preparing application sections for {round_short_name}.")
            insert_or_update_application_sections(round["id"], round["sections_config"])

        print("All config has been successfully prepared, now committing to the database.")
        db.session.commit()
        print("Config has now been committed to the database.")
        return {
            "success": True,
            "message": f"Successfully processed fund configuration for {converted_config['short_name']}",
        }
    except Exception as e:
        current_app.logger.error("Error processing fund config: %s", str(e))
        try:
            db.session.rollback()
        except RuntimeError as rollback_error:
            current_app.logger.error("Error during db rollback: %s", str(rollback_error))
        return {"success": False, "message": f"Error processing fund configuration: {str(e)}"}
