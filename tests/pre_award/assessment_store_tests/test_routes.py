import json
import logging
from copy import deepcopy
from datetime import datetime
from unittest import mock
from uuid import uuid4

import pytest
from pytest import approx
from sqlalchemy import select

from pre_award.assessment_store.api.routes.assessment_routes import (
    calculate_overall_score_percentage_for_application,
)
from pre_award.assessment_store.config.mappings.assessment_mapping_fund_round import (
    applicant_info_mapping,
)
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.models.flags.assessment_flag import AssessmentFlag
from pre_award.assessment_store.db.models.flags.flag_update import FlagStatus
from pre_award.assessment_store.db.models.tag.tags import Tag
from pre_award.assessment_store.db.queries.assessment_records.queries import get_export_data
from pre_award.assessment_store.db.queries.flags.queries import add_flag_for_application, add_update_to_assessment_flag
from pre_award.assessment_store.db.queries.qa_complete.queries import create_qa_complete_record
from services.notify import NotificationError
from tests.pre_award.assessment_store_tests._expected_responses import APPLICATION_METADATA_RESPONSE
from tests.pre_award.assessment_store_tests.conftest import test_input_data
from tests.pre_award.assessment_store_tests.test_data.flags import (
    add_flag_update_request_json,
    create_flag_request_json,
)

COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_W3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"
NS_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NS_ROUND_2_ID = "fc7aa604-989e-4364-98a7-d1234271435a"


@pytest.mark.apps_to_insert(test_input_data)
def test_get_assessments_stats(flask_test_client, seed_application_records, seed_scoring_system):
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]

    # Get test applications
    applications = flask_test_client.get(f"/assessment/application_overviews/{fund_id}/{round_id}").json

    request = flask_test_client.post(f"/assessment/assessments/get-stats/{fund_id}", json={"round_ids": [round_id]})
    assessment_stats = request.json.get(round_id)
    assert assessment_stats["qa_completed"] == 0

    create_qa_complete_record(applications[0]["application_id"], "usera")

    request = flask_test_client.post(f"/assessment/assessments/get-stats/{fund_id}", json={"round_ids": [round_id]})
    assessment_stats = request.json.get(round_id)
    assert assessment_stats["qa_completed"] == 1

    create_qa_complete_record(applications[1]["application_id"], "usera")

    flag_id = add_flag_for_application(
        justification="I think things.",
        sections_to_flag=["Overview"],
        application_id=applications[1]["application_id"],
        user_id="abc",
        status=FlagStatus.RAISED,
        allocation="Assessor",
    ).id

    request = flask_test_client.post(f"/assessment/assessments/get-stats/{fund_id}", json={"round_ids": [round_id]})
    assessment_stats = request.json.get(round_id)
    assert assessment_stats["flagged"] == 1
    assert assessment_stats["qa_completed"] == 1

    add_update_to_assessment_flag(
        justification="I think things.",
        user_id="abc",
        status=FlagStatus.RESOLVED,
        allocation="Assessor",
        assessment_flag_id=flag_id,
    )

    request = flask_test_client.post(f"/assessment/assessments/get-stats/{fund_id}", json={"round_ids": [round_id]})
    assessment_stats = request.json.get(round_id)

    assert assessment_stats["flagged"] == 0
    assert assessment_stats["qa_completed"] == 2


