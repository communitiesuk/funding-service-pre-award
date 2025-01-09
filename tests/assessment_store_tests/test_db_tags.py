import random
from uuid import uuid4

import pytest

from pre_award.assessment_store.api.routes.tag_routes import get_tags_for_fund_round, update_tags_for_fund_round
from pre_award.assessment_store.db.queries.assessment_records.queries import associate_assessment_tags
from pre_award.assessment_store.db.queries.tags.queries import get_tag_by_id, insert_tags
from tests.assessment_store_tests.conftest import test_input_data

# _db.session.remove()
# This operation cleans up the session resources and ensures that
# the session is properly closed following the raised error.

tags_incorrect_format = [
    {
        "key": "Test tag 1",
        "purpose": "Green",
        "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
    },
    {
        "value": "Not recommended",
        "species": "silk",
        "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
    },
    {
        "value": "For discussion",
        "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
    },
    {
        "value": "Incomplete - not for review",
        "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
    },
]


def test_insert_tags(_db, clear_test_data, get_tag_types):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tag_type_ids = [t["id"] for t in get_tag_types]
    tags_correct_format = [
        {
            "value": "Test tag 1",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "Not recommended",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "For discussion",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "Incomplete - not for review",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]
    tag_values = [x["value"] for x in tags_correct_format]
    result = insert_tags(tags_correct_format, fund_id_test, round_id_test)
    assert len(result) == 4
    assert [tag.value in tag_values for tag in result]


def test_insert_tags_fails_for_tag_with_special_chars(_db, clear_test_data, get_tag_types):
    tag_type_ids = [t["id"] for t in get_tag_types]
    tag_special_chars = [
        {
            "value": "Test tag 1 !£",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    with pytest.raises(ValueError) as e_info:
        insert_tags(tag_special_chars, fund_id_test, round_id_test)
    assert "The value should only contain apostrophes, hyphens, letters, digits, and spaces." in str(e_info.value)
    _db.session.remove()


def test_insert_tags_for_same_fund_round_twice_fails(_db, clear_test_data, get_tag_types):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tag_type_ids = [t["id"] for t in get_tag_types]
    tags_correct_format = [
        {
            "value": "Test tag 1",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        }
    ]
    insert_tags(tags_correct_format, fund_id_test, round_id_test)

    with pytest.raises(Exception) as e_info:
        insert_tags(tags_correct_format, fund_id_test, round_id_test)

    assert "duplicate key value violates" in str(e_info.value)
    _db.session.remove()


def test_insert_duplicate_tags_same_payload_fails(_db, clear_test_data, get_tag_types):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tag_type_ids = [t["id"] for t in get_tag_types]
    same_tags_with_different_cases = [
        {
            "value": "same test tag",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "same test tag",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]

    with pytest.raises(Exception) as e_info:
        insert_tags(same_tags_with_different_cases, fund_id_test, round_id_test)

    assert "duplicate key value violates" in str(e_info.value)
    _db.session.remove()


def test_insert_duplicate_tags_not_case_sensitive_fails(_db, clear_test_data, get_tag_types):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tag_type_ids = [t["id"] for t in get_tag_types]
    same_tags_with_different_cases = [
        {
            "value": "SAME TEST TAG NOT CASE",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "same test tag not case",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]

    with pytest.raises(Exception) as e_info:
        insert_tags(same_tags_with_different_cases, fund_id_test, round_id_test)

    assert "duplicate key value violates" in str(e_info.value)
    _db.session.remove()


def test_insert_tags_bad_tag_format(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    with pytest.raises(Exception) as e_info:
        insert_tags(tags_incorrect_format, fund_id_test, round_id_test)

    assert "'NoneType' object has no attribute 'strip" in str(e_info.value)
    _db.session.remove()


def test_insert_tag_with_unknown_type_id_fails(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tags_unknown_tag_type = [
        {
            "value": "same test tag not case",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": "4dd2b7d8-12f0-482f-b64b-8809b19baa93",
        },
    ]
    with pytest.raises(Exception) as e_info:
        insert_tags(tags_unknown_tag_type, fund_id_test, round_id_test)

    assert "ForeignKeyViolation" in str(e_info.value)
    # This operation cleans up the session resources and ensures
    # that the session is properly closed following the raised error.
    _db.session.remove()


def test_get_tags(_db, clear_test_data, get_tag_types):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    tag_type_ids = [t["id"] for t in get_tag_types]
    tags_correct_format = [
        {
            "value": "Test tag 1",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "Not recommended",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]
    insert_tags(tags_correct_format, fund_id_test, round_id_test)
    result = get_tags_for_fund_round(fund_id_test, round_id_test)
    tag_values = [x["value"] for x in tags_correct_format]
    assert len(result) == 2
    assert result[0]["value"] in tag_values
    assert all(
        key in result[0].keys()
        for key in [
            "round_id",
            "creator_user_id",
            "fund_id",
            "purpose",
            "created_at",
            "value",
            "id",
            "active",
        ]
    )


def test_deactivate_tags(app, _db, clear_test_data, seed_tags):
    seeded_tag = seed_tags[0]
    fund_id_test = seeded_tag["fund_id"]
    round_id_test = seeded_tag["round_id"]
    result = get_tags_for_fund_round(fund_id_test, round_id_test)
    assert all(tag["active"] is True for tag in result)

    # Deactivate tag
    tags_to_update = [{"active": False, "id": seeded_tag["id"]}]

    with app.test_request_context(json=tags_to_update):
        update_tags_for_fund_round(fund_id_test, round_id_test)

    with app.test_request_context(f"/funds/{fund_id_test}/rounds/{round_id_test}/tags?tag_status=true"):
        result = get_tags_for_fund_round(fund_id_test, round_id_test)
        assert len(result) == 1

    with app.test_request_context(f"/funds/{fund_id_test}/rounds/{round_id_test}/tags?tag_status=false"):
        result = get_tags_for_fund_round(fund_id_test, round_id_test)
        assert len(result) == 1

    # Reactivate tag
    tags_to_update = [{"active": True, "id": seeded_tag["id"]}]
    with app.test_request_context(json=tags_to_update):
        update_tags_for_fund_round(fund_id_test, round_id_test)

    with app.test_request_context(f"/funds/{fund_id_test}/rounds/{round_id_test}/tags?tag_status=true"):
        result = get_tags_for_fund_round(fund_id_test, round_id_test)
        assert len(result) == 2

    with app.test_request_context(f"/funds/{fund_id_test}/rounds/{round_id_test}/tags?tag_status=false"):
        result = get_tags_for_fund_round(fund_id_test, round_id_test)
        assert result.status_code == 204
        assert result.data.decode("utf-8") == ""


def test_deactivate_tags_fails_for_non_existent(app, _db, clear_test_data, seed_tags):
    seeded_tag = seed_tags[0]
    fund_id_test = seeded_tag["fund_id"]
    round_id_test = seeded_tag["round_id"]
    result = get_tags_for_fund_round(fund_id_test, round_id_test)
    assert all(tag["active"] is True for tag in result)
    tags_to_update = [{"active": False, "id": "68d39aee-4f4a-42d2-a2e7-66c5934905a1"}]

    # simulate request body
    with app.test_request_context(json=tags_to_update):
        with pytest.raises(Exception) as e_info:
            update_tags_for_fund_round(fund_id_test, round_id_test)
    assert all(text in str(e_info.value) for text in ["Tag with id", "does not exist for fund_id"])

    result = get_tags_for_fund_round(fund_id_test, round_id_test)
    assert all(tag["active"] is True for tag in result)


def test_get_tag(seed_tags):
    tag_id = seed_tags[0]["id"]
    fund_id = seed_tags[0]["fund_id"]
    round_id = seed_tags[0]["round_id"]
    tag = get_tag_by_id(fund_id, round_id, tag_id)
    assert tag
    assert str(tag.id) == tag_id
    assert tag.value == "Test tag 1"


@pytest.mark.apps_to_insert(test_input_data)
def test_get_tag_has_correct_tag_association_count(seed_application_records, seed_tags):
    """The tag association count should update when a tag is disassociated from an
    application."""
    seeded_tags_info = (
        (seed_tags[0]["id"], seed_tags[0]["value"]),
        (seed_tags[1]["id"], seed_tags[1]["value"]),
    )
    app_1_id = seed_application_records[0]["application_id"]
    app_2_id = seed_application_records[1]["application_id"]
    fund_id = seed_tags[0]["fund_id"]
    round_id = seed_tags[0]["round_id"]

    def check_tags(expected_associated_count):
        """Compare the seeded tag info with the tag info retrieved from the
        database."""
        for seeded_tag in seeded_tags_info:
            tag = get_tag_by_id(fund_id, round_id, seeded_tag[0])

            # assert we have matched on the correct tag
            assert tag
            assert str(tag.id) == seeded_tag[0]
            assert tag.value == seeded_tag[1]

            # assert the tag association count is correct
            assert tag.tag_association_count == expected_associated_count

    # There should be no tag associations
    check_tags(0)

    # generate tag associations
    new_tag_associations = [{"id": tag["id"], "user_id": "1d49a41c-a13e-41ab-a89c-240b3de3fbda"} for tag in seed_tags]

    # Associate each tag with one application
    associate_assessment_tags(app_1_id, new_tag_associations)
    check_tags(1)

    # Associate each tag with another application
    associate_assessment_tags(app_2_id, new_tag_associations)
    check_tags(2)

    # Now dis-associate and see change in tag association count (now tags are only associated with app_2)
    # sets existing tag to False
    associate_assessment_tags(
        app_1_id,
        [{"id": "", "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"}],
    )
    check_tags(2)

    # Disassociate all tags from app_2 (set existing tag to False)
    associate_assessment_tags(
        app_2_id,
        [{"id": "", "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"}],
    )
    check_tags(2)


def test_get_tag_bad_id(seed_tags):
    tag_id = str(uuid4())
    fund_id = seed_tags[0]["fund_id"]
    round_id = seed_tags[0]["round_id"]
    tag = get_tag_by_id(fund_id, round_id, tag_id)
    assert tag is None
