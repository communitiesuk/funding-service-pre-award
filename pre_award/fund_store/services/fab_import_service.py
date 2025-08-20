import copy


def transform_fund_configuration(loader_config):
    """
    Transform a single fund configuration from FAB export format to internal structure.
    Organizes fund and round data for database processing.
    """
    fab_fund_round_configs = {}

    if not loader_config.get("fund_config", None):
        print("No fund config found in the loader config.")
        raise ValueError("No fund_config found in loader config")
    if not loader_config.get("round_config", None):
        print("No round config found in the loader config.")
        raise ValueError("No round_config found in loader config")

    fund_short_name = loader_config["fund_config"]["short_name"]

    # Ensure the fund exists in the main config
    if fund_short_name not in fab_fund_round_configs:
        fab_fund_round_configs[fund_short_name] = loader_config["fund_config"]
        fab_fund_round_configs[fund_short_name]["rounds"] = {}

    if isinstance(loader_config["round_config"], dict):
        round_short_name = loader_config["round_config"]["short_name"]
        fab_fund_round_configs[fund_short_name]["rounds"][round_short_name] = loader_config["round_config"]
        fab_fund_round_configs[fund_short_name]["rounds"][round_short_name]["sections_config"] = loader_config[
            "sections_config"
        ]
        fab_fund_round_configs[fund_short_name]["rounds"][round_short_name]["base_path"] = loader_config["base_path"]

    # Allows for one file per fund and not redefining the fund information each time
    if isinstance(loader_config["round_config"], list):
        for round_config in loader_config["round_config"]:
            round_short_name = round_config["short_name"]
            fab_fund_round_configs[fund_short_name]["rounds"][round_short_name] = round_config
            # assumes the same section config for each round but updates with a fresh base path each time
            updated_sections = copy.deepcopy(loader_config["sections_config"])
            for section in updated_sections:
                tree_path = section["tree_path"]
                path_elements = str(tree_path).split(".")
                tree_path = path_elements[1:]
                tree_path = str(round_config["base_path"]) + "." + ".".join(tree_path)
                section["tree_path"] = tree_path
            fab_fund_round_configs[fund_short_name]["rounds"][round_short_name]["sections_config"] = updated_sections

    return fab_fund_round_configs