@pytest.mark.apps_to_insert([test_input_data[0].copy() for x in range(4)])
def test_gets_all_apps_for_fund_round(request, flask_test_client, seed_application_records, seed_scoring_system):
    """test_gets_all_apps_for_fund_round Tests that the number of rows returned by
    filtering by round on `assessment_records` matches the number of applications
    per round specified by the test data generation process."""

    picked_row = seed_application_records[0]

    apps_per_round = 4

    random_round_id = picked_row["round_id"]
    random_fund_id = picked_row["fund_id"]
    application_id = picked_row["application_id"]

    response_jsons = flask_test_client.get(f"/assessment/application_overviews/{random_fund_id}/{random_round_id}").json

    assert len(response_jsons) == apps_per_round

    # Define the expected keys and nested keys based on the YAML structure
    expected_keys = {
        "location_json_blob": dict,
        "funding_amount_requested": (int, float),
        "user_associations": list,
        "qa_complete": list,
        "language": str,
        "is_withdrawn": bool,
        "type_of_application": str,
        "flags": list,
        "short_id": str,
        "date_submitted": str,
        "fund_id": str,
        "round_id": str,
        "project_name": str,
        "workflow_status": str,
        "asset_type": str,
        "tag_associations": list,
        "is_qa_complete": bool,
        "overall_score_percentage": (int, float),
    }
    for response_json in response_jsons:
        # Assert that each key is present in the response and has the correct type
        for key, expected_type in expected_keys.items():
            assert key in response_json, f"Missing key: {key}"
            assert isinstance(response_json[key], expected_type), f"Incorrect type for key: {key}"

    # Check application overview returns flags in order of descending
    add_flag_for_application(
        justification="Test 1",
        sections_to_flag=["Overview"],
        application_id=application_id,
        user_id="abc",
        status=FlagStatus.RAISED,
        allocation="Assessor",
    )

    add_flag_for_application(
        justification="Test 2",
        sections_to_flag=["Overview"],
        application_id=application_id,
        user_id="abc",
        status=FlagStatus.RESOLVED,
        allocation="Assessor",
    )

    add_flag_for_application(
        justification="Test 3",
        sections_to_flag=["Overview"],
        application_id=application_id,
        user_id="abc",
        status=FlagStatus.STOPPED,
        allocation="Assessor",
    )

    response_with_flag_json = flask_test_client.get(
        f"/assessment/application_overviews/{random_fund_id}/{random_round_id}"
    ).json

    application_to_check = None
    for application in response_with_flag_json:
        if application["application_id"] == application_id:
            application_to_check = application

    # Check that the last flag in the flag array is the latest flag added
    assert application_to_check["flags"][-1]["updates"][0]["status"] == 1  # 1 = stopped
    assert application_to_check["flags"][-1]["updates"][0]["justification"] == "Test 3"


@pytest.mark.parametrize(
    "url, expected_count",
    [
        (
            f"{COF_FUND_ID}/{COF_ROUND_2_ID}?search_term={test_input_data[0]['reference']}&search_in=short_id",
            1,
        ),
        (
            f"{COF_FUND_ID}/{COF_ROUND_2_ID}?search_term=insertion&search_in=project_name",
            2,
        ),
        (f"{COF_FUND_ID}/{COF_ROUND_2_ID}?asset_type=pub", 1),
        (f"{COF_FUND_ID}/{COF_ROUND_2_ID}?status=NOT_STARTED", 3),
        (
            f"{COF_FUND_ID}/{COF_ROUND_2_ID}?search_term={test_input_data[0]['reference']}"
            + "&search_in=short_id&asset_type=BAD",
            0,
        ),
        (
            f"{COF_FUND_ID}/{COF_ROUND_2_ID}?search_term={test_input_data[0]['reference']}",
            3,
        ),
        (
            f"{NS_FUND_ID}/{NS_ROUND_2_ID}?search_term=shelter&search_in=organisation_name",
            1,
        ),
        (
            f"{NS_FUND_ID}/{NS_ROUND_2_ID}?search_term=bad_search&search_in=organisation_name",
            0,
        ),
        (f"{NS_FUND_ID}/{NS_ROUND_2_ID}?funding_type=capital", 1),
        (f"{NS_FUND_ID}/{NS_ROUND_2_ID}?funding_type=revenue", 0),
        (
            f"{NS_FUND_ID}/{NS_ROUND_2_ID}?search_term=shelter&search_in=organisation_name&funding_type=revenue",
            0,
        ),
    ],
)
@pytest.mark.apps_to_insert(test_input_data)
def test_search(url, expected_count, flask_test_client, seed_application_records):
    response_json = flask_test_client.get("/assessment/application_overviews/" + url).json

    assert len(response_json) == expected_count


