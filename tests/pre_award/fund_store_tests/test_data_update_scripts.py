from pre_award.fund_store.db.queries import (
    get_application_sections_for_round,
    get_fund_by_id,
    get_round_by_id,
)
from pre_award.fund_store.db.schemas.fund import FundSchema
from pre_award.fund_store.db.schemas.round import RoundSchema
from pre_award.fund_store.db.schemas.section import SectionSchema
from pre_award.fund_store.scripts.data_updates.FS2910_ns_links import update_rounds_with_links
from pre_award.fund_store.scripts.data_updates.FS2956_ns_weightings import update_section_weightings
from pre_award.fund_store.scripts.data_updates.patch_cyp_name import update_fund_name


def test_update_section_weightings(seed_dynamic_data):
    sections = get_application_sections_for_round(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][0]["id"],
    )
    section_to_update = None
    for s in sections:
        if "skill" in s.title_json["en"]:
            section_to_update = s
    assert section_to_update is not None, "Unable to find expected test data before updates"

    section_data = SectionSchema().dump(section_to_update)
    section_data["tree_path"] = section_to_update.path
    section_data["section_name"] = section_to_update.title_json
    section_data["weighting"] = "12"
    update_section_weightings(section_data)

    sections = get_application_sections_for_round(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][0]["id"],
    )

    for s in sections:
        if "skill" in s.title_json["en"]:
            section = s
    assert section.weighting == 12


def test_update_links_present(seed_dynamic_data):
    r = get_round_by_id(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][0]["id"],
    )
    round_data = RoundSchema().dump(r)
    round_data["privacy_notice"] = "new privacy notice"
    round_data["prospectus"] = "new prospectus"

    update_rounds_with_links([round_data])

    r = get_round_by_id(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][0]["id"],
    )

    assert r.privacy_notice == "new privacy notice"
    assert r.prospectus == "new prospectus"


def test_update_links_not_present(seed_dynamic_data):
    r = get_round_by_id(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][1]["id"],
    )
    round_data = RoundSchema().dump(r)
    round_data["privacy_notice"] = ""
    round_data["prospectus"] = ""

    update_rounds_with_links([round_data])

    r = get_round_by_id(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][1]["id"],
    )

    assert r.privacy_notice == "http://google.com"
    assert r.prospectus == "http://google.com"


def test_update_fund_name(seed_dynamic_data):
    f = get_fund_by_id(seed_dynamic_data["funds"][0]["id"])
    fund_data = FundSchema().dump(f)
    fund_data["name_json"] = "new name json"

    update_fund_name(fund_config=fund_data)

    f = get_fund_by_id(seed_dynamic_data["funds"][0]["id"])
    assert f.name_json == "new name json"
