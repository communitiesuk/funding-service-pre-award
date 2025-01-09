import json
import os

import pytest

from pre_award.fund_store.db.models.section import Section
from pre_award.fund_store.scripts.all_questions.generate_test_data import (
    HOW_IS_ORG_CLASSIFIED,
    JOINT_BID,
    START_TO_MAIN_ACTIVITIES,
    generate_test_data,
)
from pre_award.fund_store.scripts.all_questions.metadata_utils import (
    build_components_from_page,
    build_hierarchy_levels_for_page,
    build_section_header,
    generate_metadata,
    update_wording_for_multi_input_fields,
)
from pre_award.fund_store.scripts.all_questions.read_forms import (
    increment_lowest_in_hierarchy,
    remove_lowest_in_hierarchy,
    strip_leading_numbers,
)
from pre_award.fund_store.scripts.generate_all_questions import find_forms_dir

TEST_METADATA_FOLDER = "./tests/fund_store_tests/test_data/all_questions/metadata/"
TEST_FORMS_FOLDER = "./tests/fund_store_tests/test_data/all_questions/forms/"


@pytest.mark.skip(reason="Generates test data")
def test_generate_metadata():
    """Used to save generated metadata to a file, so taht file can be used for static test data"""
    filename = "organisation-information-cof-r3-w2.json"
    path_to_form = os.path.join(
        "/path/to/digital-form-builder/fsd_config/form_jsons/cof_r3w2/en/",
        filename,
    )
    with open(path_to_form, "r") as f:
        form_data = json.load(f)
    metadata = generate_metadata(full_form_data=form_data)
    with open(os.path.join(TEST_METADATA_FOLDER, f"metadata_{filename}"), "w") as f:
        json.dump(metadata, f)


@pytest.mark.skip(reason="Generates test data")
def test_generate_test_data():
    """Used to extract a small part of metadata for easier testing."""
    output_folder = "/some/temp/folder"
    files_to_generate = [START_TO_MAIN_ACTIVITIES, HOW_IS_ORG_CLASSIFIED, JOINT_BID]
    generate_test_data(
        target_test_files=files_to_generate,
        in_path=os.path.join(TEST_METADATA_FOLDER, "some_file_name.json"),
        out_folder=output_folder,
    )


