from pathlib import Path
from pre_award.fund_store.services.fund_configuration_service import load_fund_configurations_from_directory

"""
Goes through all the files in config/fund_loader_config/FAB and adds each round to FAB_FUND_ROUND_CONFIGS

Each file in that directory needs to be python format as per the FAB exports,
containing one property called LOADER_CONFIG
See test_fab_round_config.py for example

FAB_FUND_ROUND_CONFIGS example:
{
    "COF25":{
        "id": "xxx",
        "short_name": "COF25"
        "rounds":{
            "R1": {
                "id": "yyy",
                "fund_id": "xxx",
                "short_name": "R1",
                "sections_config": {}
            }
        }
    }
}
"""

this_dir = Path("pre_award") / "fund_store" / "config" / "fund_loader_config" / "FAB"

# Use the reusable service to process all FAB config files
FAB_FUND_ROUND_CONFIGS = load_fund_configurations_from_directory(this_dir)
