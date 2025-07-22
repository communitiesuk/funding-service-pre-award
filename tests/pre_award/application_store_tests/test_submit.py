import io
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from unittest import mock
from unittest.mock import MagicMock
from uuid import uuid4

import pandas as pd
import pytest
from click.testing import CliRunner
from flask_session import Session
from fsd_utils import Decision, NotifyConstants
from pytest_mock import MockerFixture

from pre_award.application_store._helpers.application import send_change_received_notification, send_submit_notification
from pre_award.application_store.db.exceptions.submit import SubmitError
from pre_award.application_store.db.models.application.applications import Applications
from pre_award.application_store.db.models.application.enums import Status as ApplicationStatus
from pre_award.application_store.db.queries.application.queries import (
    create_application,
    get_application,
    get_fund_id,
    submit_application,
    update_application_fields,
)
from pre_award.application_store.db.queries.comments.queries import export_comments_to_excel, retrieve_all_comments
from pre_award.application_store.db.queries.form.queries import add_new_forms
from pre_award.application_store.db.queries.updating.queries import update_form
from pre_award.application_store.external_services import get_fund
from pre_award.application_store.external_services.exceptions import NotificationError
from pre_award.assessment_store.config.mappings.assessment_mapping_fund_round import COF_ROUND_4_W2_ID
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.models.assessment_record.enums import Status
from pre_award.assessment_store.db.models.assessment_record.enums import Status as WorkflowStatus
from pre_award.assessment_store.db.models.comment.enums import CommentType
from pre_award.assessment_store.db.models.flags.assessment_flag import AssessmentFlag
from pre_award.assessment_store.db.models.flags.flag_update import FlagStatus, FlagUpdate
from pre_award.assessment_store.db.queries.assessment_records._helpers import derive_application_values
from pre_award.assessment_store.scripts.derive_assessment_values import derive_assessment_values
from pre_award.config import Config
from services.notify import NotificationService
from tests.pre_award.application_store_tests.conftest import create_comment_with_updates
from tests.pre_award.assessment_store_tests.test_assessment_mapping_fund_round import COF_FUND_ID
from tests.pre_award.utils import AnyStringMatching


@pytest.fixture
def mock_get_files(mocker):
    mocker.patch("pre_award.application_store.db.queries.application.queries.list_files_by_prefix", new=lambda _: [])


@pytest.fixture
def mock_successful_location_call(mocker):
    mocker.patch(
        "pre_award.assessment_store.db.queries.assessment_records._helpers.get_location_json_from_postcode",
        return_value={
            "error": False,
            "postcode": "GU1 1LY",
            "county": "Hampshire",
            "region": "England",
            "country": "England",
            "constituency": "Guildford",
        },
    )


