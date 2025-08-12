import json
import random

import pytest
import sqlalchemy

from pre_award.assessment_store.config.mappings.assessment_mapping_fund_round import COF_FUND_ID, applicant_info_mapping
from pre_award.assessment_store.db.models import Comment, Score
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.models.assessment_record.enums import Status
from pre_award.assessment_store.db.models.comment import CommentsUpdate
from pre_award.assessment_store.db.models.comment.enums import CommentType
from pre_award.assessment_store.db.queries import find_answer_by_key_runner
from pre_award.assessment_store.db.queries.assessment_records.queries import (
    find_assessor_task_list_state,
    get_assessment_export_data,
    get_export_data,
)
from pre_award.assessment_store.db.queries.comments.queries import (
    create_comment,
    get_comments_for_display,
    get_sub_criteria_to_has_comment_map,
    update_comment,
)
from pre_award.assessment_store.db.queries.scores.queries import create_score_for_app_sub_crit
from tests.pre_award.assessment_store_tests._helpers import get_assessment_record
from tests.pre_award.assessment_store_tests.conftest import test_input_data


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_select_field_by_id(seed_application_records):
    """test_select_field_by_id Tests that the correct field is picked from the
    corresponding application."""
    picked_row = seed_application_records[0]

    # We pick a random row to extract some data from.
    picked_app_id = picked_row["application_id"]

    picked_questions = random.choice(picked_row["jsonb_blob"]["forms"])
    picked_question = random.choice(picked_questions["questions"])
    picked_field = random.choice(picked_question["fields"])

    picked_key = picked_field["key"]

    field_found = find_answer_by_key_runner(picked_key, picked_app_id)[0]
    assert json.dumps(field_found, sort_keys=True) == json.dumps(picked_field, sort_keys=True)


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_non_blob_columns_mutable(db, seed_application_records):
    """test_non_blob_columns_mutable Tests we haven't made the whole table
    immutable by accident when making the json blob immutable."""

    try:
        picked_row = get_assessment_record(seed_application_records[0]["application_id"])
        picked_row.workflow_status = "IN_PROGRESS"
        db.session.commit()
    except sqlalchemy.exc.InternalError as e:
        raise AssertionError from e
    finally:
        db.session.rollback()


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_find_assessor_task_list_ui_metadata(seed_application_records):
    """test_find_assessor_task_list_ui_metadata Tests that the correct metadata is
    returned for the assessor task list UI."""

    metadata = find_assessor_task_list_state(seed_application_records[0]["application_id"])
    assert metadata == {
        "fund_id": seed_application_records[0]["fund_id"],
        "project_name": "Mock that is used to test Assessors Task List",
        "short_id": seed_application_records[0]["short_id"],
        "round_id": seed_application_records[0]["round_id"],
        "workflow_status": "NOT_STARTED",
        "date_submitted": "2022-10-27T08:32:13.383999",
        "funding_amount_requested": 4600.00,
        "language": "en",
        "is_deleted": False,
    }


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_post_comment(seed_application_records, comments_test_account):
    """test_post_comment tests we can create comment records in the comments
    table."""

    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": str(comments_test_account.id),
        "theme_id": "something",
    }
    comment_metadata = create_comment(**assessment_payload)

    assert len(comment_metadata) == 8
    assert comment_metadata["user_id"] == str(comments_test_account.id)
    assert comment_metadata["theme_id"] == "something"
    assert comment_metadata["comment_type"] == "COMMENT"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_post_comment_whole_application(seed_application_records, comments_test_account):
    """test_post_comment_whole_application tests we can create comment records in
    the comments table."""

    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": None,
        "comment": "Please provide more information",
        "comment_type": "WHOLE_APPLICATION",
        "user_id": str(comments_test_account.id),
        "theme_id": None,
    }
    comment_metadata = create_comment(**assessment_payload)

    assert len(comment_metadata) == 8
    assert comment_metadata["user_id"] == str(comments_test_account.id)
    assert comment_metadata["theme_id"] is None
    assert comment_metadata["sub_criteria_id"] is None
    assert comment_metadata["comment_type"] == "WHOLE_APPLICATION"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_put_comment(seed_application_records, comments_test_account):
    """test_put_comment tests we can create comment records in the comments
    table."""

    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id
    sub_criteria_id = "test-app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": str(comments_test_account.id),
        "theme_id": "something",
    }
    comment_metadata = create_comment(**assessment_payload)

    assert len(comment_metadata) == 8
    assert comment_metadata["user_id"] == str(comments_test_account.id)
    assert comment_metadata["theme_id"] == "something"

    updated_comment = "This is updated comment"
    comment_metadata = update_comment(comment_id=comment_metadata["id"], comment=updated_comment)

    assert len(comment_metadata) == 8
    assert comment_metadata["updates"][-1]["comment"] == updated_comment


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_put_comment_whole_application(seed_application_records, comments_test_account):
    """test_put_comment_whole_application tests we can create comment records in
    the comments table."""

    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": None,
        "comment": "Please provide more information",
        "comment_type": "WHOLE_APPLICATION",
        "user_id": str(comments_test_account.id),
        "theme_id": None,
    }
    comment_metadata = create_comment(**assessment_payload)

    assert len(comment_metadata) == 8
    assert comment_metadata["user_id"] == str(comments_test_account.id)
    assert comment_metadata["theme_id"] is None
    assert comment_metadata["sub_criteria_id"] is None
    assert comment_metadata["comment_type"] == "WHOLE_APPLICATION"

    updated_comment = "This is updated comment"
    comment_metadata = update_comment(comment_id=comment_metadata["id"], comment=updated_comment)

    assert len(comment_metadata) == 8
    assert comment_metadata["updates"][-1]["comment"] == updated_comment


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_comments(seed_application_records, comments_test_account):
    """test_get_comments tests we can get all comment records in the comments
    table filtered by application_id, subcriteria_id and theme_id."""

    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"
    theme_id = "theme"

    assessment_payload_1 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": str(comments_test_account.id),
        "theme_id": theme_id,
    }
    create_comment(**assessment_payload_1)

    assessment_payload_2 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": str(comments_test_account.id),
        "theme_id": theme_id,
    }
    create_comment(**assessment_payload_2)

    assessment_payload_3 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": str(comments_test_account.id),
        "theme_id": "different theme",
    }
    comment_metadata = create_comment(**assessment_payload_3)

    comment_metadata_for_theme = get_comments_for_display(application_id, sub_criteria_id, theme_id)
    assert len(comment_metadata_for_theme) == 2
    assert comment_metadata_for_theme[0]["theme_id"] == comment_metadata_for_theme[1]["theme_id"]

    comment_metadata_no_theme = get_comments_for_display(application_id, sub_criteria_id, theme_id=None)
    assert len(comment_metadata_no_theme) == 3

    # test without application_id
    comment_metadata_for_comment_id = get_comments_for_display(comment_id=comment_metadata["id"])
    assert len(comment_metadata_for_comment_id) == 1


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_comments_whole_application(seed_application_records, comments_test_account):
    """test_get_comments_whole_application tests we can get all comment records in
    the comments table filtered by application_id, subcriteria_id and theme_id."""

    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id

    assessment_payload_1 = {
        "application_id": application_id,
        "sub_criteria_id": None,
        "comment": "Please provide more information",
        "comment_type": "WHOLE_APPLICATION",
        "user_id": str(comments_test_account.id),
        "theme_id": None,
    }
    create_comment(**assessment_payload_1)

    assessment_payload_2 = {
        "application_id": application_id,
        "sub_criteria_id": None,
        "comment": "Please provide more information",
        "comment_type": "WHOLE_APPLICATION",
        "user_id": str(comments_test_account.id),
        "theme_id": None,
    }
    create_comment(**assessment_payload_2)

    assessment_payload_3 = {
        "application_id": application_id,
        "sub_criteria_id": None,
        "comment": "Please provide more information",
        "comment_type": "WHOLE_APPLICATION",
        "user_id": str(comments_test_account.id),
        "theme_id": None,
    }
    comment_metadata = create_comment(**assessment_payload_3)

    comment_metadata_for_theme = get_comments_for_display(application_id, None, None)
    assert len(comment_metadata_for_theme) == 3
    assert comment_metadata_for_theme[0]["theme_id"] == comment_metadata_for_theme[1]["theme_id"]
    assert comment_metadata_for_theme[0]["comment_type"] == comment_metadata_for_theme[1]["comment_type"]

    # test without application_id
    comment_metadata_for_comment_id = get_comments_for_display(comment_id=comment_metadata["id"])
    assert len(comment_metadata_for_comment_id) == 1


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria_to_has_comment_map(seed_application_records, comments_test_account):
    picked_row: AssessmentRecord = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"
    theme_id = "theme"

    assessment_payload_1 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": str(comments_test_account.id),
        "theme_id": theme_id,
    }
    create_comment(**assessment_payload_1)

    result = get_sub_criteria_to_has_comment_map(picked_row.application_id)
    assert result[sub_criteria_id] is True


