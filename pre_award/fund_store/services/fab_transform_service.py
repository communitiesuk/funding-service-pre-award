import copy


def transform_fund_configuration(loader_config):
    """
    Transform a single fund configuration from FAB export format to internal structure.
    Returns the fund data directly without nesting under fund name.
    """
    if not loader_config.get("fund_config", None):
        raise ValueError("No fund_config found in loader config")
    if not loader_config.get("round_config", None):
        raise ValueError("No round_config found in loader config")

    # Start with the fund config as base
    fund_data = loader_config["fund_config"].copy()
    fund_data["rounds"] = {}

    if isinstance(loader_config["round_config"], dict):
        round_short_name = loader_config["round_config"]["short_name"]
        fund_data["rounds"][round_short_name] = loader_config["round_config"]
        fund_data["rounds"][round_short_name]["sections_config"] = loader_config["sections_config"]
        fund_data["rounds"][round_short_name]["base_path"] = loader_config["base_path"]

    # Handle multiple rounds in one config
    if isinstance(loader_config["round_config"], list):
        for round_config in loader_config["round_config"]:
            round_short_name = round_config["short_name"]
            fund_data["rounds"][round_short_name] = round_config
            # Update section config with round-specific base path
            updated_sections = copy.deepcopy(loader_config["sections_config"])
            for section in updated_sections:
                tree_path = section["tree_path"]
                path_elements = str(tree_path).split(".")
                tree_path = path_elements[1:]
                tree_path = str(round_config["base_path"]) + "." + ".".join(tree_path)
                section["tree_path"] = tree_path
            fund_data["rounds"][round_short_name]["sections_config"] = updated_sections

    return fund_data
