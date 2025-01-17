import ast
import copy
import os
from pathlib import Path

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

FAB_FUND_ROUND_CONFIGS = {}

this_dir = Path("fund_store") / "config" / "fund_loader_config" / "FAB"

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
        if not loader_config.get("fund_config", None):
            print("No fund config found in the loader config.")
            raise ValueError(f"No fund_config found in {file}")
        if not loader_config.get("round_config", None):
            print("No round config found in the loader config.")
            raise ValueError(f"No round_config found in {file}")
        fund_short_name = loader_config["fund_config"]["short_name"]

        # Ensure the fund exists in the main config
        if fund_short_name not in FAB_FUND_ROUND_CONFIGS:
            FAB_FUND_ROUND_CONFIGS[fund_short_name] = loader_config["fund_config"]
            FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"] = {}
        if isinstance(loader_config["round_config"], dict):
            round_short_name = loader_config["round_config"]["short_name"]
            FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"][round_short_name] = loader_config["round_config"]
            FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"][round_short_name]["sections_config"] = loader_config[
                "sections_config"
            ]
            FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"][round_short_name]["base_path"] = loader_config[
                "base_path"
            ]

        # Allows for one file per fund and not redefining the fund information each time
        if isinstance(loader_config["round_config"], list):
            for round_config in loader_config["round_config"]:
                round_short_name = round_config["short_name"]
                FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"][round_short_name] = round_config
                # assumes the same section config for each round but updates with a fresh base path each time
                updated_sections = copy.deepcopy(loader_config["sections_config"])
                for section in updated_sections:
                    tree_path = section["tree_path"]
                    path_elements = str(tree_path).split(".")
                    tree_path = path_elements[1:]
                    tree_path = str(round_config["base_path"]) + "." + ".".join(tree_path)
                    section["tree_path"] = tree_path
                FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"][round_short_name]["sections_config"] = (
                    updated_sections
                )
