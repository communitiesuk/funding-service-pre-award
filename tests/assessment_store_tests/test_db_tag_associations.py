import pytest
from sqlalchemy import select

from pre_award.assessment_store.api.routes.tag_routes import (
    get_active_tags_associated_with_assessment,
    update_tags_for_fund_round,
)
from pre_award.assessment_store.db.models.assessment_record import AssessmentRecord
from pre_award.assessment_store.db.queries.assessment_records.queries import associate_assessment_tags
from tests.assessment_store_tests.conftest import test_input_data


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_associate_tags(_db, seed_application_records, seed_tags):
    app_id = seed_application_records[0]["application_id"]
    new_tags = [{"id": tag["id"], "user_id": "1d49a41c-a13e-41ab-a89c-240b3de3fbda"} for tag in seed_tags]
    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    app = _db.session.scalars(stmt).one()
    assert len(app.tag_associations) == 0

    associate_assessment_tags(app_id, new_tags)

    app = _db.session.scalars(stmt).one()
    assert len(app.tag_associations) == len(new_tags)

    seeded_tags_ids = [tag["id"] for tag in new_tags]
    associated_tag_ids = [str(t_a.tag_id) for t_a in app.tag_associations]
    assert set(seeded_tags_ids) == set(associated_tag_ids)


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_that_calling_with_the_same_tags_doesnt_duplicate_association(_db, seed_application_records, seed_tags):
    app_id = seed_application_records[0]["application_id"]
    new_tags = [{"id": tag["id"], "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"} for tag in seed_tags]
    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    app = _db.session.scalars(stmt).one()
    assert len(app.tag_associations) == 0

    associate_assessment_tags(app_id, new_tags)
    associate_assessment_tags(app_id, new_tags)

    app = _db.session.scalars(stmt).one()
    assert len(app.tag_associations) == len(new_tags)

    seeded_tags_ids = [tag["id"] for tag in new_tags]
    associated_tag_ids = [str(t_a.tag_id) for t_a in app.tag_associations]
    assert set(seeded_tags_ids) == set(associated_tag_ids)


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_tag_association_disassociation_workflow_is_working_correctly(_db, seed_application_records, seed_tags):
    app_id = seed_application_records[0]["application_id"]
    new_tags = [{"id": tag["id"], "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"} for tag in seed_tags]
    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    app = _db.session.scalars(stmt).one()
    assert len(app.tag_associations) == 0

    # associate two tags
    associate_assessment_tags(app_id, new_tags)
    tags = get_active_tags_associated_with_assessment(app_id)
    assert len(tags) == len(new_tags)

    # associate a single tag and expect other tag to be disassociated with no tag_id
    updated_tags = [
        new_tags[0],
        {"id": "", "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"},
    ]
    associate_assessment_tags(app_id, updated_tags)
    actual_tags = get_active_tags_associated_with_assessment(app_id)
    assert len(actual_tags) == len(updated_tags) - 1

    updated_tag_ids = [tag["id"] for tag in updated_tags]
    actual_tag_ids = [t_a["tag_id"] for t_a in actual_tags]
    assert updated_tag_ids[0] == actual_tag_ids[0]
    assert updated_tag_ids[1] != actual_tag_ids[0]

    # associate two tags again
    associate_assessment_tags(app_id, new_tags)
    actual_tags = get_active_tags_associated_with_assessment(app_id)
    assert len(actual_tags) == len(new_tags)

    # associate no tags and expect all associated tags to be removed
    associate_assessment_tags(app_id, [{"id": "", "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"}])
    actual_tags = get_active_tags_associated_with_assessment(app_id)
    assert actual_tags == []  # noqa: E711


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_tag_association_history_is_retained_for_reassociated_tags(_db, seed_application_records, seed_tags):
    """When a tag is associated we record the time and user if this tag is
    disassociated the associated value of that tag is set to False when another
    tag is raised for an application for a tag with the same tag_ig, ensure we
    create a new record for this."""
    app_id = seed_application_records[0]["application_id"]
    new_tags = [{"id": tag["id"], "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"} for tag in seed_tags]
    single_tag = [new_tags[0]]

    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    app = _db.session.scalars(stmt).one()
    # check there are no tags associated or disassociated for an app
    assert len(app.tag_associations) == 0

    # (TAG 1) associate a single tag
    associate_assessment_tags(app_id, single_tag)
    app = _db.session.scalars(stmt).one()
    # check total associated or disassociated tags
    assert len(app.tag_associations) == 1
    # check total associated tags
    tags = get_active_tags_associated_with_assessment(app_id)
    assert len(tags) == 1
    assert tags[0]["user_id"] == "5dd2b7d8-12f0-482f-b64b-8809b19baa93"

    # (TAG 2) disassociate the tag
    associate_assessment_tags(app_id, [{"id": "", "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"}])
    tags = get_active_tags_associated_with_assessment(app_id)
    app = _db.session.scalars(stmt).one()
    # check total associated or disassociated tags

    assert len(app.tag_associations) == 2
    # check total associated tags
    tags = get_active_tags_associated_with_assessment(app_id)
    assert tags == []  # noqa: E711

    # (TAG 3) associate the single tag again as a different user
    single_tag[0]["user_id"] = "2d8e6a2e-aa22-417f-a138-90569c8b238f"
    associate_assessment_tags(app_id, single_tag)
    app = _db.session.scalars(stmt).one()
    # check total associated or disassociated tags
    assert len(app.tag_associations) == 3
    # check total associated tags
    tags = get_active_tags_associated_with_assessment(app_id)
    assert len(tags) == 1
    assert tags[0]["user_id"] == "2d8e6a2e-aa22-417f-a138-90569c8b238f"

    # (TAG 4) disassociate the tag
    associate_assessment_tags(app_id, [{"id": "", "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"}])
    tags = get_active_tags_associated_with_assessment(app_id)
    app = _db.session.scalars(stmt).one()
    # check total associated or disassociated tags
    assert len(app.tag_associations) == 4
    # check total associated tags
    tags = get_active_tags_associated_with_assessment(app_id)
    assert tags == []  # noqa: E711


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_tag_association_only_returns_assocaitions_for_active_tags(app, _db, seed_application_records, seed_tags):
    app_id = seed_application_records[0]["application_id"]
    new_tags = [
        {
            "id": tag["id"],
            "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "fund_id": tag["fund_id"],
            "round_id": tag["round_id"],
        }
        for tag in seed_tags
    ]
    single_tag = new_tags[0]
    fund_id = single_tag["fund_id"]
    round_id = single_tag["round_id"]
    del single_tag["fund_id"]
    del single_tag["round_id"]

    stmt = select(AssessmentRecord).where(AssessmentRecord.application_id == app_id)
    application = _db.session.scalars(stmt).one()
    # check there are no tags associated or disassociated for an app
    assert len(application.tag_associations) == 0

    # associate a single tag
    associate_assessment_tags(app_id, [single_tag])
    application = _db.session.scalars(stmt).one()
    # check total associated tags
    assert len(application.tag_associations) == 1
    tags = get_active_tags_associated_with_assessment(app_id)
    assert len(tags) == 1
    assert tags[0]["user_id"] == "5dd2b7d8-12f0-482f-b64b-8809b19baa93"

    # Deactivate tag
    tags_to_update = [{"active": False, "id": single_tag["id"]}]
    with app.test_request_context(json=tags_to_update):
        update_tags_for_fund_round(fund_id, round_id)

    # we return no tags associations as the tag is not inactive
    tags = get_active_tags_associated_with_assessment(app_id)
    assert tags == []
    # the association still exists but the tag is not inactive
    application = _db.session.scalars(stmt).one()
    assert len(application.tag_associations) == 1
