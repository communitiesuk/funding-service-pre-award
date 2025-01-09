# flake8: noqa
from pre_award.fund_store.config.fund_loader_config.cyp.cyp_r1 import APPLICATION_BASE_PATH
from pre_award.fund_store.config.fund_loader_config.cyp.cyp_r1 import ASSESSMENT_BASE_PATH
from pre_award.fund_store.config.fund_loader_config.cyp.cyp_r1 import CYP_ROUND_1_ID
from pre_award.fund_store.config.fund_loader_config.cyp.cyp_r1 import fund_config
from pre_award.fund_store.config.fund_loader_config.cyp.cyp_r1 import r1_application_sections
from pre_award.fund_store.config.fund_loader_config.cyp.cyp_r1 import round_config
from pre_award.fund_store.db.queries import insert_assessment_sections
from pre_award.fund_store.db.queries import insert_base_sections
from pre_award.fund_store.db.queries import insert_fund_data
from pre_award.fund_store.db.queries import insert_or_update_application_sections
from pre_award.fund_store.db.queries import upsert_round_data


def main() -> None:
    print("Inserting fund data for the CYP fund.")
    insert_fund_data(fund_config)
    print("Inserting round data for round 1 of the CYP fund.")
    upsert_round_data(round_config)

    print("Inserting base sections for CYP Round 1.")
    insert_base_sections(APPLICATION_BASE_PATH, ASSESSMENT_BASE_PATH, CYP_ROUND_1_ID)
    print("Inserting application sections for CYP Round 1.")
    insert_or_update_application_sections(CYP_ROUND_1_ID, r1_application_sections)


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
