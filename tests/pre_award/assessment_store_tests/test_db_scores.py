import datetime
import uuid
from unittest.mock import MagicMock

import pytest

from pre_award.assessment_store.api.routes.progress_routes import get_progress_for_applications
from pre_award.assessment_store.api.routes.score_routes import get_scoring_system_name_for_round_id
from pre_award.assessment_store.db.models import AssessmentFlag, AssessmentRecord, Score
from pre_award.assessment_store.db.models.assessment_record.enums import Status as ApplicationStatus
from pre_award.assessment_store.db.models.flags import FlagStatus, FlagUpdate
from pre_award.assessment_store.db.queries.assessment_records.queries import check_all_change_requests_accepted
from pre_award.assessment_store.db.queries.flags.queries import get_change_requests_for_application
from pre_award.assessment_store.db.queries.scores.queries import (
    accept_sub_criteria,
    create_score_for_app_sub_crit,
    get_scores_for_app_sub_crit,
    get_sub_criteria_to_latest_score_map,
)
from tests.pre_award.assessment_store_tests._helpers import get_assessment_record
from tests.pre_award.assessment_store_tests.conftest import test_input_data


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_create_scores_for_application_sub_crit(db, seed_application_records):
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
def test_get_sub_criteria_to_latest_score_map(db, seed_application_records):
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
    db.session.add_all(scores)
    db.session.commit()

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


def test_all_change_requests_accepted(db):
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

    db.session.add(application)
    db.session.add(a_score)
    db.session.add(a_change_request)
    db.session.commit()

    check_all_change_requests_accepted(application_id)


@pytest.fixture
def setup_application_with_requests_and_scores(db):
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
            workflow_status=ApplicationStatus.CHANGE_REQUESTED,
            asset_type="an_asset_type",
            jsonb_blob={},
        )
        db.session.add(application)
        db.session.flush()

        if score_data:
            for sub_criteria_id, score_value in score_data:
                db.session.add(
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
                db.session.add(
                    AssessmentFlag(
                        application_id=application_id,
                        sections_to_flag=sections,
                        latest_allocation=[],
                        latest_status=FlagStatus.RAISED,
                        updates=[
                            FlagUpdate(
                                justification="None",
                                user_id=user_id,
                                status=FlagStatus.RAISED,
                                allocation=None,
                            )
                        ],
                        field_ids=["some_id"],
                        is_change_request=True,
                    )
                )

        db.session.commit()
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
    setup_application_with_requests_and_scores, score_value, expected_result
):
    sub_criteria_id = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(
        score_data=[(sub_criteria_id, score_value)],
        flag_data=[[sub_criteria_id]],
    )
    result = check_all_change_requests_accepted(application_id)
    assert result == expected_result


def test_multiple_requests_all_accepted(db, setup_application_with_requests_and_scores):
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


def test_multiple_change_requests_one_section_accepted(db, setup_application_with_requests_and_scores):
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


def test_change_request_multiple_sections_none_accepted(db, setup_application_with_requests_and_scores):
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


def test_change_request_multiple_sections_all_accepted(db, setup_application_with_requests_and_scores):
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


def test_approve_sub_criteria_resolves_change_request(db, setup_application_with_requests_and_scores):
    section_1 = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(flag_data=[[section_1], [section_1]])

    accept_sub_criteria(
        application_id=application_id, sub_criteria_id=section_1, user_id=str(uuid.uuid4()), message="test", score=1
    )

    change_requests = get_change_requests_for_application(application_id)
    assert all(cr.latest_status == FlagStatus.RESOLVED for cr in change_requests)


def test_approve_sub_criteria_creates_score(db, setup_application_with_requests_and_scores):
    sub_criteria_id = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(flag_data=[[sub_criteria_id]])

    accept_sub_criteria(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        user_id=str(uuid.uuid4()),
        message="test",
        score=1,
    )

    scores = db.session.query(Score).filter_by(application_id=application_id, sub_criteria_id=sub_criteria_id).all()
    assert len(scores) == 1
    assert scores[0].score == 1
    assert scores[0].justification == "test"


def test_approve_sub_criteria_updates_application_status(db, setup_application_with_requests_and_scores):
    sub_criteria_id = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(flag_data=[[sub_criteria_id]])

    accept_sub_criteria(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        user_id=str(uuid.uuid4()),
        message="test",
        score=1,
    )

    application = db.session.query(AssessmentRecord).filter_by(application_id=application_id).first()
    assert application.workflow_status == ApplicationStatus.IN_PROGRESS


def test_approve_sub_criteria_multiple_change_requests_diff_subcriteria(setup_application_with_requests_and_scores, db):
    sub_criteria_id_1 = str(uuid.uuid4())
    sub_criteria_id_2 = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(flag_data=[[sub_criteria_id_1], [sub_criteria_id_2]])

    accept_sub_criteria(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id_1,
        user_id=str(uuid.uuid4()),
        message="test",
        score=1,
    )

    change_requests = get_change_requests_for_application(application_id, only_raised=False, sort_by_update=True)
    resolved_requests = [cr for cr in change_requests if cr.latest_status == FlagStatus.RESOLVED]
    unresolved_requests = [cr for cr in change_requests if cr.latest_status == FlagStatus.RAISED]

    assert len(resolved_requests) == 1
    assert len(unresolved_requests) == 1
    assert unresolved_requests[0].sections_to_flag == [sub_criteria_id_2]

    application = db.session.query(AssessmentRecord).filter_by(application_id=application_id).first()
    assert application.workflow_status == ApplicationStatus.CHANGE_REQUESTED

    # Accepting last remaining sub-criteria should change application status
    accept_sub_criteria(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id_2,
        user_id=str(uuid.uuid4()),
        message="test",
        score=2,
    )

    change_requests = get_change_requests_for_application(application_id)
    resolved_requests = [cr for cr in change_requests if cr.latest_status == FlagStatus.RESOLVED]
    unresolved_requests = [cr for cr in change_requests if cr.latest_status == FlagStatus.RAISED]

    assert len(resolved_requests) == 2
    assert len(unresolved_requests) == 0

    application = db.session.query(AssessmentRecord).filter_by(application_id=application_id).first()
    assert application.workflow_status == ApplicationStatus.IN_PROGRESS


def test_accept_sub_criteria_multiple_change_requests_same_subcriteria(setup_application_with_requests_and_scores):
    sub_criteria_id = str(uuid.uuid4())
    application_id = setup_application_with_requests_and_scores(flag_data=[[sub_criteria_id], [sub_criteria_id]])

    accept_sub_criteria(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        user_id=str(uuid.uuid4()),
        message="test",
        score=1,
    )

    change_requests = get_change_requests_for_application(application_id)
    resolved_requests = [cr for cr in change_requests if cr.latest_status == FlagStatus.RESOLVED]
    unresolved_requests = [cr for cr in change_requests if cr.latest_status == FlagStatus.RAISED]

    assert len(resolved_requests) == 2
    assert len(unresolved_requests) == 0