@pytest.mark.skip(reason="used for tdd only")
def test_get_application_metadata_for_application_id(flask_test_client):
    response_json = flask_test_client.get("/assessment/application_overviews/a3ec41db-3eac-4220-90db-c92dea049c00").json

    assert response_json == APPLICATION_METADATA_RESPONSE


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria(flask_test_client, seed_application_records):
    """Test to check that sub criteria metadata and ordered themes are returned
    for a COFR2W2 sub criteria."""

    sub_criteria_id = "benefits"
    application_id = seed_application_records[0]["application_id"]
    response_json = flask_test_client.get(f"/assessment/sub_criteria_overview/{application_id}/{sub_criteria_id}").json
    # The order of themes within a sub_criteria is important,
    # ensure it is preserved
    expected_theme_order = ["community_use", "risk_loss_impact"]
    actual_theme_order = []
    for theme in response_json["themes"]:
        actual_theme_order.append(theme["id"])
    assert expected_theme_order == actual_theme_order
    assert "short_id" in response_json
    assert "id" in response_json


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria_metadata_for_false_sub_criteria_id(flask_test_client, seed_application_records):
    """Test to check that sub criteria metadata is not retuned for false sub
    criteria."""

    sub_criteria_id = "does-not-exist"
    application_id = seed_application_records[0]["application_id"]
    response = flask_test_client.get(f"/assessment/sub_criteria_overview/{application_id}/{sub_criteria_id}").json

    assert response["code"] == 404
    assert "sub_criteria: 'does-not-exist' not found." in response["message"]


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_update_ar_status_to_completed(request, flask_test_client, seed_application_records):
    """Test checks that the status code returned by the POST request is 204, which
    indicates that the request was successful and that the application status was
    updated to COMPLETED."""

    application_id = seed_application_records[0]["application_id"]
    response = flask_test_client.post(f"/assessment/application/{application_id}/status/complete")

    assert response.status_code == 204


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_application_json(flask_test_client, seed_application_records):
    application_id = seed_application_records[0]["application_id"]
    response = flask_test_client.get(f"/assessment/application/{application_id}/json")
    assert 200 == response.status_code

    json_blob = response.json
    assert application_id == json_blob["application_id"]


expected_flag = AssessmentFlag(
    application_id=uuid4(),
    id=uuid4(),
    latest_status=FlagStatus.STOPPED,
    latest_allocation="TEAM_2",
    sections_to_flag=[],
    updates=[],
    field_ids=[],
    is_change_request=False,
)


def test_get_flags(flask_test_client, mocker):
    mocker.patch(
        "pre_award.assessment_store.api.routes.flag_routes.get_flags_for_application",
        return_value=[expected_flag],
    )
    response = flask_test_client.get("/assessment/flags/app_id")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == str(expected_flag.id)


@pytest.mark.apps_to_insert([test_input_data[0].copy() for x in range(4)])
def test_get_team_flag_stats(flask_test_client, seed_application_records):
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]
    # Get test applications
    applications = flask_test_client.get(f"/assessment/application_overviews/{fund_id}/{round_id}").json

    # Add a RAISED flag for the first application
    # so that one result from the set is flagged as RAISED
    # and only one team exists with a flag allocated
    add_flag_for_application(
        justification="bob",
        sections_to_flag=["Overview"],
        application_id=applications[0]["application_id"],
        user_id="abc",
        status="RAISED",
        allocation="ASSESSOR",
    )

    response = flask_test_client.get(f"/assessment/assessments/get-team-flag-stats/{fund_id}/{round_id}")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["team_name"] == "ASSESSOR"
    assert response.json[0]["raised"] == 1

    # Add a RAISED flag for second application
    # still only one team exists with a flag allocated
    # response should still have only one row for one team
    # 2 raised
    add_flag_for_application(
        justification="bob",
        sections_to_flag=["Overview"],
        application_id=applications[1]["application_id"],
        user_id="abc",
        status="RAISED",
        allocation="ASSESSOR",
    )

    # Add a RAISED flag for first application
    # for a second team response have 2 rows for the two teams
    add_flag_for_application(
        justification="bob",
        sections_to_flag=["Overview"],
        application_id=applications[0]["application_id"],
        user_id="abc",
        status="RAISED",
        allocation="LEAD_ASSESSOR",
    )

    response = flask_test_client.get(f"/assessment/assessments/get-team-flag-stats/{fund_id}/{round_id}")

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["team_name"] == "ASSESSOR"
    assert response.json[0]["raised"] == 2
    assert response.json[1]["team_name"] == "LEAD_ASSESSOR"
    assert response.json[1]["raised"] == 1


