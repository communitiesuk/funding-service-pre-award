from fund_store.config.fund_loader_config.cof.deprecated_fund_config.assessment_section_config import (
    scored_sections,
    unscored_sections,
)


def map_fields(fields, all_fields):
    ordered_fields = []
    for index, field in enumerate(fields):
        # check to see if there are grouped fields
        # they should be shown in a single assessment component - grouped
        # therefore give them the same display order
        if type(field["field_id"]) is list:
            for index, grouped_field in enumerate(field["field_id"]):
                ordered_fields.append({"form_json_id": grouped_field, "display_order": 10 * (index + 1)})
                all_fields.append(
                    {
                        "form_json_id": grouped_field,
                        "type": field["field_type"],
                        "presentation_type": field["presentation_type"],
                        "title": field["question"],
                    }
                )
        else:
            ordered_fields.append({"form_json_id": field["field_id"], "display_order": 10 * (index + 1)})
            all_fields.append(
                {
                    "form_json_id": field["field_id"],
                    "type": field["field_type"],
                    "presentation_type": field["presentation_type"],
                    "title": field["question"],
                }
            )

    return ordered_fields


def alpha_numeric_sort_section(
    index,
    section_config,
    all_an_sorted_sections,
    all_fields,
    nested_keys_in_config,
    parent_tree_path,
    depth_count,
):
    # resets when we drop down to the next tree level
    current_tree_path = index + 1

    # depth count tracks the level of recursive call
    if depth_count < len(nested_keys_in_config):
        next_level_key = nested_keys_in_config[depth_count]
        depth_count += 1
    else:
        next_level_key = None

    # If there is a parent tree path then this should prepend the current tree path
    tree_path = f"{parent_tree_path}.{current_tree_path}" if parent_tree_path else current_tree_path

    # Add current section
    new_section = {
        "section_name": section_config["id"],
        "tree_path": tree_path,
        "weighting": section_config["weighting"] if "weighting" in section_config else None,
    }

    # Check if this section has field_ids and then add section
    if "answers" in section_config:
        all_an_sorted_sections += [{**new_section, "fields": map_fields(section_config["answers"], all_fields)}]
    else:
        all_an_sorted_sections += [{**new_section}]

    # Before continuing to the next iteration at this level, check is there are any sub_levels to iterate through
    if next_level_key:
        for index, sub_section_config in enumerate(section_config[next_level_key]):
            alpha_numeric_sort_section(
                index,
                sub_section_config,
                all_an_sorted_sections,
                all_fields,
                nested_keys_in_config,
                tree_path,
                depth_count,
            )


def sort_sections_from_config(sections_config, sub_keys, all_fields, starting_path):
    all_an_sorted_sections = []
    for index, sc in enumerate(sections_config):
        alpha_numeric_sort_section(index, sc, all_an_sorted_sections, all_fields, sub_keys, starting_path, 0)
    return all_an_sorted_sections


def return_numerically_sorted_section_for_assessment(scored_sections, unscored_sections):
    sub_keys = ["sub_criteria", "themes"]
    all_fields = []
    return {
        "sorted_scored_sections": sort_sections_from_config(scored_sections, sub_keys, all_fields, 1),
        "sorted_unscored_sections": sort_sections_from_config(unscored_sections, sub_keys, all_fields, 2),
        "all_fields": all_fields,
    }


sorted_sections_and_field_ids = return_numerically_sorted_section_for_assessment(scored_sections, unscored_sections)
