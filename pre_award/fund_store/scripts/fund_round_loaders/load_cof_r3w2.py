# flake8: noqa
from fund_store.config.fund_loader_config.cof.cof_r3 import (
    APPLICATION_BASE_PATH_COF_R3_W2,
)
from fund_store.config.fund_loader_config.cof.cof_r3 import (
    ASSESSMENT_BASE_PATH_COF_R3_W2,
)
from fund_store.config.fund_loader_config.cof.cof_r3 import COF_ROUND_3_WINDOW_2_ID
from fund_store.config.fund_loader_config.cof.cof_r3 import cof_r3w2_sections
from fund_store.config.fund_loader_config.cof.cof_r3 import round_config_w2
from fund_store.db.queries import insert_base_sections
from fund_store.db.queries import insert_or_update_application_sections
from fund_store.db.queries import upsert_round_data


def main() -> None:
    print("'insert_fund_config(...)' not required as COFR3W2 shares the same fund config from COFR3W1.")
    print("Inserting round data.")
    upsert_round_data(round_config_w2)

    print("Inserting base sections config.")
    insert_base_sections(
        APPLICATION_BASE_PATH_COF_R3_W2,
        ASSESSMENT_BASE_PATH_COF_R3_W2,
        COF_ROUND_3_WINDOW_2_ID,
    )
    print("Inserting sections.")
    insert_or_update_application_sections(COF_ROUND_3_WINDOW_2_ID, cof_r3w2_sections)


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
