def _transform_fund_configuration(loader_config, fab_fund_round_configs):
    """
    Transform a single fund configuration from FAB export format to internal structure.
    Organizes fund and round data for database processing.
    """
    import copy

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


def prepare_fund_data_for_processing(loader_config):
    """
    Prepare fund configuration data from FAB export for database processing.
    Returns structured fund data ready for saving to database.
    """
    fab_fund_round_configs = {}
    _transform_fund_configuration(loader_config, fab_fund_round_configs)
    fund_short_name = loader_config["fund_config"]["short_name"]
    return fab_fund_round_configs[fund_short_name]


def load_fund_configurations_from_directory(fab_directory_path):
    """
    Load and consolidate all fund configurations from Python files in a directory.
    Used by the existing loader scripts to bulk process fund setups.
    """
    import ast
    import os

    fab_fund_round_configs = {}

    for file in os.listdir(fab_directory_path):
        if file.startswith("__") or not file.endswith(".py"):
            continue

        with open(fab_directory_path / file, "r") as json_file:
            content = json_file.read()
            if content.startswith("LOADER_CONFIG = "):
                content = content.split("LOADER_CONFIG = ")[1]
            elif content.startswith("LOADER_CONFIG="):
                content = content.split("LOADER_CONFIG=")[1]
            else:
                raise ValueError(f"fund config file {file.title()} does not start with 'LOADER_CONFIG='")

            loader_config = ast.literal_eval(content)
            _transform_fund_configuration(loader_config, fab_fund_round_configs)

    return fab_fund_round_configs
