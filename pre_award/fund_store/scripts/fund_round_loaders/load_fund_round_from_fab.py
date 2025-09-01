# flake8: noqa
import os

import click

from pre_award.db import db
from pre_award.fund_store.config.fund_loader_config.FAB import FAB_FUND_ROUND_CONFIGS
from pre_award.fund_store.services.fab_import_service import process_fund_config


def load_fund_from_fab_impl(fund_short_code="", seed_all_funds=False):
    if fund_short_code == "" and seed_all_funds == False:
        print(f"Nothing to seed.")

        return

    if fund_short_code == "" and seed_all_funds is True:
        print(f"Seeding all funds")
        # Get a list of all Python files in the fund_round_loaders directory
        loader_module_names = [
            fund_config_file
            for fund_config_file in os.listdir("pre_award/fund_store/config/fund_loader_config/FAB")
            if fund_config_file.endswith(".py")
        ]

        for module_name in loader_module_names:
            # Remove the ".py" extension to get the module name
            file_name = module_name[:-3]

            skip_files = ["__init__", "cof_25", "cof_25_eoi"]
            if file_name in skip_files:
                continue

            if fund_short_code != "":
                fund_short_code += ","

            # file names should inlcude the round short name "_" separated
            fund_short_code += module_name[:-3].upper().split("_")[0]

    print(f"Funds to seed: {fund_short_code}")
    for fund_to_seed in fund_short_code.split(","):
        FUND_CONFIG = FAB_FUND_ROUND_CONFIGS.get(fund_to_seed, None)
        if not FUND_CONFIG:
            raise ValueError(f"Config for fund {fund_to_seed} does not exist")

        if FUND_CONFIG:
            # Use the new service function
            result = process_fund_config(FUND_CONFIG)
            if not result["success"]:
                raise Exception(result["message"])


@click.command()
@click.option("--fund_short_code", default="", help="Fund short code")
@click.option("--seed_all_funds", default=False, help="See all funds")
def load_fund_from_fab(fund_short_code, seed_all_funds) -> None:
    """
    Insert the FAB fund and round data into the database.
    See required schema for import here: file_location

    Accept comma separated funds too.
    """
    load_fund_from_fab_impl(fund_short_code, seed_all_funds)


if __name__ == "__main__":
    from app import create_app

    with create_app().app_context():
        load_fund_from_fab()
