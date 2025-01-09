import json

import pytest

from pre_award.assessment_store.db.queries.assessment_records._helpers import (
    derive_application_values,
    get_location_json_from_postcode,
)


@pytest.fixture(scope="function")
def mock_data_key_mappings(monkeypatch):
    fund_round_data_key_mappings = {
        "TESTREF": {
            "location": "yEmHpp",
            "asset_type": "yaQoxU",
            "funding_one": "JzWvhj",
            "funding_two": "jLIgoi",
        }
    }
    monkeypatch.setattr(
        "pre_award.assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )
    yield


def test_derive_cof_values_no_location(app, mock_data_key_mappings):
    single_application_json = "tests/assessment_store_tests/test_data/single_application_no_location.json"

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)
    derived_fields = derive_application_values(loaded_test_json)
    assert "TEST-REF" == derived_fields["short_id"]
    assert "funding-service-design" == derived_fields["fund_id"]
    assert "summer" == derived_fields["round_id"]
    assert "test-application-id" == derived_fields["application_id"]
    assert "Project name" == derived_fields["project_name"]
    assert "community-centre" == derived_fields["asset_type"]

    assert derived_fields["location_json_blob"]["error"] is True
    assert "Not Available" == derived_fields["location_json_blob"]["county"]


@pytest.mark.parametrize(
    "postcode,expected_country",
    [
        ("B90 4RF", "England"),
        ("EX22 6TA", "England"),
    ],
)
def test_derive_cof_values_location_present_no_error(app, postcode, expected_country, mock_data_key_mappings):
    single_application_json = "tests/assessment_store_tests/test_data/single_application_no_location.json"

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)
        # set mock location in json
        loaded_test_json["forms"][12]["questions"][2]["fields"][0]["answer"] = (
            f"Test Address,null, Test Town Or City,null, {postcode}"
        )

    derived_fields = derive_application_values(loaded_test_json)
    assert "TEST-REF" == derived_fields["short_id"]

    assert derived_fields["location_json_blob"]["error"] is False
    assert expected_country == derived_fields["location_json_blob"]["country"]


def test_derive_cof_values_location_present_with_error(app, mock_data_key_mappings):
    single_application_json = "tests/assessment_store_tests/test_data/single_application_no_location.json"

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)
    derived_fields = derive_application_values(loaded_test_json)
    assert "TEST-REF" == derived_fields["short_id"]

    assert derived_fields["location_json_blob"]["error"] is True
    assert "Not Available" == derived_fields["location_json_blob"]["county"]


@pytest.mark.parametrize(
    "field_one, field_two,funding_field_type, exp_total",
    [
        ("JzWvhj", "jLIgoi", None, 4700),
        (None, "jLIgoi", None, 2400),
        ("JzWvhj", None, None, 2300),
        (None, None, None, 0),
        ("both", "wrong", None, 0),
        ("bad", "jLIgoi", None, 2400),
        ("JzWvhj", "wrong", None, 2300),
        (["JzWvhj"], ["jLIgoi"], "multiInputField", 4700),
        (["JzWvhj"], [None], "multiInputField", 2300),
        (["JzWvhj"], ["incorrect"], "multiInputField", 2300),
        ([None], ["jLIgoi"], "multiInputField", 2400),
        (["baad"], ["jLIgoi"], "multiInputField", 2400),
        (["both lists"], ["are wrong"], "multiInputField", 0),
    ],
)
def test_derive_funding(app, exp_total, field_one, field_two, funding_field_type, monkeypatch):
    fund_round_data_key_mappings = {
        "TESTREF": {
            "location": None,
            "asset_type": None,
            "funding_one": field_one,
            "funding_two": field_two,
            "funding_field_type": funding_field_type,
        }
    }
    monkeypatch.setattr(
        "pre_award.assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )
    single_application_json = "tests/assessment_store_tests/test_data/single_application_no_location.json"
    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)
    derived_fields = derive_application_values(loaded_test_json)
    assert "TEST-REF" == derived_fields["short_id"]
    assert derived_fields["funding_amount_requested"] == exp_total


def test_get_location_request_error(app, mocker):
    mocker.patch(
        "pre_award.assessment_store.db.queries.assessment_records._helpers.requests.post", side_effect=Exception()
    )
    location_data = get_location_json_from_postcode("AA12 1DB")
    assert location_data is None
