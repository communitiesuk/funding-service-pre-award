# flake8: noqa
from pre_award.fund_store.config.fund_loader_config.cof.eoi import APPLICATION_BASE_PATH_COF_EOI
from pre_award.fund_store.config.fund_loader_config.cof.eoi import ASSESSMENT_BASE_PATH_COF_EOI
from pre_award.fund_store.config.fund_loader_config.cof.eoi import COF_EOI_ROUND_ID
from pre_award.fund_store.config.fund_loader_config.cof.eoi import cof_eoi_sections
from pre_award.fund_store.config.fund_loader_config.cof.eoi import fund_config
from pre_award.fund_store.config.fund_loader_config.cof.eoi import round_config_eoi
from pre_award.fund_store.db.queries import insert_base_sections
from pre_award.fund_store.db.queries import insert_fund_data
from pre_award.fund_store.db.queries import insert_or_update_application_sections
from pre_award.fund_store.db.queries import upsert_round_data


def main() -> None:
    print("Inserting fund and round data.")
    insert_fund_data(fund_config)
    upsert_round_data(round_config_eoi)

    print("Inserting base sections config.")
    insert_base_sections(
        APPLICATION_BASE_PATH_COF_EOI,
        ASSESSMENT_BASE_PATH_COF_EOI,
        COF_EOI_ROUND_ID,
    )
    print("Inserting sections.")
    insert_or_update_application_sections(COF_EOI_ROUND_ID, cof_eoi_sections)


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
