import json

import click

from application_store.db.queries.application.queries import get_application
from assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from assessment_store.db.queries.assessment_records._helpers import derive_application_values


@click.command()
@click.option(
    "-a",
    "--application_id",
    help="Application ID to derive values",
    prompt=True,
)
def derive_assessment_values(application_id):
    from flask import current_app

    from db import db

    current_app.logger.info(
        "Deriving values for %(application_id)s",
        dict(application_id=application_id),
    )

    application_json = get_application(application_id, include_forms=True, as_json=True)
    derived_values = derive_application_values(application_json)

    print(json.dumps(derived_values, sort_keys=True, indent=2))

    if click.confirm("Do you want to commit those values to the database?"):
        assessment_record: AssessmentRecord = db.session.get(AssessmentRecord, application_id)
        assessment_record.location_json_blob = derived_values["location_json_blob"]
        assessment_record.funding_amount_requested = derived_values["funding_amount_requested"]
        assessment_record.asset_type = derived_values["asset_type"]
        db.session.commit()
        current_app.logger.info("Database updated with derived values")
    else:
        current_app.logger.info("Database not updated")


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        derive_assessment_values()
