#!/usr/bin/env python3
# flake8: noqa
from pre_award.fund_store.config.fund_loader_config.cof.cof_r2 import APPLICATION_BASE_PATH
from pre_award.fund_store.config.fund_loader_config.cof.cof_r2 import ASSESSMENT_BASE_PATH
from pre_award.fund_store.config.fund_loader_config.cof.cof_r2 import COF_ROUND_2_WINDOW_2_ID
from pre_award.fund_store.config.fund_loader_config.cof.cof_r2 import COF_ROUND_2_WINDOW_3_ID
from pre_award.fund_store.config.fund_loader_config.cof.cof_r2 import cof_r2_sections
from pre_award.fund_store.config.fund_loader_config.cof.cof_r2 import fund_config
from pre_award.fund_store.config.fund_loader_config.cof.cof_r2 import rounds_config
from pre_award.fund_store.db.queries import insert_base_sections
from pre_award.fund_store.db.queries import insert_fund_data
from pre_award.fund_store.db.queries import insert_or_update_application_sections
from pre_award.fund_store.db.queries import upsert_round_data


def main() -> None:
    inserted_fund = insert_fund_data(fund_config)
    print("Fund inserted:")
    print(inserted_fund)
    inserted_rounds = upsert_round_data(rounds_config)
    print("Rounds inserted:")
    print(inserted_rounds)

    print("Inserting base sections config.")
    # Insert base sections
    insert_base_sections(APPLICATION_BASE_PATH, ASSESSMENT_BASE_PATH, COF_ROUND_2_WINDOW_2_ID)
    insert_base_sections(APPLICATION_BASE_PATH, ASSESSMENT_BASE_PATH, COF_ROUND_2_WINDOW_3_ID)
    print("Inserting sections.")
    # only need to do it for one round as they have identical section sorts
    insert_or_update_application_sections(COF_ROUND_2_WINDOW_2_ID, cof_r2_sections)


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