def test_create_flag(flask_test_client):
    request_body = {
        **create_flag_request_json,
        "application_id": str(uuid4()),
    }
    with mock.patch(
        "pre_award.assessment_store.api.routes.flag_routes.add_flag_for_application",
        return_value=expected_flag,
    ) as create_mock:
        response = flask_test_client.post(
            "/assessment/flags/",
            data=json.dumps(request_body),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 200
        create_mock.assert_called_with(**request_body)
        assert response.json["id"] == str(expected_flag.id)


def test_update_flag(flask_test_client):
    request_body = {
        **add_flag_update_request_json,
        "assessment_flag_id": str(uuid4()),
    }
    with mock.patch(
        "pre_award.assessment_store.api.routes.flag_routes.add_update_to_assessment_flag",
        return_value=expected_flag,
    ) as update_mock:
        response = flask_test_client.put(
            "/assessment/flags/",
            data=json.dumps(request_body),
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 200
        update_mock.assert_called_once_with(**request_body)
        assert response.json["id"] == str(expected_flag.id)


def test_get_tag(flask_test_client, mocker):
    tag_id = uuid4()
    mock_tag = Tag(
        id=tag_id,
        value="tag value 1",
        creator_user_id="test-user",
        active=True,
        fund_id=uuid4(),
        round_id=uuid4(),
        type_id=uuid4(),
    )
    with mocker.patch("pre_award.assessment_store.api.routes.tag_routes.get_tag_by_id", return_value=mock_tag):
        response = flask_test_client.get("/assessment/funds/test-fund/rounds/round-id/tags/tag-id")
        assert response.status_code == 200
        assert response.json
        assert response.json["id"] == str(tag_id)


def test_get_tag_none_exists(flask_test_client, mocker):
    with mocker.patch("pre_award.assessment_store.api.routes.tag_routes.get_tag_by_id", return_value=None):
        response = flask_test_client.get("/assessment/funds/test-fund/rounds/round-id/tags/tag-id")
        assert response.status_code == 404


@pytest.mark.apps_to_insert([test_input_data[0].copy() for _ in range(4)])
@pytest.mark.unique_fund_round(True)
@pytest.mark.parametrize(
    "fund_config, round_config, expected_keys",
    [
        (None, None, {"Application ID", "Date Submitted", "Short ID"}),
        (
            {
                "ASSESSOR_EXPORT": {
                    "form_fields": {
                        "aHIGbK": {"en": {"title": "Charity number "}},
                        "aAeszH": {"en": {"title": "Do you need to do any further feasibility work?"}},
                        "ozgwXq": {"en": {"title": "Risks to your project (document upload)"}},
                        "KAgrBz": {"en": {"title": "Project name"}},
                    }
                }
            },
            None,
            {
                "Application ID",
                "Date Submitted",
                "Short ID",
                "Charity number ",
                "Do you need to do any further feasibility work?",
                "Risks to your project (document upload)",
                "Project name",
            },
        ),
        (
            {
                "ASSESSOR_EXPORT": {
                    "form_fields": {
                        "aHIGbK": {"en": {"title": "Charity number "}},
                        "aAeszH": {"en": {"title": "Do you need to do any further feasibility work?"}},
                        "ozgwXq": {"en": {"title": "Risks to your project (document upload)"}},
                        "KAgrBz": {"en": {"title": "Project name"}},
                    }
                }
            },
            {
                "ASSESSOR_EXPORT": {
                    "form_fields": {
                        "xYz123": {"en": {"title": "Special round field"}},
                    }
                }
            },
            {"Application ID", "Date Submitted", "Short ID", "Special round field"},
        ),
    ],
)
def test_get_application_fields_export(
    flask_test_client, seed_application_records, monkeypatch, fund_config, round_config, expected_keys
):
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]

    if round_config:
        monkeypatch.setitem(applicant_info_mapping, f"{fund_id}:{round_id}", round_config)
    if fund_config:
        monkeypatch.setitem(applicant_info_mapping, f"{fund_id}", fund_config)

    result = flask_test_client.get(f"/assessment/application_fields_export/{fund_id}/{round_id}/ASSESSOR_EXPORT").json

    response_keys = set(result["en_list"][0].keys())
    assert response_keys == expected_keys


@pytest.mark.apps_to_insert([test_input_data[0].copy() for x in range(4)])
@pytest.mark.unique_fund_round(True)
def test_get_export_data_with_and_without_timezone(db, seed_application_records):
    round_id = seed_application_records[0]["round_id"]
    assessment_records = db.session.execute(select(AssessmentRecord)).scalars().all()

    # Date strings with and without timezone information
    date_strings = [
        "2023-10-10T14:48:00+00:00",  # UTC with explicit timezone
        "2023-10-10T14:48:00",  # UTC without explicit timezone
        "2023-10-11T10:30:00+00:00",
        "2023-10-11T10:30:00",
    ]
    for record, date_string in zip(assessment_records, date_strings, strict=False):
        record.jsonb_blob["date_submitted"] = date_string

    list_of_fields = {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "aHIGbK": {"en": {"title": "Charity number "}},
                "aAeszH": {"en": {"title": "Do you need to do any further feasibility work?"}},
                "ozgwXq": {"en": {"title": "Risks to your project (document upload)"}},
                "KAgrBz": {"en": {"title": "Project name"}},
            }
        }
    }

    result = get_export_data(
        round_id=round_id,
        report_type="ASSESSOR_EXPORT",
        list_of_fields=list_of_fields,
        assessment_metadatas=assessment_records,
        language="en",
    )

    assert len(result) == 4
    assert result[0]["Date Submitted"] == "10/10/2023 14:48:00"
    assert result[1]["Date Submitted"] == "10/10/2023 14:48:00"
    assert result[2]["Date Submitted"] == "11/10/2023 10:30:00"
    assert result[3]["Date Submitted"] == "11/10/2023 10:30:00"


