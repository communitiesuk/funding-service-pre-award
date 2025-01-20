import datetime
import uuid
from unittest.mock import MagicMock

import pytest

from assessment_store.api.routes.progress_routes import get_progress_for_applications
from assessment_store.api.routes.score_routes import get_scoring_system_name_for_round_id
from assessment_store.db.models import AssessmentFlag, AssessmentRecord, Score
from assessment_store.db.models.flags import FlagStatus
from assessment_store.db.queries.assessment_records.queries import check_all_change_requests_accepted
from assessment_store.db.queries.scores.queries import (
    create_score_for_app_sub_crit,
    get_scores_for_app_sub_crit,
    get_sub_criteria_to_latest_score_map,
)
from tests.assessment_store_tests._helpers import get_assessment_record
from tests.assessment_store_tests.conftest import test_input_data


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_create_scores_for_application_sub_crit(_db, seed_application_records):
    """test_create_scores_for_application_sub_crit Tests we can create score
    records in the scores table in the appropriate format."""

    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    score_metadata = create_score_for_app_sub_crit(**assessment_payload)

    assert len(score_metadata) == 7
    assert score_metadata["date_created"]
    assert score_metadata["score"] == 3


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_latest_score_for_application_sub_crit(seed_application_records):
    """test_get_latest_score_for_application_sub_crit Tests we can add score
    records in the scores table and return the most recently created."""

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
    create_score_metadata = create_score_for_app_sub_crit(**assessment_payload)

    score_metadata = get_scores_for_app_sub_crit(application_id, sub_criteria_id)
    latest_score_metadata = score_metadata[0]

    assert latest_score_metadata["date_created"] == create_score_metadata.get("date_created")
    assert latest_score_metadata["score"] == create_score_metadata.get("score")
    assert latest_score_metadata["justification"] == create_score_metadata.get("justification")


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_score_history(seed_application_records):
    """test_get_score_history Tests we can get all score records in the scores
    table."""

    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload_1 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_metadata_1 = create_score_for_app_sub_crit(**assessment_payload_1)

    assessment_payload_2 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 5,
        "justification": "great",
        "user_id": "test",
    }
    create_score_metadata_2 = create_score_for_app_sub_crit(**assessment_payload_2)

    score_metadata = get_scores_for_app_sub_crit(application_id, sub_criteria_id, True)

    assert len(score_metadata) == 2
    assert score_metadata[0]["score"] == create_score_metadata_2["score"]
    assert score_metadata[1]["justification"] == create_score_metadata_1["justification"]


@pytest.mark.apps_to_insert(test_input_data)
def test_get_progress_for_applications(seed_application_records):
    """test_create_scores_for_application_sub_crit Tests we can create score
    records in the scores table in the appropriate format."""

    application_id_1 = seed_application_records[0]["application_id"]
    application_id_2 = seed_application_records[1]["application_id"]
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]
    sub_criteria_ids = ["benefits", "engagement"]

    score_payload_1 = {
        "application_id": application_id_1,
        "sub_criteria_id": sub_criteria_ids[0],
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**score_payload_1)

    score_payload_2 = {
        "application_id": application_id_1,
        "sub_criteria_id": sub_criteria_ids[1],
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**score_payload_2)

    score_payload_3 = {
        "application_id": application_id_2,
        "sub_criteria_id": sub_criteria_ids[1],
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**score_payload_3)

    request = MagicMock()
    request.get_json.return_value = {
        "application_ids": [
            application_id_1,
            application_id_2,
        ]
    }
    application_progress_list = get_progress_for_applications(
        fund_id, round_id, application_ids=[application_id_1, application_id_2]
    )

    assert len(application_progress_list) == 2
    for application in application_progress_list:
        if application["application_id"] == application_id_1:
            assert application["progress"] == 20
        if application["application_id"] == application_id_2:
            assert application["progress"] == 10


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria_to_latest_score_map(_db, seed_application_records):
    application_id = seed_application_records[0]["application_id"]
    sub_criteria_1_id = str(uuid.uuid4())
    sub_criteria_2_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    now = datetime.datetime.now()
    earlier = now - datetime.timedelta(days=1)
    latest = now + datetime.timedelta(days=1)

    scores = [
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_1_id,
            score=2,
            justification="test",
            date_created=earlier,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_1_id,
            score=5,
            justification="test",
            date_created=now,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_1_id,
            score=2,
            justification="test",
            date_created=latest,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_2_id,
            score=1,
            justification="test",
            date_created=earlier,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_2_id,
            score=3,
            justification="test",
            date_created=now,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_2_id,
            score=5,
            justification="test",
            date_created=latest,
            user_id=user_id,
        ),
    ]
    _db.session.add_all(scores)
    _db.session.commit()

    result = get_sub_criteria_to_latest_score_map(str(application_id))

    assert result[sub_criteria_1_id] == 2
    assert result[sub_criteria_2_id] == 5


def test_get_scoring_system(seed_scoring_system):
    """test_get_scoring_system Tests getting a scoring system for a given
    round_id.

    Note: The scoring systems are loaded into the database as part of the migration

    """
    test_cases = {
        "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762": "OneToFive",
        "888aae3d-7e2c-4523-b9c1-95952b3d1644": "OneToFive",
        # Add more test cases as needed
    }
    for round_id, scoring_system in test_cases.items():
        returned_scoring_system = get_scoring_system_name_for_round_id(round_id)
        assert returned_scoring_system["scoring_system"] == scoring_system
        assert returned_scoring_system["round_id"] == round_id


