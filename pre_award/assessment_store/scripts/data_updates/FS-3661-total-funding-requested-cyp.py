from flask import current_app
from sqlalchemy import select, update

from assessment_store.config.mappings.assessment_mapping_fund_round import (
    fund_round_data_key_mappings,
)
from assessment_store.db.models import AssessmentRecord
from db import db


def update_funding_amount_requested_for_cyp():
    # Update the `funding_amount_requested` calculation for CYP
    # "888aae3d-7e2c-4523-b9c1-95952b3d1644" is the round_id for CYP R1
    import jsonpath_rw_ext

    select_assessment_records_for_round_stmt = select(
        AssessmentRecord.application_id, AssessmentRecord.jsonb_blob
    ).where(AssessmentRecord.round_id == "888aae3d-7e2c-4523-b9c1-95952b3d1644")

    cyp_records = db.session.execute(select_assessment_records_for_round_stmt)

    for application_id, jsonb_blob in cyp_records:
        current_app.logger.info("Processing application id %(application_id)s.", dict(application_id=application_id))
        total_funding = 0
        for key in fund_round_data_key_mappings["CYPR1"]["funding_two"]:
            total_funding = total_funding + int(
                float(
                    (
                        jsonpath_rw_ext.parse(f"$.forms[*].questions[*].fields[?(@.key == '{key}')]")
                        .find(jsonb_blob)[0]
                        .value["answer"]
                    )
                )
            )

        new_funding_amount_requested = total_funding
        current_app.logger.info(
            "New funding amount requested: %(new_funding_amount_requested)s",
            dict(new_funding_amount_requested=new_funding_amount_requested),
        )
        update_statement = (
            update(AssessmentRecord)
            .values(funding_amount_requested=new_funding_amount_requested)
            .where(AssessmentRecord.application_id == application_id)
        )
        db.session.execute(update_statement)
    db.session.commit()


def main() -> None:
    current_app.logger.warning("Updating funding_amount_requested for CYP R1")
    update_funding_amount_requested_for_cyp()
    current_app.logger.warning("Update of funding_amount_requested for CYP R1 COMPLETE")


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