def test_get_all_users_associated_with_application(flask_test_client):
    mock_users = [
        {
            "application_id": "app1",
            "user_id": "user1",
            "assigner_id": "assigner1",
            "created_at": datetime(2024, 6, 10, 15, 35, 47, 999),
            "active": True,
            "log": "{'activated': '2024-06-10T15:35:47Z'}",
        },
        {
            "application_id": "app1",
            "user_id": "user2",
            "assigner_id": "assigner1",
            "created_at": datetime(2024, 6, 10, 15, 35, 47, 999),
            "active": False,
            "log": "{'activated': '2024-06-10T15:35:47Z', 'deactivated': '2024-06-11T15:35:47Z'}",
        },
    ]

    expected_response = deepcopy(mock_users)
    expected_response[0]["created_at"] = expected_response[0]["created_at"].isoformat()
    expected_response[1]["created_at"] = expected_response[1]["created_at"].isoformat()

    with mock.patch(
        "pre_award.assessment_store.api.routes.user_routes.get_user_application_associations",
        return_value=mock_users,
    ) as mock_get_users:
        response = flask_test_client.get("/assessment/application/app1/users")

        assert response.status_code == 200
        assert response.json == expected_response
        mock_get_users.assert_called_once_with(application_id="app1", active=None)


def test_get_user_application_association(flask_test_client):
    mock_association = {
        "application_id": "app1",
        "user_id": "user1",
        "assigner_id": "assigner1",
        "created_at": datetime(2024, 6, 10, 15, 35, 47, 999),
        "active": True,
        "log": "{'activated': '2024-06-10T15:35:47Z'}",
    }

    expected_response = deepcopy(mock_association)
    expected_response["created_at"] = expected_response["created_at"].isoformat()

    with mock.patch(
        "pre_award.assessment_store.api.routes.user_routes.get_user_application_associations",
        return_value=[mock_association],
    ) as mock_get_association:
        response = flask_test_client.get("/assessment/application/app1/user/user1")

        assert response.status_code == 200
        assert response.json == expected_response
        mock_get_association.assert_called_once_with(application_id="app1", user_id="user1")


