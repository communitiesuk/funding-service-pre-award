# flake8: noqa
from pre_award.fund_store.config.fund_loader_config.cof.cof_r4 import (
    APPLICATION_BASE_PATH_COF_R4_W1,
)
from pre_award.fund_store.config.fund_loader_config.cof.cof_r4 import (
    ASSESSMENT_BASE_PATH_COF_R4_W1,
)
from pre_award.fund_store.config.fund_loader_config.cof.cof_r4 import COF_ROUND_4_WINDOW_1_ID
from pre_award.fund_store.config.fund_loader_config.cof.cof_r4 import cof_r4w1_sections
from pre_award.fund_store.config.fund_loader_config.cof.cof_r4 import fund_config
from pre_award.fund_store.config.fund_loader_config.cof.cof_r4 import round_config_w1
from pre_award.fund_store.db.queries import insert_base_sections
from pre_award.fund_store.db.queries import insert_fund_data
from pre_award.fund_store.db.queries import insert_or_update_application_sections
from pre_award.fund_store.db.queries import upsert_round_data


def main() -> None:
    print("Inserting fund and round data.")
    insert_fund_data(fund_config)
    upsert_round_data(round_config_w1)

    print("Inserting base sections config.")
    insert_base_sections(
        APPLICATION_BASE_PATH_COF_R4_W1,
        ASSESSMENT_BASE_PATH_COF_R4_W1,
        COF_ROUND_4_WINDOW_1_ID,
    )
    print("Inserting sections.")
    insert_or_update_application_sections(COF_ROUND_4_WINDOW_1_ID, cof_r4w1_sections)


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
