import ast
import os
from pathlib import Path
from pre_award.fund_store.services.fab_transform_service import transform_fund_configuration

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

FAB_FUND_ROUND_CONFIGS = {}

for file in os.listdir(this_dir):
    if file.startswith("__") or not file.endswith(".py"):
        continue

    with open(this_dir / file, "r") as json_file:
        content = json_file.read()
        if content.startswith("LOADER_CONFIG = "):
            content = content.split("LOADER_CONFIG = ")[1]
        elif content.startswith("LOADER_CONFIG="):
            content = content.split("LOADER_CONFIG=")[1]
        else:
            raise ValueError(f"fund config file {file.title()} does not start with 'LOADER_CONFIG='")

        loader_config = ast.literal_eval(content)
        fund_data = transform_fund_configuration(loader_config)
        fund_short_name = loader_config["fund_config"]["short_name"]
        if fund_short_name not in FAB_FUND_ROUND_CONFIGS:
            FAB_FUND_ROUND_CONFIGS[fund_short_name] = fund_data
        else:
            FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"].update(fund_data["rounds"])
