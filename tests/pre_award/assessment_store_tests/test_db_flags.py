from uuid import uuid4

import pytest
from sqlalchemy import select

from pre_award.assessment_store.db.models.assessment_record import AssessmentRecord
from pre_award.assessment_store.db.models.assessment_record.enums import Status
from pre_award.assessment_store.db.models.flags.flag_update import FlagStatus
from pre_award.assessment_store.db.queries.flags.queries import (
    add_flag_for_application,
    add_update_to_assessment_flag,
    get_flags_for_application,
)
from tests.pre_award.assessment_store_tests._helpers import get_assessment_record
from tests.pre_award.assessment_store_tests.conftest import test_input_data
from tests.pre_award.assessment_store_tests.test_data.flags import add_flag_update_request_json, flag_config


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_create_flag(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]

    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    results = _db.session.scalars(stmt).all()

    assert len(results) == 1
    assert len(results[0].flags) == 0

    user_id = uuid4()
    flag_data = {
        "application_id": str(app_id),
        "sections_to_flag": ["section_1", "section_2"],
        "justification": "justifying the flag creation",
        "user_id": str(user_id),
        "status": FlagStatus.RAISED,
        "allocation": "TEAM_1",
    }
    create_result = add_flag_for_application(**flag_data)
    assert create_result.latest_status == FlagStatus.RAISED

    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    results = _db.session.scalars(stmt).all()

    assert len(results) == 1
    assert len(results[0].flags) == 1


@pytest.mark.apps_to_insert([{**test_input_data[0], "flags": [flag_config[0]]}])
def test_add_flag_update(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]

    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    results = _db.session.scalars(stmt).all()

    assert len(results) == 1
    assert len(results[0].flags) == 1
    assert len(results[0].flags[0].updates) == 1
    assert results[0].flags[0].latest_allocation == "TEAM_1"

    updated_flag = add_update_to_assessment_flag(
        **add_flag_update_request_json,
        assessment_flag_id=results[0].flags[0].id,
    )
    assert updated_flag.latest_allocation == add_flag_update_request_json["allocation"]

    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    results = _db.session.scalars(stmt).all()

    assert len(results) == 1
    assert len(results[0].flags) == 1
    assert len(results[0].flags[0].updates) == 2
    assert results[0].flags[0].latest_status == FlagStatus.STOPPED
    assert results[0].flags[0].latest_allocation == "TEAM_2"


@pytest.mark.apps_to_insert([{**test_input_data[0], "flags": [flag_config[0]]}])
def test_get_flags_for_application(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    result = get_flags_for_application(app_id)
    assert len(result) == 1
    assert result[0].updates[0].justification == "Test justification 1"
    assert result[0].sections_to_flag[0] == "Test section 1"


# @pytest.mark.skip(reason="integrate flags into seeded data")
@pytest.mark.parametrize(
    "status_or_flag, expected_application_count",
    [
        (
            "NOT_STARTED",
            0,
        ),
        (
            "IN_PROGRESS",
            1,
        ),
        (
            "COMPLETED",
            0,
        ),
        (
            "FLAGGED",
            2,
        ),
        (
            "STOPPED",
            0,
        ),
        (
            "QA_COMPLETED",
            0,
        ),
        (
            "UNKNOWN_STATUS_OR_FLAG",
            0,
        ),
    ],
)
@pytest.mark.apps_to_insert(
    [
        test_input_data[0],
        {**test_input_data[1], "flags": [flag_config[2]]},
        {**test_input_data[2], "flags": [flag_config[1]]},
    ]
)
def test_get_most_recent_metadata_statuses_for_fund_round_id(
    _db, status_or_flag, expected_application_count, seed_application_records
):
    from pre_award.assessment_store.db.queries.assessment_records.queries import (
        get_metadata_for_fund_round_id,
    )

    app_1 = get_assessment_record(seed_application_records[0]["application_id"])
    app_2 = get_assessment_record(seed_application_records[1]["application_id"])
    app_1.workflow_status = Status.IN_PROGRESS
    app_2.workflow_status = Status.COMPLETED
    _db.session.add_all([app_1, app_2])
    _db.session.commit()

    metadata = get_metadata_for_fund_round_id(
        seed_application_records[0]["fund_id"],
        seed_application_records[0]["round_id"],
        "",
        "",
        status_or_flag,
    )
    assert expected_application_count == len(metadata)