@pytest.mark.parametrize(
    "send_email_value, notify_side_effect", [(True, None), (False, None), (True, NotificationError("could not send"))]
)
def test_add_user_application_association(flask_test_client, send_email_value, mocker, notify_side_effect, caplog):
    mock_association = {
        "application_id": "app1",
        "user_id": "user1",
        "assigner_id": "assigner1",
        "created_at": datetime(2024, 6, 10, 15, 35, 47, 999),
        "active": True,
        "log": "{'activated': '2024-06-10T15:35:47Z'}",
    }

    expected_response = deepcopy(mock_association)
    expected_response["created_at"] = expected_response["created_at"].isoformat()

    with (
        mock.patch(
            "pre_award.assessment_store.api.routes.user_routes.create_user_application_association",
            return_value=mock_association,
        ) as mock_create_association,
        mock.patch("pre_award.assessment_store.api.routes.user_routes.get_metadata_for_application"),
        mock.patch("pre_award.assessment_store.api.routes.user_routes.get_account_data"),
        mock.patch("pre_award.assessment_store.api.routes.user_routes.get_fund_data"),
        mock.patch("pre_award.assessment_store.api.routes.user_routes.create_assessment_url_for_application"),
    ):
        mock_notification_service = mock.MagicMock()
        mocker.patch(
            "pre_award.assessment_store.api.routes.user_routes.get_notification_service",
            return_value=mock_notification_service,
        )
        if notify_side_effect:
            mock_notification_service.send_assessment_assigned_email.side_effect = notify_side_effect
        response = flask_test_client.post(
            "/assessment/application/app1/user/user1",
            json={"assigner_id": "assigner1", "send_email": send_email_value},
        )

        assert response.status_code == 201
        assert response.json == expected_response
        mock_create_association.assert_called_once_with(application_id="app1", user_id="user1", assigner_id="assigner1")
        if send_email_value:
            mock_notification_service.send_assessment_assigned_email.assert_called_once()
        else:
            mock_notification_service.send_assessment_assigned_email.assert_not_called()

        if notify_side_effect and send_email_value:
            assert (
                "app",
                logging.ERROR,
                "Could not send assessment assigned email, user: {user_id}, application {application_id}",
            ) in caplog.record_tuples


@pytest.mark.parametrize(
    "send_email_value, notify_side_effect", [(True, None), (False, None), (True, NotificationError("could not send"))]
)
def test_update_user_application_association(flask_test_client, send_email_value, notify_side_effect, mocker, caplog):
    mock_association = {
        "application_id": "app1",
        "user_id": "user1",
        "assigner_id": "assigner1",
        "created_at": datetime(2024, 6, 10, 15, 35, 47, 999),
        "active": False,
        "log": "{'activated': '2024-06-10T15:35:47Z', 'deactivated': '2024-06-11T15:35:47Z'}",
    }

    expected_response = deepcopy(mock_association)
    expected_response["created_at"] = expected_response["created_at"].isoformat()

    with (
        mock.patch(
            "pre_award.assessment_store.api.routes.user_routes.update_user_application_association_db",
            return_value=mock_association,
        ) as mock_update_association,
        mock.patch("pre_award.assessment_store.api.routes.user_routes.get_metadata_for_application"),
        mock.patch("pre_award.assessment_store.api.routes.user_routes.get_account_data"),
        mock.patch("pre_award.assessment_store.api.routes.user_routes.get_fund_data"),
        mock.patch("pre_award.assessment_store.api.routes.user_routes.create_assessment_url_for_application"),
    ):
        mock_notification_service = mock.MagicMock()
        mocker.patch(
            "pre_award.assessment_store.api.routes.user_routes.get_notification_service",
            return_value=mock_notification_service,
        )
        if notify_side_effect:
            mock_notification_service.send_assessment_unassigned_email.side_effect = notify_side_effect
        response = flask_test_client.put(
            "/assessment/application/app1/user/user1",
            json={
                "active": False,
                "assigner_id": "assigner1",
                "send_email": send_email_value,
            },
        )

        assert response.status_code == 200
        assert response.json == expected_response
        mock_update_association.assert_called_once_with(
            application_id="app1",
            user_id="user1",
            active=False,
            assigner_id="assigner1",
        )
        if send_email_value:
            mock_notification_service.send_assessment_unassigned_email.assert_called_once()
        else:
            mock_notification_service.send_assessment_assigned_email.assert_not_called()

        if notify_side_effect and send_email_value:
            assert (
                "app",
                logging.ERROR,
                "Could not send assessment email, active: {active}, user: {user_id}, application {application_id}",
            ) in caplog.record_tuples