@pytest.fixture(scope="function")
def mock_data_key_mappings(monkeypatch):
    fund_round_data_key_mappings = {
        "TESTTEST": {
            "location": None,
            "asset_type": None,
            "funding_one": None,
            "funding_two": None,
        }
    }
    monkeypatch.setattr(
        "pre_award.assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )
    yield


@pytest.fixture
def existing_json_blob():
    return {
        "forms": [
            {
                "questions": [
                    {
                        "fields": [
                            {"key": "field1", "answer": "value1"},
                            {"key": "field2", "answer": "value2"},
                        ]
                    }
                ]
            }
        ]
    }


@pytest.fixture
def new_json_blob():
    return {
        "forms": [
            {
                "questions": [
                    {
                        "fields": [
                            {"key": "field1", "answer": "value1"},
                            {"key": "field2", "answer": "value2"},
                        ]
                    }
                ]
            }
        ]
    }


@pytest.fixture
def setup_completed_application(db, app, mocker, mock_get_files):
    with open("tests/pre_award/application_store_tests/seed_data/COF_R4W2_all_forms.json", "r") as f:
        cof_application = json.load(f)
        forms = cof_application["forms"]
    empty_forms = [form["name"] for form in forms]
    target_application = create_application(
        account_id=uuid4(), fund_id=COF_FUND_ID, round_id=COF_ROUND_4_W2_ID, language="en"
    )
    target_application.project_name = "test"
    target_application.date_submitted = datetime.fromisoformat(cof_application["date_submitted"])
    db.session.add(target_application)
    db.session.commit()

    application_id = target_application.id
    add_new_forms(forms=empty_forms, application_id=application_id)

    for form in forms:
        update_form(
            application_id,
            form["name"],
            form["questions"],
            True,
        )
    yield application_id


def test_submit_application_with_location_bad_key(
    db,
    monkeypatch,
    setup_completed_application,
    mock_successful_location_call,
):
    fund_round_data_key_mappings = {
        "TESTTEST": {
            "location": "badkey",
            "asset_type": None,
            "funding_one": None,
            "funding_two": None,
        }
    }
    monkeypatch.setattr(
        "pre_award.assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )
    application_id = setup_completed_application

    submit_application(application_id)
    assessment_record: AssessmentRecord = (
        db.session.query(AssessmentRecord).where(AssessmentRecord.application_id == application_id).one()
    )
    assert assessment_record
    assert assessment_record.location_json_blob
    assert assessment_record.location_json_blob["error"] is True


def test_submit_application_with_location(db, setup_completed_application, monkeypatch, mock_successful_location_call):
    fund_round_data_key_mappings = {
        "TESTTEST": {
            "location": "EfdliG",
            "asset_type": None,
            "funding_one": None,
            "funding_two": None,
        }
    }
    monkeypatch.setattr(
        "pre_award.assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )

    application_id = setup_completed_application

    submit_application(application_id)
    assessment_record: AssessmentRecord = (
        db.session.query(AssessmentRecord).where(AssessmentRecord.application_id == application_id).one()
    )
    assert assessment_record
    assert assessment_record.location_json_blob
    assert assessment_record.location_json_blob["error"] is False
    assert assessment_record.location_json_blob["county"] == "Hampshire"


def test_submit_route_success(
    flask_test_client,
    mock_successful_submit_notification,
    db,
    seed_application_records,
    mocker,
    mock_get_fund_data,
    mock_get_round,
    mock_data_key_mappings,
    mock_successful_location_call,
    mock_get_files,
):
    target_application = seed_application_records[0]
    application_id = target_application.id
    target_application.project_name = "unit test project"

    db.session.add(target_application)
    db.session.commit()

    response = flask_test_client.post(
        f"/application/applications/{application_id}/submit",
        follow_redirects=True,
    )

    assert response.status_code == 201
    assert all(k in response.json for k in ("id", "email", "reference", "eoi_decision"))

    db.session.expunge(target_application)
    application_after_submit = db.session.query(Applications).where(Applications.id == application_id).one()

    assert application_after_submit.status == ApplicationStatus.SUBMITTED

    assessment_record: AssessmentRecord = (
        db.session.query(AssessmentRecord).where(AssessmentRecord.application_id == application_id).one()
    )
    assert assessment_record
    assert assessment_record.jsonb_blob["forms"]

    try:
        datetime.strptime(assessment_record.jsonb_blob["date_submitted"], "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError as e:
        pytest.fail(f"Unexpected serialised application date format {e}")


def test_submit_route_submit_error(flask_test_client, seed_application_records, mocker, mock_successful_location_call):
    target_application = seed_application_records[0]
    application_id = target_application.id
    mocker.patch(
        "pre_award.application_store.api.routes.application.routes.submit_application",
        side_effect=SubmitError(application_id=application_id),
    )

    response = flask_test_client.post(
        f"/application/applications/{application_id}/submit",
        follow_redirects=True,
    )
    assert response.status_code == 500
    assert response.json["message"] == f"Unable to submit application {application_id}"


def test_submit_application_raises_error_on_db_violation(
    seed_application_records, mocker, db, mock_data_key_mappings, mock_successful_location_call, mock_get_files
):
    target_application = seed_application_records[0]
    target_application.project_name = None  # will cause not null constraint violation

    db.session.add(target_application)
    db.session.commit()
    application_id = target_application.id
    with pytest.raises(SubmitError) as se:
        submit_application(application_id)
    assert type(se.value) is SubmitError
    assert str(se.value).startswith(f"Unable to submit application [{application_id}]")


def test_submit_application_route_succeeds_on_notify_error(
    seed_application_records,
    mocker,
    db,
    flask_test_client,
    mock_data_key_mappings,
    mock_get_files,
    mock_successful_location_call,
):
    target_application = seed_application_records[0]
    application_id = target_application.id
    target_application.project_name = "unit test project"

    db.session.add(target_application)
    db.session.commit()

    mocker.patch(
        "pre_award.application_store.api.routes.application.routes.send_submit_notification",
        side_effect=NotificationError(),
    )

    response = flask_test_client.post(
        f"/application/applications/{application_id}/submit",
        follow_redirects=True,
    )
    assert response.status_code == 201


@pytest.mark.parametrize("eoi_result", [({"decision": "BAD_VALUE"}), ({"decision": Decision.FAIL})])
def test_send_submit_notification_do_not_send(mocker, app, mock_get_files, eoi_result, mock_notification_service_calls):
    mocker.patch("pre_award.application_store._helpers.application.create_qa_base64file", return_value={"forms": []})
    send_submit_notification(
        application={},
        eoi_results=eoi_result,
        account=MagicMock(),
        application_with_form_json={},
        application_with_form_json_and_fund_name={},
        round_data=MagicMock(),
    )
    assert len(mock_notification_service_calls) == 0


@pytest.mark.parametrize(
    "eoi_result, exp_template, exp_personalisation",
    [
        (
            None,
            "00000000-0000-0000-0000-000000000001",
            {
                "name of fund": "Community Ownership Fund",
                "application reference": AnyStringMatching(r"TEST-TEST-[A-Z]{6}"),
                "date submitted": "13 December 2024 at 01:58pm",
                "round name": "round title",
                "question": mock.ANY,
                "URL of prospectus": "https://prospectus",
                "contact email": "contact@test.com",
            },
        ),
        (
            {"decision": Decision.PASS},
            "00000000-0000-0000-0000-000000000002",
            {
                "name of fund": "Community Ownership Fund",
                "application reference": AnyStringMatching(r"TEST-TEST-[A-Z]{6}"),
                "date submitted": "13 December 2024 at 01:58pm",
                "round name": "round title",
                "question": mock.ANY,
                "full name": "Test User",
            },
        ),
        (
            {"decision": Decision.PASS_WITH_CAVEATS, "caveats": ["a", "b", "c"]},
            "00000000-0000-0000-0000-000000000003",
            {
                "name of fund": "Community Ownership Fund",
                "application reference": AnyStringMatching(r"TEST-TEST-[A-Z]{6}"),
                "date submitted": "13 December 2024 at 01:58pm",
                "round name": "round title",
                "question": mock.ANY,
                "caveats": ["a", "b", "c"],
                "full name": "Test User",
            },
        ),
    ],
)
def test_send_submit_notification(
    mocker,
    db,
    app,
    setup_completed_application,
    mock_get_files,
    eoi_result,
    exp_template,
    exp_personalisation,
    mock_notification_service_calls,
):
    # mocker.patch("pre_award.application_store._helpers.application.create_qa_base64file", return_value={"forms": []})
    mock_account = MagicMock(email="test@test.com", full_name="Test User")
    mock_round = MagicMock(contact_email="contact@test.com")
    mocker.patch(
        "services.notify.NotificationService.APPLICATION_SUBMISSION_TEMPLATE_ID_EN",
        "00000000-0000-0000-0000-000000000001",
    )
    mocker.patch.dict(
        "services.notify.NotificationService.EXPRESSION_OF_INTEREST_TEMPLATE_ID",
        {
            "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4": {
                NotifyConstants.TEMPLATE_TYPE_EOI_PASS: {
                    "fund_name": "COF",
                    "template_id": {
                        "en": "00000000-0000-0000-0000-000000000002",
                        "cy": "",
                    },
                },
                NotifyConstants.TEMPLATE_TYPE_EOI_PASS_W_CAVEATS: {
                    "fund_name": "COF",
                    "template_id": {
                        "en": "00000000-0000-0000-0000-000000000003",
                        "cy": "",
                    },
                },
            }
        },
    )

    application = db.session.get(Applications, setup_completed_application)
    application_with_form_json = get_application(setup_completed_application, as_json=True, include_forms=True)

    if eoi_result:
        application_with_form_json |= {**eoi_result}

    fund_id = get_fund_id(setup_completed_application)
    fund_data = get_fund(fund_id)
    language = application_with_form_json["language"]
    application_with_form_json_and_fund_name = {
        **application_with_form_json,
        "fund_name": fund_data.name_json[language],
        "round_name": "round title",
        "prospectus_url": "https://prospectus",
    }

    send_submit_notification(
        application=application,
        eoi_results=eoi_result,
        account=mock_account,
        application_with_form_json=application_with_form_json,
        application_with_form_json_and_fund_name=application_with_form_json_and_fund_name,
        round_data=mock_round,
    )
    assert len(mock_notification_service_calls) == 1
    assert mock_notification_service_calls == [
        mocker.call(
            "test@test.com",
            exp_template,
            personalisation=exp_personalisation,
            govuk_notify_reference=None,
            email_reply_to_id=None,
        )
    ]


@pytest.fixture
def setup_submitted_application(db, setup_completed_application, monkeypatch, mock_successful_location_call):
    fund_round_data_key_mappings = {
        "TESTTEST": {
            "location": None,
            "asset_type": None,
            "funding_one": None,
            "funding_two": None,
        }
    }
    monkeypatch.setattr(
        "pre_award.assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )

    application_id = setup_completed_application

    submit_application(application_id)
    yield application_id


def test_derive_values_script(
    setup_submitted_application, db, monkeypatch, mock_data_key_mappings, mock_successful_location_call
):
    application_id = str(setup_submitted_application)
    assessment_record: AssessmentRecord = db.session.get(AssessmentRecord, application_id)
    assert assessment_record.asset_type == "No asset type specified."
    assert assessment_record.funding_amount_requested == 0
    assert assessment_record.location_json_blob == {
        "error": False,
        "postcode": "Not Available",
        "county": "Not Available",
        "region": "Not Available",
        "country": "Not Available",
        "constituency": "Not Available",
    }

    runner = CliRunner()

    # setup data mappings so running the script will change values
    fund_round_data_key_mappings = {
        "TESTTEST": {
            "location": "EfdliG",
            "asset_type": "oXGwlA",
            "funding_one": "ABROnB",
            "funding_two": ["tSKhQQ", "UyaAHw"],
            "funding_field_type": "multiInputField",
        }
    }
    monkeypatch.setattr(
        "pre_award.assessment_store.db.queries.assessment_records._helpers.fund_round_data_key_mappings",
        fund_round_data_key_mappings,
    )

    # call script and say not confirmation prompt (no commit)
    result = runner.invoke(derive_assessment_values, ["-a", application_id], input="n")
    assert result.exit_code == 0
    assessment_record_2: AssessmentRecord = db.session.get(AssessmentRecord, application_id)
    assert assessment_record_2.asset_type == "No asset type specified."
    assert assessment_record_2.funding_amount_requested == 0
    assert assessment_record_2.location_json_blob == {
        "error": False,
        "postcode": "Not Available",
        "county": "Not Available",
        "region": "Not Available",
        "country": "Not Available",
        "constituency": "Not Available",
    }

    # Call script again but yes to prompt (commit == True)
    result = runner.invoke(derive_assessment_values, ["-a", application_id], input="y")
    assert result.exit_code == 0
    assessment_record_2: AssessmentRecord = db.session.get(AssessmentRecord, application_id)
    assert assessment_record_2.asset_type == "cinema"
    assert assessment_record_2.funding_amount_requested == 1524
    assert assessment_record_2.location_json_blob["error"] is False
    assert assessment_record_2.location_json_blob["county"] == "Hampshire"


@pytest.mark.fund_config(
    {
        "name": "Generated test fund",
        "identifier": "1",
        "short_name": "TEST",
        "description": "Testing fund",
        "welsh_available": False,
        "name_json": {"en": "English title", "cy": "Welsh title"},
        "funding_type": "UNCOMPETED",
        "rounds": [],
    }
)
def test_fields_resubmitted_uncompeted_application(setup_submitted_application, mocker, db):
    application_id = str(setup_submitted_application)
    application = get_application(application_id, include_forms=True)
    resubmitted_assessment = db.session.get(AssessmentRecord, application_id)
    resubmitted_assessment.workflow_status = Status.CHANGE_REQUESTED

    # Modify answer to a question
    test_field = application.forms[0].json[0]["fields"][0]
    original_answer = test_field["answer"]
    test_field["answer"] = "some test answer"

    # Modify project name (to test derived values)
    application.project_name = "A test project for resubmission"

    db.session.add(application)
    db.session.commit()

    submit_application(application_id)
    resubmitted_assessment = db.session.get(AssessmentRecord, application_id)

    for form in resubmitted_assessment.jsonb_blob["forms"]:
        for section in form["questions"]:
            for field in section["fields"]:
                if field["key"] == test_field["key"]:
                    assert field["answer"] == test_field["answer"]
                    try:
                        datetime.fromisoformat(list(field["history_log"][0].keys())[0])
                    except ValueError:
                        raise AssertionError("History log key is not an isoformat datetime") from None
                    assert list(field["history_log"][0].values())[0] == original_answer

    assert resubmitted_assessment.project_name == application.project_name
    assert resubmitted_assessment.workflow_status == Status.CHANGE_RECEIVED


@pytest.mark.fund_config(
    {
        "name": "Generated test fund",
        "identifier": "1",
        "short_name": "TEST",
        "description": "Testing fund",
        "welsh_available": False,
        "name_json": {"en": "English title", "cy": "Welsh title"},
        "funding_type": "UNCOMPETED",
        "rounds": [],
    }
)
def test_flags_resubmitted_uncompeted_application(setup_submitted_application, db):
    application_id = str(setup_submitted_application)
    application = get_application(application_id, include_forms=True)

    # Modify answer to a question
    test_field = application.forms[0].json[0]["fields"][0]
    test_field["answer"] = "some test answer"

    # Modify project name (to test derived values)
    application.project_name = "A test project for resubmission"

    # Another test field that isn't modified
    test_field_2 = application.forms[1].json[0]["fields"][0]

    assessor_user_id = uuid4()
    # Flag associated with changed field (should be the only one that is resolved)
    flag_update_1 = FlagUpdate(
        justification="A flag to request changes",
        user_id=assessor_user_id,
        status=FlagStatus.RAISED,
        allocation=[],
    )
    assessment_flag_1 = AssessmentFlag(
        application_id=application_id,
        sections_to_flag=[],
        latest_allocation=[],
        latest_status=FlagStatus.RAISED,
        updates=[flag_update_1],
        field_ids=[test_field["key"]],
        is_change_request=True,
    )

    # Flag associated with a field that is unchanged
    flag_update_2 = FlagUpdate(
        justification="A flag to request changes but shouldn't get resolved",
        user_id=assessor_user_id,
        status=FlagStatus.RAISED,
        allocation=[],
    )
    assessment_flag_2 = AssessmentFlag(
        application_id=application_id,
        sections_to_flag=[],
        latest_allocation=[],
        latest_status=FlagStatus.RAISED,
        updates=[flag_update_2],
        field_ids=[test_field_2["key"]],
        is_change_request=True,
    )

    # Flag that isn't a change request
    flag_update_3 = FlagUpdate(
        justification="A flag that isn't a change request",
        user_id=assessor_user_id,
        status=FlagStatus.RAISED,
        allocation=[],
    )
    assessment_flag_3 = AssessmentFlag(
        application_id=application_id,
        sections_to_flag=[],
        latest_allocation=[],
        latest_status=FlagStatus.RAISED,
        updates=[flag_update_3],
        field_ids=[test_field["key"]],
        is_change_request=False,
    )

    db.session.add(assessment_flag_1)
    db.session.add(assessment_flag_2)
    db.session.add(assessment_flag_3)
    db.session.add(application)
    db.session.commit()

    submit_application(application_id)
    resubmitted_assessment = db.session.get(AssessmentRecord, application_id)

    assert resubmitted_assessment.project_name == application.project_name

    updated_assessment_flags = (
        db.session.query(AssessmentFlag)
        .filter(AssessmentFlag.application_id == application_id, AssessmentFlag.latest_status == FlagStatus.RESOLVED)
        .all()
    )
    updated_flag_updates = (
        db.session.query(FlagUpdate)
        .join(AssessmentFlag)
        .filter(AssessmentFlag.application_id == application_id, FlagUpdate.status == FlagStatus.RESOLVED)
        .all()
    )

    assert len(updated_assessment_flags) == 2, "All flags should have been resolved"
    assert len(updated_flag_updates) == 2, "All flags update should have a resolved status"

    assert updated_assessment_flags[0].id == assessment_flag_1.id
    assert updated_flag_updates[0].user_id == application.account_id
    assert updated_flag_updates[0].assessment_flag_id == updated_assessment_flags[0].id


COMPETED_CONFIG = {
    "name": "Generated test fund",
    "identifier": "1",
    "short_name": "TEST",
    "description": "Testing fund",
    "welsh_available": False,
    "name_json": {"en": "English title", "cy": "Welsh title"},
    "funding_type": "COMPETED",
    "rounds": [],
}

DPIF_CONFIG = {
    "name": "Generated test fund",
    "identifier": "1",
    "short_name": "DPIF",
    "description": "Testing fund",
    "welsh_available": False,
    "name_json": {"en": "English title", "cy": "Welsh title"},
    "funding_type": "UNCOMPETED",
    "rounds": [],
}


@pytest.mark.parametrize(
    "fund_configs",
    [
        pytest.param(None, marks=pytest.mark.fund_config(COMPETED_CONFIG), id="COMPETED"),
        pytest.param(None, marks=pytest.mark.fund_config(DPIF_CONFIG), id="DPIF"),
    ],
)
def test_resubmitted_application_from_competed_fund(fund_configs, setup_submitted_application, db):
    application_id = str(setup_submitted_application)
    application = get_application(application_id, include_forms=True)

    # Modify answer to a question
    test_field = application.forms[0].json[0]["fields"][0]
    original_answer = test_field["answer"]
    test_field["answer"] = "some test answer"

    # Modify project name (to test derived values)
    original_project_name = application.project_name
    application.project_name = "A test project for resubmission"

    db.session.add(application)
    db.session.commit()

    submit_application(application_id)
    resubmitted_assessment = db.session.get(AssessmentRecord, application_id)

    for form in resubmitted_assessment.jsonb_blob["forms"]:
        for section in form["questions"]:
            for field in section["fields"]:
                if field["key"] == test_field["key"]:
                    assert field["answer"] == original_answer
                    assert "history_log" not in field

    assert resubmitted_assessment.project_name == original_project_name


@pytest.mark.parametrize("mock_now", ["2024-01-01T12:00:00+00:00"])
def test_no_changes(existing_json_blob, new_json_blob, mock_now):
    with mock.patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.side_effect = lambda tz=None: mock_datetime.now.return_value
        changed_fields = update_application_fields(existing_json_blob, new_json_blob, [])

    # Should return empty set with no changed fields
    assert changed_fields == set()

    # There should be no history logs
    for form in new_json_blob["forms"]:
        for section in form["questions"]:
            for field in section["fields"]:
                assert "history_log" not in field
                assert "requested_change" not in field
                assert "unrequested_change" not in field


@pytest.mark.parametrize("mock_now", ["2024-01-01T12:00:00+00:00"])
def test_multiple_fields_changed(existing_json_blob, new_json_blob, mock_now):
    new_json_blob["forms"][0]["questions"][0]["fields"][0]["answer"] = "changed_value1"
    new_json_blob["forms"][0]["questions"][0]["fields"][1]["answer"] = "changed_value2"
    with mock.patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.side_effect = lambda tz=None: mock_datetime.now.return_value
        changed_fields = update_application_fields(existing_json_blob, new_json_blob, ["field1"])

    assert changed_fields == {"field1", "field2"}

    f1 = new_json_blob["forms"][0]["questions"][0]["fields"][0]
    f2 = new_json_blob["forms"][0]["questions"][0]["fields"][1]
    assert "history_log" in f1
    assert "requested_change" in f1
    assert "history_log" in f2
    assert "unrequested_change" in f2

    assert len(f1["history_log"]) == 1
    assert len(f2["history_log"]) == 1


@pytest.mark.parametrize("mock_now", ["2024-01-01T12:00:00+00:00"])
def test_existing_history_log_is_appended(existing_json_blob, new_json_blob, mock_now):
    # Set up existing history log for field
    existing_json_blob["forms"][0]["questions"][0]["fields"][1]["history_log"] = [
        {"2023-12-31T23:59:59+00:00": "previous_value"}
    ]
    new_json_blob["forms"][0]["questions"][0]["fields"][1]["answer"] = "another_new_value"

    with mock.patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.side_effect = lambda tz=None: mock_datetime.now.return_value
        changed_fields = update_application_fields(existing_json_blob, new_json_blob, [])

    assert changed_fields == {"field2"}

    # History log should contain both previous changes
    f2 = new_json_blob["forms"][0]["questions"][0]["fields"][1]
    assert len(f2["history_log"]) == 2

    old_val = existing_json_blob["forms"][0]["questions"][0]["fields"][1]["answer"]
    assert list(f2["history_log"][-1].values())[0] == old_val


@pytest.mark.fund_config(
    {
        "name": "Generated test fund",
        "identifier": "1",
        "short_name": "TEST",
        "description": "Testing fund",
        "welsh_available": False,
        "name_json": {"en": "English title", "cy": "Welsh title"},
        "funding_type": "UNCOMPETED",
        "rounds": [],
    }
)
def test_assessment_records_workflow_status(
    mocker: MockerFixture, setup_submitted_application: Applications, db: Session
) -> None:
    application_id = str(setup_submitted_application)
    application = get_application(application_id, include_forms=True)
    assessment_record = db.session.get(AssessmentRecord, application_id)
    mocker.patch(
        "pre_award.application_store.db.queries.application.queries.db.session.scalar", return_value=assessment_record
    )

    submit_application(application_id)
    assert application.status.name == "SUBMITTED"  # type: ignore
    assert assessment_record.workflow_status.name == "NOT_STARTED"

    # Resubmit an already submitted application (e.g. by refreshing "Application Submitted" success page)
    submit_application(application_id)
    assert application.status.name == "SUBMITTED"  # type: ignore
    assessment_record = db.session.get(AssessmentRecord, application_id)
    # workflow_status shouldn't change on resubmission
    assert assessment_record.workflow_status.name == "NOT_STARTED"

    # Simulate a change request to the application
    application.status = ApplicationStatus.CHANGE_REQUESTED  # type: ignore
    assessment_record.workflow_status = WorkflowStatus.CHANGE_REQUESTED
    db.session.commit()

    # Simulate reviewing and completing the section
    application.status = ApplicationStatus.COMPLETED  # type: ignore
    db.session.commit()

    # Resubmit application after changes have been made
    submit_application(application_id)
    application = db.session.get(Applications, application_id)
    assert application.status.name == "SUBMITTED"  # type: ignore
    assessment_record = db.session.get(AssessmentRecord, application_id)
    assert assessment_record.workflow_status.name == "CHANGE_RECEIVED"


@pytest.mark.parametrize(
    "exp_template, exp_personalisation",
    [
        (
            "00000000-0000-0000-0000-000000000004",
            {
                "name of fund": "Community Ownership Fund",
                "round name": "test",
                "sign in link": Config.ASSESS_HOST + "/assess/fund_dashboard/COF/test/",
                "contact email": "contact@test.com",
            },
        )
    ],
)
def test_send_change_received_notification(
    mocker,
    db,
    app,
    setup_completed_application,
    mock_get_files,
    exp_template,
    exp_personalisation,
    mock_notification_service_calls,
):
    mock_round = MagicMock(title="test", contact_email="contact@test.com", short_name="test")
    mocker.patch(
        "services.notify.NotificationService.CHANGE_RECEIVED_TEMPLATE_ID",
        "00000000-0000-0000-0000-000000000004",
    )

    fund_id = get_fund_id(setup_completed_application)
    fund_data = get_fund(fund_id)

    send_change_received_notification(
        fund=fund_data,
        round_data=mock_round,
    )
    assert len(mock_notification_service_calls) == 1
    assert mock_notification_service_calls == [
        mocker.call(
            mock_round.contact_email,
            exp_template,
            personalisation=exp_personalisation,
            govuk_notify_reference=None,
            email_reply_to_id=NotificationService.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(
                NotificationService.FUNDING_SERVICE_SUPPORT_EMAIL_ADDRESS
            ),
        )
    ]


def test_derive_application_values_pfn(pfn_application_json_extract, app):
    """Test the derive_application_values function with a PFN application JSON extract.
    Specifically, check that the funding amount requested is calculated correctly"""
    app.logger.disabled = True

    result = derive_application_values(pfn_application_json_extract)
    assert result["application_id"] == "1234567-abcd-ab12-cd34-123456asdfgh"
    assert result["short_id"].startswith("PFN-RP")

    # funding_one: sum of ["JoEKPs", "MaHzlK", "cSAvLl", "lXHVDo"] fields' values in pfn_application_json
    # funding_two: sum of ["YQGJbm", "VmCcNW", "pCCkfZ", "aaOhAH"] fields' values in pfn_application_json
    # funding_amount_requested: sum of funding_one and funding_two
    assert result["funding_amount_requested"] == 12000 + 18000
    assert result["language"] == "en"
    assert result["project_name"] == "Test Council"


def test_export_comments_to_excel(
    db,
    setup_submitted_application,
    app,
    mock_comments_sub_criteria,
    comments_test_account,
    comments_base_time,
    comments_data,
):
    application_id = setup_submitted_application
    user_id = comments_test_account.id

    # Create comments with updates for the test application
    for idx, cdata in enumerate(comments_data):
        create_comment_with_updates(
            db=db,
            application_id=application_id,
            user_id=user_id,
            sub_criteria_id=cdata["sub_criteria_id"],
            comment_type=cdata["comment_type"],
            update_texts=cdata["updates"],
            comments_base_time=comments_base_time + timedelta(hours=idx),
            account=comments_test_account,
        )

    # Create a different application to later check for filtering
    other_app = Applications(
        id="00000000-0000-0000-0000-000000000000",
        account_id="other-user",
        fund_id=str(uuid4()),
        round_id=str(uuid4()),
        key="other-key",
        language="en",
        reference="OTHER-REF",
        project_name="Other Project",
    )
    db.session.add(other_app)
    db.session.commit()

    # Create an assessment record for the other application
    assessment_record = AssessmentRecord(
        application_id=other_app.id,
        short_id="OTHER-SHORT-ID",
        type_of_application="Test",
        project_name="Other Project",
        funding_amount_requested=0,
        round_id=other_app.round_id,
        fund_id=other_app.fund_id,
        language="en",
        workflow_status="NOT_STARTED",
        asset_type="Test",
        jsonb_blob={},
    )
    db.session.add(assessment_record)
    db.session.commit()

    # Create a comment for the other application
    create_comment_with_updates(
        db=db,
        application_id=other_app.id,
        user_id="other-user",
        sub_criteria_id=None,
        comment_type=CommentType.WHOLE_APPLICATION,
        update_texts=["Other app comment"],
        comments_base_time=comments_base_time,
        account=comments_test_account,
    )
    # Retrieve the test application
    application = db.session.get(Applications, application_id)

    # Retrieve comments for the test application
    comments_list = retrieve_all_comments(
        fund_id=application.fund_id,
        round_id=application.round_id,
        application_id=application.id,
    )

    # Export to Excel (in-memory)
    fund_short_name = "TEST"
    round_short_name = "ROUND"
    with app.test_request_context():
        response = export_comments_to_excel(
            comments_list, fund_short_name, round_short_name, application_id=application_id
        )
        response.direct_passthrough = False
        output = response.get_data()

    # Read the Excel file
    output_io = io.BytesIO(output)
    df = pd.read_excel(output_io)

    # Check that all comments for the test application are present
    expected_comments = []
    for cdata in comments_data:
        expected_comments.extend(cdata["updates"])
    assert Counter(df["Comment"]) == Counter(expected_comments)

    # Check that no comments from the other applications are present
    assert "Other app comment" not in df["Comment"].values

    # Check ordering: Application-level comments (sub_criteria_id=None) first,
    # then by sub_criteria_id, then by date_created
    sub_criteria_col = df["Sub-criteria name"].fillna("None").values
    app_level_end = 0
    for val in sub_criteria_col:
        if val == "None":
            app_level_end += 1
        else:
            break

    # All application-level comments should be at the top
    assert all(val == "None" for val in sub_criteria_col[:app_level_end])
    # The rest should be grouped by sub_criteria_id (SC1, then SC2)
    sc1_start = app_level_end
    sc1_end = sc1_start + sum(1 for c in comments_data if c["sub_criteria_id"] == "SC1" for _ in c["updates"])
    assert all(val == "Sub Criteria 1" for val in sub_criteria_col[sc1_start:sc1_end])
    assert all(val == "Sub Criteria 2" for val in sub_criteria_col[sc1_end:])
