from datetime import datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from sqlalchemy import select

from pre_award.assessment_store.db.models.assessment_record import AssessmentRecord
from pre_award.assessment_store.db.models.assessment_record.enums import Status
from pre_award.assessment_store.db.models.flags.assessment_flag import AssessmentFlag
from pre_award.assessment_store.db.models.flags.flag_update import FlagStatus, FlagUpdate
from pre_award.assessment_store.db.queries.flags.queries import (
    add_flag_for_application,
    add_update_to_assessment_flag,
    get_change_requests_for_application,
    get_flags_for_application,
    is_first_change_request_for_date,
    prepare_change_requests_metadata,
)
from tests.pre_award.assessment_store_tests._helpers import get_assessment_record
from tests.pre_award.assessment_store_tests.conftest import test_input_data
from tests.pre_award.assessment_store_tests.test_data.flags import add_flag_update_request_json, flag_config


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_create_flag(db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]

    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    results = db.session.scalars(stmt).all()

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
    results = db.session.scalars(stmt).all()

    assert len(results) == 1
    assert len(results[0].flags) == 1


@pytest.mark.apps_to_insert([{**test_input_data[0], "flags": [flag_config[0]]}])
def test_add_flag_update(db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]

    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    results = db.session.scalars(stmt).all()

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
    results = db.session.scalars(stmt).all()

    assert len(results) == 1
    assert len(results[0].flags) == 1
    assert len(results[0].flags[0].updates) == 2
    assert results[0].flags[0].latest_status == FlagStatus.STOPPED
    assert results[0].flags[0].latest_allocation == "TEAM_2"


@pytest.mark.apps_to_insert([{**test_input_data[0], "flags": [flag_config[0]]}])
def test_get_flags_for_application(db, seed_application_records):
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
    status_or_flag, expected_application_count, seed_application_records, db
):
    from pre_award.assessment_store.db.queries.assessment_records.queries import (
        get_metadata_for_fund_round_id,
    )

    app_1 = get_assessment_record(seed_application_records[0]["application_id"])
    app_2 = get_assessment_record(seed_application_records[1]["application_id"])
    app_1.workflow_status = Status.IN_PROGRESS
    app_2.workflow_status = Status.COMPLETED
    db.session.add_all([app_1, app_2])
    db.session.commit()

    metadata = get_metadata_for_fund_round_id(
        seed_application_records[0]["fund_id"],
        seed_application_records[0]["round_id"],
        "",
        "",
        status_or_flag,
    )
    assert expected_application_count == len(metadata)


# Test cases
def test_get_change_requests_no_flags(mocker):
    mock_session = mocker.patch("pre_award.assessment_store.db.queries.flags.queries.db.session.query")
    mock_join = mock_session.return_value.join
    mock_filter1 = mock_join.return_value.filter
    mock_options = mock_filter1.return_value.options
    mock_filter2 = mock_options.return_value.filter
    mock_filter2.return_value.all.return_value = []

    result = prepare_change_requests_metadata("123")
    assert result is None


def test_get_change_requests_with_flags(mocker):
    mock_flag_update = MagicMock()
    mock_flag_update.justification = "Justification 1"

    mock_assessment_flag = MagicMock()
    mock_assessment_flag.field_ids = ["field_1", "field_2"]
    mock_assessment_flag.updates = [mock_flag_update]

    mock_session = mocker.patch("pre_award.assessment_store.db.queries.flags.queries.db.session.query")
    mock_join = mock_session.return_value.join
    mock_filter1 = mock_join.return_value.filter
    mock_options = mock_filter1.return_value.options
    mock_filter2 = mock_options.return_value.filter
    mock_filter2.return_value.all.return_value = [mock_assessment_flag]

    result = prepare_change_requests_metadata("123")

    expected_result = {
        "field_1": ["Justification 1"],
        "field_2": ["Justification 1"],
    }
    assert result == expected_result


