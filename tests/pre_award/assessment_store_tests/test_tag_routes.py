import pytest
from flask import url_for

from tests.pre_award.assessment_store_tests.conftest import test_input_data


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_associate_tags_with_assessment_empty_return(app, flask_test_client, seed_application_records):
    resp = flask_test_client.put(
        url_for(
            "assessment_store_bp.assessment_tag_bp.associate_tags_with_assessment",
            application_id=seed_application_records[0]["application_id"],
        ),
        json=[],
    )
    assert resp.json == []
