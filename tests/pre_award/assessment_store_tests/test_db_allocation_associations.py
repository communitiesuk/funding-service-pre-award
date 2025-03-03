import uuid
from datetime import datetime, timezone

import pytest

from pre_award.assessment_store.db.models.assessment_record.allocation_association import AllocationAssociation
from pre_award.assessment_store.db.queries.assessment_records.queries import (
    create_user_application_association,
    get_user_application_associations,
    update_user_application_association,
)
from tests.pre_award.assessment_store_tests.conftest import test_input_data


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_get_users_for_application(db, seed_application_records, mock_tasklist_function_calls):
    user_id_1 = str(uuid.uuid4())
    user_id_2 = str(uuid.uuid4())
    assigner_id = str(uuid.uuid4())
    app_id = seed_application_records[0]["application_id"]
    allocation_association_1 = AllocationAssociation(
        user_id=user_id_1,
        assigner_id=assigner_id,
        application_id=app_id,
        active=True,
        log={
            datetime.now(tz=timezone.utc).isoformat(): {
                "status": "activated",
                "assigner": str(assigner_id),
            }
        },
    )
    allocation_association_2 = AllocationAssociation(
        user_id=user_id_2,
        assigner_id=assigner_id,
        application_id=app_id,
        active=False,
        log={
            datetime.now(tz=timezone.utc).isoformat(): {
                "status": "deactivated",
                "assigner": str(assigner_id),
            }
        },
    )
    db.session.add(allocation_association_1)
    db.session.commit()
    db.session.add(allocation_association_2)
    db.session.commit()
    users = get_user_application_associations(application_id=app_id)
    assert len(users) == 2

    active_users = get_user_application_associations(application_id=app_id, active=True)
    assert len(active_users) == 1
    assert str(active_users[0].user_id) == user_id_1

    inactive_users = get_user_application_associations(application_id=app_id, active=False)
    assert len(inactive_users) == 1
    assert str(inactive_users[0].user_id) == user_id_2


@pytest.mark.apps_to_insert([{**test_input_data[0]}, {**test_input_data[1]}])
def test_get_applications_for_user(db, seed_application_records):
    user_id = str(uuid.uuid4())
    assigner_id_1 = str(uuid.uuid4())
    assigner_id_2 = str(uuid.uuid4())
    app_id_1 = seed_application_records[0]["application_id"]
    app_id_2 = seed_application_records[1]["application_id"]
    allocation_association_1 = AllocationAssociation(
        user_id=user_id,
        assigner_id=assigner_id_1,
        application_id=app_id_1,
        active=True,
        log={
            datetime.now(tz=timezone.utc).isoformat(): {
                "status": "activated",
                "assigner": str(assigner_id_1),
            }
        },
    )
    allocation_association_2 = AllocationAssociation(
        user_id=user_id,
        assigner_id=assigner_id_2,
        application_id=app_id_2,
        active=False,
        log={
            datetime.now(tz=timezone.utc).isoformat(): {
                "status": "deactivated",
                "assigner": str(assigner_id_2),
            }
        },
    )
    db.session.add(allocation_association_1)
    db.session.commit()
    db.session.add(allocation_association_2)
    db.session.commit()
    applications = get_user_application_associations(user_id=user_id)
    assert len(applications) == 2

    active_applications = get_user_application_associations(user_id=user_id, active=True)
    assert len(active_applications) == 1
    assert str(active_applications[0].application_id) == app_id_1

    inactive_applications = get_user_application_associations(user_id=user_id, active=False)
    assert len(inactive_applications) == 1
    assert str(inactive_applications[0].application_id) == app_id_2

    assigner_1_applications = get_user_application_associations(assigner_id=assigner_id_1)
    assert len(assigner_1_applications) == 1
    assert str(assigner_1_applications[0].application_id) == app_id_1


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_create_user_application_association(db, seed_application_records):
    user_id = str(uuid.uuid4())
    assigner_id = str(uuid.uuid4())
    app_id = seed_application_records[0]["application_id"]
    new_association = create_user_application_association(app_id, user_id, assigner_id)
    assert new_association is not None
    assert str(new_association.application_id) == app_id
    assert str(new_association.user_id) == user_id
    assert new_association.active is True
    assert {"assigner": assigner_id, "status": "activated"} == list(new_association.log.values())[0]
    try:
        datetime.fromisoformat(list(new_association.log.keys())[0])
    except ValueError as e:
        raise AssertionError("log keys should be in isoformat") from e


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_update_user_application_association(db, seed_application_records):
    user_id = str(uuid.uuid4())
    assigner_id_1 = str(uuid.uuid4())
    assigner_id_2 = str(uuid.uuid4())
    app_id = seed_application_records[0]["application_id"]
    create_user_application_association(app_id, user_id, assigner_id_1)
    updated_association = update_user_application_association(app_id, user_id, active=False, assigner_id=assigner_id_2)
    assert updated_association.active is False
    assert len(updated_association.log.keys()) == 2
    assert str(updated_association.assigner_id) == assigner_id_2
    logs = [(datetime.fromisoformat(key), value) for key, value in updated_association.log.items()]

    # The timestamp for deactivated should be after activated
    assert logs[0][1]["status"] == "activated" if logs[0][0] < logs[1][0] else "deactivated"
    assert logs[1][1]["status"] == "deactivated" if logs[0][0] < logs[1][0] else "activated"


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_duplicate_user_application_association(db, seed_application_records):
    user_id = str(uuid.uuid4())
    app_id = seed_application_records[0]["application_id"]
    updated_association = create_user_application_association(app_id, user_id, str(uuid.uuid4()))
    duplicate_return_value = create_user_application_association(app_id, user_id, str(uuid.uuid4()))
    assert updated_association is not None
    assert duplicate_return_value is None