def test_get_all_applications_associated_with_user(flask_test_client):
    mock_applications = [
        {
            "application_id": "app1",
            "user_id": "user1",
            "assigner_id": "assigner1",
            "created_at": datetime(2024, 6, 10, 15, 35, 47, 999),
            "active": True,
            "log": "{'activated': '2024-06-10T15:35:47Z'}",
        },
        {
            "application_id": "app2",
            "user_id": "user1",
            "assigner_id": "assigner1",
            "created_at": datetime(2024, 6, 11, 15, 35, 47, 999),
            "active": False,
            "log": "{'activated': '2024-06-10T15:35:47Z', 'deactivated': '2024-06-11T15:35:47Z'}",
        },
    ]

    expected_response = deepcopy(mock_applications)
    expected_response[0]["created_at"] = expected_response[0]["created_at"].isoformat()
    expected_response[1]["created_at"] = expected_response[1]["created_at"].isoformat()

    with mock.patch(
        "pre_award.assessment_store.api.routes.user_routes.get_user_application_associations",
        return_value=mock_applications,
    ) as mock_get_applications:
        response = flask_test_client.get("/assessment/user/user1/applications")

        assert response.status_code == 200
        assert response.json == expected_response
        mock_get_applications.assert_called_once_with(user_id="user1", active=None)


def test_get_all_applications_assigned_by_user(flask_test_client):
    mock_applications = [
        {
            "application_id": "app1",
            "user_id": "user1",
            "assigner_id": "assigner1",
            "created_at": datetime(2024, 6, 10, 15, 35, 47, 999),
            "active": True,
            "log": "{'activated': '2024-06-10T15:35:47Z'}",
        },
        {
            "application_id": "app2",
            "user_id": "user2",
            "assigner_id": "assigner1",
            "created_at": datetime(2024, 6, 11, 15, 35, 47, 999),
            "active": False,
            "log": "{'activated': '2024-06-10T15:35:47Z', 'deactivated': '2024-06-11T15:35:47Z'}",
        },
    ]

    expected_response = deepcopy(mock_applications)
    expected_response[0]["created_at"] = expected_response[0]["created_at"].isoformat()
    expected_response[1]["created_at"] = expected_response[1]["created_at"].isoformat()

    with mock.patch(
        "pre_award.assessment_store.api.routes.user_routes.get_user_application_associations",
        return_value=mock_applications,
    ) as mock_get_applications:
        response = flask_test_client.get("/assessment/user/assigner1/assignees")

        assert response.status_code == 200
        assert response.json == expected_response
        mock_get_applications.assert_called_once_with(assigner_id="assigner1", active=None)


COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
app = {"round_id": COF_ROUND_2_ID, "fund_id": COF_FUND_ID, "application_id": "app789"}
scoring_system = {"maximum_score": 5}
sub_criteria_scores = {"sub1": 3, "sub2": 4, "sub3": 5}

mapping_config = {
    f"{COF_FUND_ID}:{COF_ROUND_2_ID}": {
        "scored_criteria": [
            {
                "id": "criteria1",
                "weighting": 2,
                "sub_criteria": [{"id": "sub1"}, {"id": "sub2"}],
            },
            {"id": "criteria2", "weighting": 1, "sub_criteria": [{"id": "sub3"}]},
        ]
    }
}


@pytest.fixture
def mock_get_scoring_system(mocker):
    return mocker.patch(
        "pre_award.assessment_store.api.routes.assessment_routes.get_scoring_system_for_round_id",
        return_value=scoring_system,
    )


@pytest.fixture
def mock_get_scores(mocker):
    return mocker.patch(
        "pre_award.assessment_store.api.routes.assessment_routes.get_sub_criteria_to_latest_score_map",
        return_value=sub_criteria_scores,
    )


def test_calculate_overall_score_percentage_for_application(mocker, mock_get_scores, mock_get_scoring_system):
    mock_config = mocker.patch("pre_award.assessment_store.api.routes.assessment_routes.Config")
    mock_config.ASSESSMENT_MAPPING_CONFIG = mapping_config
    result = calculate_overall_score_percentage_for_application(
        application_id=app["application_id"], fund_id=app["fund_id"], round_id=app["round_id"]
    )
    expected_score = ((3 * 2 + 4 * 2 + 5 * 1) / (5 * 2 * 2 + 5 * 1 * 1)) * 100
    assert result == expected_score, "The calculated score did not match the expected score"