@pytest.mark.parametrize(
    "insertion_object",
    [
        Score(
            application_id="a3ec41db-3eac-4220-90db-c92dea049c01",
            sub_criteria_id="test",
            user_id="test",
            score=5,
            justification="great",
        ),
        Comment(
            application_id="a3ec41db-3eac-4220-90db-c92dea049c01",
            sub_criteria_id="test",
            user_id="test",
            comment_type=CommentType.COMMENT,
            updates=[CommentsUpdate(comment="great")],
        ),
    ],
)
@pytest.mark.apps_to_insert(test_input_data)
def test_update_workflow_status_on_insert(db, insertion_object, seed_application_records):
    application_id = seed_application_records[0]["application_id"]
    assessment_record = (
        db.session.query(AssessmentRecord).where(AssessmentRecord.application_id == application_id).first()
    )

    assert assessment_record.workflow_status == Status.NOT_STARTED

    insertion_object.application_id = application_id
    db.session.add(insertion_object)
    db.session.commit()

    assert assessment_record.workflow_status == Status.IN_PROGRESS


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_output_tracker_data(seed_application_records, mocker):
    mocker.patch(
        "pre_award.assessment_store.db.queries.assessment_records.queries.get_account_name",
        return_value="Test user",
    )
    # TODO expand this test with more scenarios
    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 5,
        "justification": "great",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**assessment_payload)

    data = get_assessment_export_data(
        picked_row.fund_id,
        picked_row.round_id,
        "OUTPUT_TRACKER",
        {
            "OUTPUT_TRACKER": {
                "form_fields": {
                    "aHIGbK": {"en": {"title": "Charity number "}},
                    "aAeszH": {"en": {"title": "Do you need to do any further feasibility work?"}},
                    "ozgwXq": {"en": {"title": "Risks to your project (document upload)"}},
                    "KAgrBz": {"en": {"title": "Project name"}},
                }
            }
        },
    )
    # TODO add test data for cy_list

    # default score fields
    assert data["en_list"][0]["Application ID"] == picked_row.application_id
    assert data["en_list"][0]["Short ID"] == "COF-R2W2-JWBTLX"
    assert data["en_list"][0]["Score Subcriteria"] == "app-info"
    assert data["en_list"][0]["Score"] == 5
    assert data["en_list"][0]["Score Justification"] == "great"
    assert len(data["en_list"][0]["Score Date"]) == 10
    assert len(data["en_list"][0]["Score Time"]) == 8
    assert data["en_list"][0]["Scorer Name"] == "Test user"

    # custom fields
    assert data["en_list"][0]["Charity number "] == "Test"
    assert data["en_list"][0]["Do you need to do any further feasibility work?"] is False
    assert data["en_list"][0]["Project name"] == "Save the humble pub in Bangor"
    assert data["en_list"][0]["Risks to your project (document upload)"] == "sample1.doc"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_output_tracker_with_no_scores_data(seed_application_records, mocker):
    mocker.patch(
        "pre_award.assessment_store.db.queries.assessment_records.queries.get_account_name",
        return_value="Test user",
    )

    picked_row = get_assessment_record(seed_application_records[0]["application_id"])

    data = get_assessment_export_data(
        picked_row.fund_id,
        picked_row.round_id,
        "OUTPUT_TRACKER",
        {
            "OUTPUT_TRACKER": {
                "form_fields": {
                    "aHIGbK": {"en": {"title": "Charity number "}},
                    "aAeszH": {"en": {"title": "Do you need to do any further feasibility work?"}},
                    "ozgwXq": {"en": {"title": "Risks to your project (document upload)"}},
                    "KAgrBz": {"en": {"title": "Project name"}},
                }
            }
        },
    )

    assert data["en_list"][0]["Score"] == "No scores yet"

    # check the rest of the data is correct
    assert data["en_list"][0]["Application ID"] == picked_row.application_id
    assert data["en_list"][0]["Short ID"] == "COF-R2W2-JWBTLX"

    # custom fields
    assert data["en_list"][0]["Charity number "] == "Test"
    assert data["en_list"][0]["Do you need to do any further feasibility work?"] is False
    assert data["en_list"][0]["Project name"] == "Save the humble pub in Bangor"
    assert data["en_list"][0]["Risks to your project (document upload)"] == "sample1.doc"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_output_tracker_columns_remain_same_for_scored_and_unscored_reports(seed_application_records, mocker):
    mocker.patch(
        "pre_award.assessment_store.db.queries.assessment_records.queries.get_account_name",
        return_value="Test user",
    )

    picked_row = get_assessment_record(seed_application_records[0]["application_id"])

    no_scores = get_assessment_export_data(
        picked_row.fund_id,
        picked_row.round_id,
        "OUTPUT_TRACKER",
        {
            "OUTPUT_TRACKER": {
                "form_fields": {
                    "KAgrBz": {"en": {"title": "Project name"}},
                }
            }
        },
    )

    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 5,
        "justification": "great",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**assessment_payload)

    with_scores = get_assessment_export_data(
        picked_row.fund_id,
        picked_row.round_id,
        "OUTPUT_TRACKER",
        {
            "OUTPUT_TRACKER": {
                "form_fields": {
                    "KAgrBz": {"en": {"title": "Project name"}},
                }
            }
        },
    )

    no_scores_cols = list(no_scores["en_list"][0].keys())
    with_scores_cols = list(with_scores["en_list"][0].keys())[: len(no_scores_cols)]
    assert no_scores_cols == with_scores_cols


