# flake8: noqa
from pre_award.fund_store.config.fund_loader_config.cof.cof_r3 import COF_ROUND_3_WINDOW_1_ID
from pre_award.fund_store.config.fund_loader_config.cof.cof_r3 import cof_r3_sections
from pre_award.fund_store.db.queries import update_application_section_names


def main() -> None:
    print("Updating section names to sentance case.")
    update_application_section_names(COF_ROUND_3_WINDOW_1_ID, cof_r3_sections)


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