def test_calculate_running_score_percentage_for_application(mocker, mock_get_scores, mock_get_scoring_system):
    mock_config = mocker.patch("pre_award.assessment_store.api.routes.assessment_routes.Config")
    mock_config.ASSESSMENT_MAPPING_CONFIG = {
        f"{COF_FUND_ID}:{COF_ROUND_2_ID}": {
            "scored_criteria": [
                {
                    "id": "criteria1",
                    "weighting": 0.3,
                    "sub_criteria": [{"id": "sub1"}, {"id": "sub2"}],
                },
                {"id": "criteria2", "weighting": 0.6, "sub_criteria": [{"id": "sub3"}]},
                {"id": "criteria3", "weighting": 0.1, "sub_criteria": [{"id": "sub4"}]},
            ]
        }
    }
    mock_get_scores.return_value = {"sub1": 3, "sub3": 5}
    result = calculate_overall_score_percentage_for_application(
        application_id=app["application_id"], fund_id=app["fund_id"], round_id=app["round_id"]
    )
    # Note this is a fractional percentage
    expected_score = ((3 * 0.3 + 5 * 0.6) / (5 * 2 * 0.3 + 5 * 1 * 0.6 + 5 * 1 * 0.1)) * 100
    assert result == approx(expected_score), "The calculated score did not match the expected score"


def test_calculate_score_percentage_with_zero_weights(mocker, mock_get_scores, mock_get_scoring_system):
    mock_config = mocker.patch("pre_award.assessment_store.api.routes.assessment_routes.Config")
    mock_config.ASSESSMENT_MAPPING_CONFIG = {
        f"{COF_FUND_ID}:{COF_ROUND_2_ID}": {
            "scored_criteria": [
                {
                    "id": "criteria1",
                    "weighting": 0.3,
                    "sub_criteria": [{"id": "sub1"}, {"id": "sub2"}],
                },
                {"id": "criteria2", "weighting": 0.7, "sub_criteria": [{"id": "sub3"}]},
                {"id": "criteria3", "weighting": 0, "sub_criteria": [{"id": "sub4"}]},
            ]
        }
    }
    mock_get_scores.return_value = {"sub1": 3, "sub2": 0, "sub3": 5, "sub4": 5}
    result = calculate_overall_score_percentage_for_application(
        application_id=app["application_id"], fund_id=app["fund_id"], round_id=app["round_id"]
    )
    expected_score = ((3 * 0.3 + 5 * 0.7) / (5 * 2 * 0.3 + 5 * 1 * 0.7)) * 100
    assert result == approx(expected_score), "The calculated score did not match the expected score"


def test_with_no_sub_criteria_scores(mocker, mock_get_scores, mock_get_scoring_system):
    mock_config = mocker.patch("pre_award.assessment_store.api.routes.assessment_routes.Config")
    mock_config.ASSESSMENT_MAPPING_CONFIG = mapping_config
    mock_get_scores.return_value = {}
    result = calculate_overall_score_percentage_for_application(
        application_id=app["application_id"], fund_id=app["fund_id"], round_id=app["round_id"]
    )
    assert result == 0, "The result should be 0 when there are no sub-criteria scores"


def test_with_invalid_application_id(mocker, mock_get_scores, mock_get_scoring_system):
    mock_config = mocker.patch("pre_award.assessment_store.api.routes.assessment_routes.Config")
    mock_config.ASSESSMENT_MAPPING_CONFIG = mapping_config
    mock_get_scores.side_effect = KeyError("Invalid application ID")
    with pytest.raises(KeyError):
        calculate_overall_score_percentage_for_application(
            application_id=app["application_id"], fund_id=app["fund_id"], round_id=app["round_id"]
        )


def test_no_scored_criteria_exists(mocker, mock_get_scores, mock_get_scoring_system):
    mock_config = mocker.patch("pre_award.assessment_store.api.routes.assessment_routes.Config")
    mock_config.ASSESSMENT_MAPPING_CONFIG = {f"{COF_FUND_ID}:{COF_ROUND_2_ID}": {"scored_criteria": []}}
    result = calculate_overall_score_percentage_for_application(
        application_id=app["application_id"], fund_id=app["fund_id"], round_id=app["round_id"]
    )
    assert result is None, "The result should be 0 when there are no scored criteria"