@pytest.mark.apps_to_insert([test_input_data[4]])  # taken from assessment store for cof r4w1
def test_get_cof_r4w1_export_data_en(seed_application_records):
    app_id = test_input_data[4]["id"]
    test_record = get_assessment_record(app_id)
    result = get_export_data(
        "round_id",
        "ASSESSOR_EXPORT",
        applicant_info_mapping[COF_FUND_ID],
        [test_record],
        "en",
    )
    assert len(result) == 1
    assert str(result[0]["Application ID"]) == app_id
    assert result[0]["Name of lead contact"] == "test lead person"
    assert result[0]["Type of organisation"] == "CIO"
    assert result[0]["Asset type"] == "community-centre"
    assert result[0]["Type of asset (other)"] == ""
    assert result[0]["Charity number"] == "786786"
    assert result[0]["Organisation address"] == "test, test, test, test, ss12ss"
    assert result[0]["Postcode of asset"] == "NP10 8QQ"
    assert result[0]["Capital funding request"] == "966585"
    assert result[0]["Revenue costs (optional)"] == 456


@pytest.mark.apps_to_insert([test_input_data[5]])  # taken from assessment store for cof r4w1
def test_get_cof_r4w1_export_data_cy(seed_application_records):
    app_id = test_input_data[5]["id"]
    test_record = get_assessment_record(app_id)
    result = get_export_data(
        "round_id",
        "ASSESSOR_EXPORT",
        applicant_info_mapping[COF_FUND_ID],
        [test_record],
        "cy",
    )
    assert len(result) == 1
    assert str(result[0]["Application ID"]) == app_id
    assert result[0]["Enw'r cyswllt arweiniol"] == "asdf"
    assert result[0]["Math o sefydliad"] == "Cwmni cydweithredol, fel cymdeithas budd cymunedol"
    assert result[0]["Math o ased"] == "Arall"
    assert result[0]["Math o eiddo (arall)"] == "other asset type"
    assert result[0]["Rhif elusen"] == ""
    assert result[0]["Cyfeiriad y sefydliad"] == "line 1, town, county, PL11RN"
    assert result[0]["Cod post o ased"] == "PL11RN"
    assert result[0]["Cais cyllido cyfalaf"] == "234234"
    assert result[0]["Costau refeniw (dewisol)"] == ""
