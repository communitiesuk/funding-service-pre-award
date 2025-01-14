import pytest

from pre_award.fund_store.db.queries import (
    get_all_funds,
    get_fund_by_id,
    get_fund_by_short_name,
    get_round_by_id,
    get_round_by_short_name,
    get_rounds_for_fund_by_id,
    get_rounds_for_fund_by_short_name,
)
from services.data.models.fund import FundingType


def test_get_fund_by_id(seed_dynamic_data):
    f = get_fund_by_id(seed_dynamic_data["funds"][0]["id"])
    assert f.name_json["en"] == "Unit Test Fund 1"
    assert f.short_name == "FND1"
    assert hasattr(f, "ggis_scheme_reference_number")
    assert f.ggis_scheme_reference_number == ""


def test_get_fund_by_short_name(seed_dynamic_data):
    f = get_fund_by_short_name("FND1")
    assert f.name_json["en"] == "Unit Test Fund 1"
    assert f.short_name == "FND1"


def test_get_round_by_id(seed_dynamic_data):
    r = get_round_by_id(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][0]["id"],
    )
    assert r.title_json["en"] == "Unit Test Round 1"
    assert r.short_name == "RND1"
    assert str(r.id) == seed_dynamic_data["funds"][0]["rounds"][0]["id"]


def test_get_rounds_for_fund_by_id(seed_dynamic_data):
    r = get_rounds_for_fund_by_id(seed_dynamic_data["funds"][0]["id"])
    assert len(r) == 2
    # assert r[0].title_json["en"] == "Unit Test Round 1"
    assert r[0].short_name == "RND1"
    assert r[1].short_name == "RND2"
    assert str(r[0].id) == seed_dynamic_data["funds"][0]["rounds"][0]["id"]


def test_get_rounds_for_fund_by_short_name(seed_dynamic_data):
    r = get_rounds_for_fund_by_short_name("FND1")
    assert len(r) == 2
    # assert r[0].title_json["en"] == "Unit Test Round 1"
    assert r[0].short_name == "RND1"
    assert r[1].short_name == "RND2"
    assert str(r[0].id) == seed_dynamic_data["funds"][0]["rounds"][0]["id"]


@pytest.mark.parametrize(
    "fund_short_name, round_short_name, expected_none, expected_title",
    [
        ("FND1", "RND1", False, "Unit Test Round 1"),
        ("fnd1", "rnd1", False, "Unit Test Round 1"),
        ("bad", "rnd1", True, None),
        ("fund", "bad", True, None),
        ("FND1", "RND2", False, "Unit Test Round 2"),
    ],
)
def test_get_round_by_short_name(
    fund_short_name,
    round_short_name,
    expected_none,
    expected_title,
    seed_dynamic_data,
):
    r = get_round_by_short_name(fund_short_name, round_short_name)

    if expected_none:
        assert r is None
    else:
        assert r.title_json["en"] == expected_title


def test_get_all_funds(seed_dynamic_data):
    result = get_all_funds()
    assert len(result) == 1
    assert result[0].name_json["en"] == "Unit Test Fund 1"
    assert result[0].funding_type == FundingType.COMPETITIVE
