def alpha_numeric_sort_section(index, section_config, tree_base_path):
    an_sorted_sections = []
    top_section_tree_level = f"{tree_base_path}.{index + 1}"
    an_sorted_sections.append(
        {
            "section_name": str(section_config["section_title"]["en"]),
            "tree_path": str(top_section_tree_level),
        }
    )

    for index, form_section in enumerate(section_config["ordered_form_names_within_section"]):
        current_form_section_tree_level = index + 1
        an_sorted_sections.append(
            {
                "section_name": str(form_section["en"]).replace("-", " ").title(),
                "tree_path": str(f"{top_section_tree_level}.{current_form_section_tree_level}"),
                "form_name": form_section["en"],
            }
        )
    return an_sorted_sections


def sort_sections_from_config(sections_config, tree_base_path):
    all_an_sorted_sections = []
    for index, sc in enumerate(sections_config):
        all_an_sorted_sections += alpha_numeric_sort_section(index, sc, tree_base_path)
    return all_an_sorted_sections


def return_numerically_sorted_section_for_application(application_display_config, tree_base_path):
    return {"sorted_sections": sort_sections_from_config(application_display_config, tree_base_path)}