def test_all_change_requests_accepted(_db):
    application_id = uuid.uuid4()
    sub_criteria_1_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    now = datetime.datetime.now()

    application = AssessmentRecord(
        application_id=application_id,
        short_id="some_id",
        type_of_application="some_type",
        project_name="some_project_name",
        funding_amount_requested=0.0,
        round_id=uuid.uuid4(),
        fund_id=uuid.uuid4(),
        workflow_status="IN_PROGRESS",
        asset_type="an_asset_type",
        jsonb_blob={},
    )

    a_score = Score(
        application_id=application_id,
        sub_criteria_id=sub_criteria_1_id,
        score=1,
        justification="test",
        date_created=now,
        user_id=user_id,
    )

    a_change_request = AssessmentFlag(
        application_id=application_id,
        sections_to_flag=[sub_criteria_1_id],
        latest_allocation=[],
        latest_status=FlagStatus.RAISED,
        updates=[],
        field_ids=["some_id"],
        is_change_request=True,
    )

    _db.session.add(application)
    _db.session.add(a_score)
    _db.session.add(a_change_request)
    _db.session.commit()

    check_all_change_requests_accepted(application_id)


@pytest.fixture
def setup_application_with_requests_and_scores(_db):
    def _create_app_and_data(
        score_data=None,
        flag_data=None,
    ):
        application_id = uuid.uuid4()
        user_id = str(uuid.uuid4())
        now = datetime.datetime.now()

        application = AssessmentRecord(
            application_id=application_id,
            short_id="some_id",
            type_of_application="some_type",
            project_name="some_project_name",
            funding_amount_requested=0.0,
            round_id=uuid.uuid4(),
            fund_id=uuid.uuid4(),
            workflow_status="IN_PROGRESS",
            asset_type="an_asset_type",
            jsonb_blob={},
        )
        _db.session.add(application)
        _db.session.flush()

        if score_data:
            for sub_criteria_id, score_value in score_data:
                _db.session.add(
                    Score(
                        application_id=application_id,
                        sub_criteria_id=sub_criteria_id,
                        score=score_value,
                        justification="test",
                        date_created=now,
                        user_id=user_id,
                    )
                )

        if flag_data:
            for sections in flag_data:
                _db.session.add(
                    AssessmentFlag(
                        application_id=application_id,
                        sections_to_flag=sections,
                        latest_allocation=[],
                        latest_status=FlagStatus.RAISED,
                        updates=[],
                        field_ids=["some_id"],
                        is_change_request=True,
                    )
                )

        _db.session.commit()
        return application_id

    return _create_app_and_data


@pytest.mark.parametrize(
    "score_value,expected_result",
    [
        (1, True),
        (0, False),
    ],
)
def test_single_request_with_parametrized_score(
    _db, setup_application_with_requests_and_scores, score_value, expected_result
):
    sub_criteria_id = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(
        score_data=[(sub_criteria_id, score_value)],
        flag_data=[[sub_criteria_id]],
    )
    result = check_all_change_requests_accepted(application_id)
    assert result == expected_result


def test_multiple_requests_all_accepted(_db, setup_application_with_requests_and_scores):
    sub_criteria_1_id = str(uuid.uuid4())
    sub_criteria_2_id = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(
        score_data=[
            (sub_criteria_1_id, 1),
            (sub_criteria_2_id, 1),
        ],
        flag_data=[
            [sub_criteria_1_id],
            [sub_criteria_2_id],
        ],
    )
    result = check_all_change_requests_accepted(application_id)
    assert result is True


def test_multiple_change_requests_one_section_accepted(_db, setup_application_with_requests_and_scores):
    sub_criteria_1_id = str(uuid.uuid4())
    sub_criteria_2_id = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(
        score_data=[
            (sub_criteria_1_id, 1),
        ],
        flag_data=[
            [sub_criteria_1_id],
            [sub_criteria_2_id],
        ],
    )
    result = check_all_change_requests_accepted(application_id)
    assert result is False


def test_change_request_multiple_sections_none_accepted(_db, setup_application_with_requests_and_scores):
    sub_criteria_1_id = str(uuid.uuid4())
    sub_criteria_2_id = str(uuid.uuid4())
    sub_criteria_3_id = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(
        flag_data=[
            [sub_criteria_1_id, sub_criteria_2_id, sub_criteria_3_id],
        ]
    )
    result = check_all_change_requests_accepted(application_id)
    assert result is False


def test_change_request_multiple_sections_all_accepted(_db, setup_application_with_requests_and_scores):
    sub_criteria_1_id = str(uuid.uuid4())
    sub_criteria_2_id = str(uuid.uuid4())
    sub_criteria_3_id = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(
        score_data=[
            (sub_criteria_1_id, 1),
            (sub_criteria_2_id, 1),
            (sub_criteria_3_id, 1),
        ],
        flag_data=[[sub_criteria_1_id, sub_criteria_2_id], [sub_criteria_3_id]],
    )
    result = check_all_change_requests_accepted(application_id)
    assert result is True