def test_generate_index_org_info_cof_r3w2():
    with open(os.path.join(TEST_METADATA_FOLDER, "metadata_org_info_cof_r3w2.json"), "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(p for p in form_data["all_pages"] if p["path"] == form_data["start_page"])
    build_hierarchy_levels_for_page(first_page, results, 1, form_data["all_pages"], start_page=True)

    assert len(results) == 18
    org_details_level = results["/organisation-names"]
    assert results["/alternative-names-of-your-organisation"] == org_details_level + 1
    assert results["/purpose-and-activities"] == org_details_level
    assert results["/previous-projects-similar-to-this-one"] == org_details_level + 1

    assert results["/how-your-organisation-is-classified"] == org_details_level
    assert results["/how-your-organisation-is-classified-other"] == org_details_level + 1
    # TODO why does this fail assert results["/registration-details"] == org_details_level
    assert results["/trading-subsidiaries"] == org_details_level
    assert results["/parent-organisation-details"] == org_details_level + 1

    assert results["/organisation-address"] == org_details_level
    assert results["/correspondence-address"] == org_details_level + 1
    assert results["/joint-applications"] == org_details_level
    assert results["/partner-organisation-details"] == org_details_level + 1


def test_generate_index_applicant_ns():
    with open(os.path.join(TEST_METADATA_FOLDER, "metadata_applicant_ns.json"), "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(p for p in form_data["all_pages"] if p["path"] == form_data["start_page"])
    build_hierarchy_levels_for_page(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 4
    start_level = results["/13-applicant-information"]
    assert results["/lead-contact-details"] == start_level
    assert results["/authorised-signatory-details"] == start_level + 1
    assert results["/summary"] == start_level


def test_generate_index_risk_cyp():
    with open(os.path.join(TEST_METADATA_FOLDER, "metadata_risk_cyp.json"), "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(p for p in form_data["all_pages"] if p["path"] == form_data["start_page"])
    build_hierarchy_levels_for_page(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 5
    start_level = results["/intro-risk-and-deliverability"]
    for _, value in results.items():
        assert value == start_level


def test_generate_index_name_app_cyp():
    with open(os.path.join(TEST_METADATA_FOLDER, "metadata_name_app_cyp.json"), "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(p for p in form_data["all_pages"] if p["path"] == form_data["start_page"])
    build_hierarchy_levels_for_page(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 2
    start_level = results["/name-your-application"]
    assert results["/summary"] == start_level


def test_generate_index_branch_out_multi_pages_back_to_parent_sibling():
    with open(os.path.join(TEST_METADATA_FOLDER, "joint_bid_out_and_back.json"), "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(p for p in form_data["all_pages"] if p["path"] == form_data["start_page"])
    build_hierarchy_levels_for_page(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 5
    start_level = results["/joint-bid"]
    assert results["/partner-organisation-details"] == start_level + 1
    assert results["/work-with-partner-organisations"] == start_level + 1
    assert results["/agreement-exists"] == start_level + 1
    assert results["/website-and-social-media"] == start_level


def test_generate_index_branch_out_all_back_to_new():
    with open(os.path.join(TEST_METADATA_FOLDER, "how_is_org_classified.json"), "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(p for p in form_data["all_pages"] if p["path"] == form_data["start_page"])
    build_hierarchy_levels_for_page(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 5
    start_level = results["/how-is-your-organisation-classified"]
    assert results["/how-is-your-organisation-classified-other"] == start_level + 1
    assert results["/charity-number"] == start_level + 1
    assert results["/company-registration-number"] == start_level + 1
    assert results["/organisation-address"] == start_level


def test_generate_index_simple_branch():
    with open(os.path.join(TEST_METADATA_FOLDER, "start_to_main_activites.json"), "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(p for p in form_data["all_pages"] if p["path"] == form_data["start_page"])
    build_hierarchy_levels_for_page(first_page, results, 1, form_data["all_pages"])

    assert len(results) == 4
    org_details_level = results["/organisation-details"]
    assert results["/alternative-organisation-name"] == org_details_level + 1
    assert results["/tell-us-about-your-organisations-main-activities"] == org_details_level


def test_generate_index_about_your_org_cyp():
    with open(os.path.join(TEST_METADATA_FOLDER, "metadata_about_your_org_cyp.json"), "r") as f:
        form_data = json.load(f)

    results = {}

    first_page = next(p for p in form_data["all_pages"] if p["path"] == form_data["start_page"])
    build_hierarchy_levels_for_page(first_page, results, 1, form_data["all_pages"], start_page=True)

    assert len(results) == 16
    org_details_level = results["/organisation-details"]
    assert results["/alternative-organisation-name"] == org_details_level + 1
    assert results["/tell-us-about-your-organisations-main-activities"] == org_details_level
    assert results["/how-is-your-organisation-classified"] == org_details_level
    assert results["/how-is-your-organisation-classified-other"] == org_details_level + 1
    assert results["/organisation-address"] == org_details_level


@pytest.mark.parametrize(
    "number,exp",
    [
        ("5.1", "5"),
        ("5.0.0", "5.0"),
        ("5.1.2", "5.1"),
        ("5", ""),
        ("5.1.2.3.4.6", "5.1.2.3.4"),
    ],
)
def test_remove_lowest_in_hierarchy(number, exp):
    assert remove_lowest_in_hierarchy(number) == exp


@pytest.mark.parametrize(
    "number,exp",
    [
        ("5.1", "5.2"),
        ("5.1.", "5.2"),
        ("5.1.2", "5.1.3"),
        ("5", "6"),
        ("5.1.2.3.4.5", "5.1.2.3.4.6"),
    ],
)
def test_increment_lowest_in_hierarchy(number, exp):
    assert increment_lowest_in_hierarchy(number) == exp


@pytest.mark.parametrize(
    "text,exp",
    [
        ("5.1 hello", "hello"),
        ("5.1. hello", "hello"),
        ("55.1. hello", "hello"),
        ("5.13. hello", "hello"),
        ("hello", "hello"),
    ],
)
def test_strip_leading_numbers(text, exp):
    assert strip_leading_numbers(text) == exp


@pytest.mark.parametrize(
    "section,lang,exp_anchor,exp_text",
    [
        (
            Section(title_json={"en": "Before You Start"}),
            "en",
            "before-you-start",
            "Before You Start",
        ),
        (
            Section(title_json={"en": "1. Before You Start"}),
            "en",
            "before-you-start",
            "Before You Start",
        ),
        (
            Section(title_json={"en": "Before You Start", "cy": "Welsh"}),
            "cy",
            "welsh",
            "Welsh",
        ),
        (
            Section(title_json={"en": "Before You Start", "cy": "10. Welsh"}),
            "cy",
            "welsh",
            "Welsh",
        ),
    ],
)
def test_build_section_headers(section, lang, exp_anchor, exp_text):
    res_anchor, res_text = build_section_header(section, lang)
    assert res_anchor == exp_anchor
    assert res_text == exp_text


def test_find_forms_dir_no_lang(tmp_path):
    temp_json_dir = os.path.join(tmp_path, "form_jsons")
    os.mkdir(temp_json_dir)
    round_dir = os.path.join(temp_json_dir, "f1_r1")
    os.mkdir(round_dir)
    result = find_forms_dir(temp_json_dir, "f1", "r1", "en")
    assert result == round_dir


def test_find_forms_dir_with_lang(tmp_path):
    temp_json_dir = os.path.join(tmp_path, "form_jsons")
    os.mkdir(temp_json_dir)
    round_dir = os.path.join(temp_json_dir, "f1_r1")
    os.mkdir(round_dir)
    round_dir = os.path.join(round_dir, "en")
    os.mkdir(round_dir)
    result = find_forms_dir(temp_json_dir, "f1", "r1", "en")
    assert result == round_dir


def test_generate_component_display_name_your_app():
    with open(
        os.path.join(TEST_FORMS_FOLDER, "name-your-application.json"),
        "r",
    ) as f:
        form_json = json.load(f)
    page_json = next(p for p in form_json["pages"] if p["path"] == "/11-name-your-application")
    components = build_components_from_page(page_json, include_html_components=True)
    assert len(components) == 1
    assert components[0]["title"] == "Name your application"


def test_build_components_empty_text_and_title():
    with open(
        os.path.join(TEST_FORMS_FOLDER, "about-your-organisation-cyp.json"),
        "r",
    ) as f:
        form_json = json.load(f)

    # Test intro has no text
    page_json = next(p for p in form_json["pages"] if p["path"] == "/intro-about-your-organisation")
    components = build_components_from_page(page_json, include_html_components=False)
    assert len(components) == 0


def test_build_components_include_options_from_radios_and_branching_text():
    with open(
        os.path.join(TEST_FORMS_FOLDER, "about-your-organisation-cyp.json"),
        "r",
    ) as f:
        form_json = json.load(f)

    # Test if for all options in how classified
    page_json = next(p for p in form_json["pages"] if p["path"] == "/how-is-your-organisation-classified")
    components = build_components_from_page(
        page_json,
        include_html_components=False,
        form_lists=form_json["lists"],
        form_conditions=form_json["conditions"],
        index_of_printed_headers={
            "/how-is-your-organisation-classified-other": {"heading_number": "1"},
            "/charity-number": {"heading_number": "2"},
            "/company-registration-number": {"heading_number": "3"},
        },
    )

    assert len(components) == 1
    assert components[0]["hide_title"] is True
    assert len(components[0]["text"]) == 4
    assert components[0]["text"][0] == "Select one option"
    assert isinstance(components[0]["text"][1], list)
    assert len(components[0]["text"][1]) == 6
    assert components[0]["text"][2] == "If 'Other', go to <strong>1</strong>"


def test_build_components_bullets_in_hint():
    with open(
        os.path.join(TEST_FORMS_FOLDER, "your-skills-and-experience-dpi.json"),
        "r",
    ) as f:
        form_json = json.load(f)

    page_json = next(p for p in form_json["pages"] if p["path"] == "/similar-previous-projects")
    components = build_components_from_page(page_json, include_html_components=False)
    assert len(components) == 1
    assert len(components[0]["text"]) == 3
    assert components[0]["text"][2] == "(Max 250 words)"
    assert len(components[0]["text"][1]) == 3


def test_build_components_multi_input():
    with open(os.path.join(TEST_FORMS_FOLDER, "risk-and-deliverability-cyp.json"), "r") as f:
        form_json = json.load(f)
    page_json = next(p for p in form_json["pages"] if p["path"] == "/risks-to-the-project")
    components = build_components_from_page(
        page_json,
        include_html_components=True,
        form_lists=form_json["lists"],
    )

    # TODO - print header with bullet lists, remove 'multiinput needed' text
    assert len(components) == 2
    assert len(components[1]["text"]) == 6


@pytest.mark.parametrize(
    "input_text,exp_result_length",
    [
        (["You can add more stuff on the next step"], 0),
        (["You can add more stuff on the next step", "something else"], 1),
        (["You can add more stuff on the next step", ["a list"], "something else"], 2),
        (["asdfasdfasdf"], 1),
        (["You can add more stuff on the next step. And do something else"], 0),
        (["You can add more on the next step"], 1),
        (["You can add DIFFERENT the next step"], 1),
    ],
)
def test_update_wording_for_multi_input_fields(input_text, exp_result_length):
    result = update_wording_for_multi_input_fields(input_text)
    assert len(result) == exp_result_length