def test_get_change_requests_multiple_flags(mocker):
    mock_flag_update1 = MagicMock()
    mock_flag_update1.justification = "Justification 1"

    mock_flag_update2 = MagicMock()
    mock_flag_update2.justification = "Justification 2"

    mock_assessment_flag1 = MagicMock()
    mock_assessment_flag1.field_ids = ["field_1"]
    mock_assessment_flag1.updates = [mock_flag_update1]

    mock_assessment_flag2 = MagicMock()
    mock_assessment_flag2.field_ids = ["field_2"]
    mock_assessment_flag2.updates = [mock_flag_update2]

    mock_session = mocker.patch("pre_award.assessment_store.db.queries.flags.queries.db.session.query")
    mock_join = mock_session.return_value.join
    mock_filter1 = mock_join.return_value.filter
    mock_options = mock_filter1.return_value.options
    mock_filter2 = mock_options.return_value.filter
    mock_filter2.return_value.all.return_value = [
        mock_assessment_flag1,
        mock_assessment_flag2,
    ]

    result = prepare_change_requests_metadata("123")

    expected_result = {
        "field_1": ["Justification 1"],
        "field_2": ["Justification 2"],
    }
    assert result == expected_result


def create_change_request(db, application_id, status, updates=None, is_change_request=True):
    flag = AssessmentFlag(
        application_id=application_id,
        latest_status=status,
        latest_allocation="Team A",
        sections_to_flag=["section1"],
        updates=[],
        field_ids=["field1"],
        is_change_request=is_change_request,
    )
    if db:
        db.session.add(flag)
        db.session.commit()

    if updates:
        for i, update in enumerate(updates):
            new_update = FlagUpdate(
                assessment_flag_id=flag.id,
                user_id=f"user{i}",
                date_created=update.get("date_created", datetime(2025, 2, 4)),
                justification=update.get("justification", f"Test justification {i}"),
                status=update.get("status", status),
                allocation="Team A",
            )
            if db:
                db.session.add(new_update)
        if db:
            db.session.commit()
        flag.updates.append(new_update)

    return flag


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_get_all_change_requests(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    create_change_request(
        _db, app_id, FlagStatus.RAISED, updates=[{"status": FlagStatus.RAISED, "date_created": datetime(2025, 2, 4)}]
    )
    create_change_request(
        _db,
        app_id,
        FlagStatus.RESOLVED,
        updates=[{"status": FlagStatus.RESOLVED, "date_created": datetime(2025, 2, 4) - timedelta(days=1)}],
    )

    results = get_change_requests_for_application(app_id)
    assert len(results) == 2


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_get_only_raised_change_requests(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    create_change_request(
        _db, app_id, FlagStatus.RAISED, updates=[{"status": FlagStatus.RAISED, "date_created": datetime(2025, 2, 4)}]
    )
    create_change_request(
        _db,
        app_id,
        FlagStatus.RESOLVED,
        updates=[{"status": FlagStatus.RESOLVED, "date_created": datetime(2025, 2, 4) - timedelta(days=1)}],
    )

    results = get_change_requests_for_application(app_id, only_raised=True)
    assert len(results) == 1
    assert results[0].latest_status == FlagStatus.RAISED


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_sort_by_update(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    base_date = datetime(2025, 2, 4)

    flag1 = create_change_request(
        _db,
        app_id,
        FlagStatus.RAISED,
        updates=[
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=3)},
            {"status": FlagStatus.RESOLVED, "date_created": base_date - timedelta(days=2)},
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=1)},
        ],
    )
    flag2 = create_change_request(
        _db,
        app_id,
        FlagStatus.RAISED,
        updates=[
            {"status": FlagStatus.RESOLVED, "date_created": base_date - timedelta(days=4)},
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=3)},
        ],
    )
    flag3 = create_change_request(
        _db,
        app_id,
        FlagStatus.RESOLVED,
        updates=[
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=5)},
            {"status": FlagStatus.RESOLVED, "date_created": base_date - timedelta(days=4)},
            {"status": FlagStatus.RESOLVED, "date_created": base_date - timedelta(days=3)},
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=2)},
        ],
    )

    results = get_change_requests_for_application(app_id, sort_by_update=True)
    assert len(results) == 3
    assert results[0].id == flag1.id and results[1].id == flag3.id and results[2].id == flag2.id, (
        "Flags returned in wrong order"
    )


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_sort_by_update_only_raised(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    base_date = datetime(2025, 2, 4)

    flag1 = create_change_request(
        _db,
        app_id,
        FlagStatus.RAISED,
        updates=[
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=6)},
            {"status": FlagStatus.RESOLVED, "date_created": base_date - timedelta(days=5)},
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=4)},
        ],
    )
    create_change_request(
        _db,
        app_id,
        FlagStatus.RESOLVED,
        updates=[
            {"status": FlagStatus.RESOLVED, "date_created": base_date},
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=3)},
        ],
    )
    flag3 = create_change_request(
        _db,
        app_id,
        FlagStatus.RAISED,
        updates=[
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=4)},
            {"status": FlagStatus.RESOLVED, "date_created": base_date - timedelta(days=2)},
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=2)},
        ],
    )
    flag4 = create_change_request(
        _db,
        app_id,
        FlagStatus.RAISED,
        updates=[
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=1)},
            {"status": FlagStatus.RAISED, "date_created": base_date - timedelta(days=4)},
        ],
    )

    results = get_change_requests_for_application(app_id, only_raised=True, sort_by_update=True)
    assert len(results) == 3

    assert flag4.id == results[0].id and flag3.id == results[1].id and flag1.id == results[2].id


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_no_change_requests(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    results = get_change_requests_for_application(app_id)
    assert len(results) == 0


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_exclude_non_change_requests(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    create_change_request(
        _db,
        app_id,
        FlagStatus.RAISED,
        updates=[{"status": FlagStatus.RAISED, "date_created": datetime(2025, 2, 4)}],
        is_change_request=False,
    )
    create_change_request(
        _db, app_id, FlagStatus.RAISED, updates=[{"status": FlagStatus.RAISED, "date_created": datetime(2025, 2, 4)}]
    )

    results = get_change_requests_for_application(app_id)
    assert len(results) == 1
    assert results[0].is_change_request is True


def test_no_previous_change_requests(mocker):
    today_date = datetime(2025, 2, 4).date()
    application_id = "mock-application-id"
    mocker.patch(
        "pre_award.assessment_store.db.queries.flags.queries.get_change_requests_for_application", return_value=[]
    )

    result = is_first_change_request_for_date(application_id, today_date)
    assert result is True


def test_latest_request_previous_day(mocker):
    today_date = datetime(2025, 2, 4).date()
    application_id = "mock-application-id"
    yesterday = datetime(2025, 2, 3)
    mock_flag = create_change_request(
        None, application_id, FlagStatus.RAISED, updates=[{"date_created": yesterday, "status": FlagStatus.RAISED}]
    )

    mocker.patch(
        "pre_award.assessment_store.db.queries.flags.queries.get_change_requests_for_application",
        return_value=[mock_flag],
    )

    result = is_first_change_request_for_date(application_id, today_date)
    assert result is True


def test_latest_request_today(mocker):
    today_date = datetime(2025, 2, 4).date()
    application_id = "mock-application-id"
    today_datetime = datetime(2025, 2, 4, 10, 0)
    mock_flag = create_change_request(
        None, application_id, FlagStatus.RAISED, updates=[{"date_created": today_datetime, "status": FlagStatus.RAISED}]
    )

    mocker.patch(
        "pre_award.assessment_store.db.queries.flags.queries.get_change_requests_for_application",
        return_value=[mock_flag],
    )

    result = is_first_change_request_for_date(application_id, today_date)
    assert result is False


def test_multiple_updates_none_today(mocker):
    today_date = datetime(2025, 2, 4).date()
    application_id = "mock-application-id"
    updates = [
        {"date_created": datetime(2025, 2, 2), "status": FlagStatus.RAISED},
        {"date_created": datetime(2025, 2, 3), "status": FlagStatus.RESOLVED},
    ]

    mock_flag = create_change_request(None, application_id, FlagStatus.RAISED, updates=updates)

    mocker.patch(
        "pre_award.assessment_store.db.queries.flags.queries.get_change_requests_for_application",
        return_value=[mock_flag],
    )

    result = is_first_change_request_for_date(application_id, today_date)
    assert result is True


def test_multiple_updates_with_today(mocker):
    today_date = datetime(2025, 2, 4).date()
    application_id = "mock-application-id"
    updates = [
        {"date_created": datetime(2025, 2, 2), "status": FlagStatus.RAISED},
        {"date_created": datetime(2025, 2, 4, 9, 0), "status": FlagStatus.RAISED},
    ]

    mock_flag = create_change_request(None, application_id, FlagStatus.RAISED, updates=updates)

    mocker.patch(
        "pre_award.assessment_store.db.queries.flags.queries.get_change_requests_for_application",
        return_value=[mock_flag],
    )

    result = is_first_change_request_for_date(application_id, today_date)
    assert result is False
