import copy
import json
import random
from datetime import datetime, timedelta
from typing import Any, List
from uuid import uuid4

import pytest
from flask import current_app
from flask.testing import FlaskClient
from sqlalchemy import exc
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from werkzeug.test import TestResponse

from app import create_app
from pre_award.account_store.db.models.account import Account
from pre_award.assessment_store.config.mappings.assessment_mapping_fund_round import (
    fund_round_mapping_config_with_round_id,
)
from pre_award.assessment_store.db.models import AssessmentRound
from pre_award.assessment_store.db.models.assessment_record import AssessmentRecord
from pre_award.assessment_store.db.models.assessment_record.allocation_association import AllocationAssociation
from pre_award.assessment_store.db.models.assessment_record.tag_association import TagAssociation
from pre_award.assessment_store.db.models.comment import Comment, CommentsUpdate
from pre_award.assessment_store.db.models.comment.enums import CommentType
from pre_award.assessment_store.db.models.flags.assessment_flag import AssessmentFlag
from pre_award.assessment_store.db.models.flags.flag_update import FlagUpdate
from pre_award.assessment_store.db.models.qa_complete import QaComplete
from pre_award.assessment_store.db.models.score import Score
from pre_award.assessment_store.db.models.tag.tag_types import TagType
from pre_award.assessment_store.db.queries.assessment_records._helpers import derive_application_values
from pre_award.assessment_store.db.queries.scores.queries import (
    _insert_scoring_system,
    insert_scoring_system_for_round_id,
)
from pre_award.assessment_store.db.queries.tags.queries import insert_tags
from pre_award.assessment_store.db.schemas.schemas import TagSchema, TagTypeSchema
from pre_award.config import Config
from pre_award.db import db

with open("tests/pre_award/assessment_store_tests/test_data/hand-crafted-apps.json", "r") as f:
    test_input_data = json.load(f)
with open("tests/pre_award/assessment_store_tests/test_data/ctdf-application.json", "r") as f:
    ctdf_input_data = json.load(f)


@pytest.fixture
def ctdf_application():
    yield copy.deepcopy(ctdf_input_data)


def bulk_insert_application_record(
    application_json_strings: List[str],
    application_type: str = "",
    is_json=False,
) -> List[AssessmentRecord]:
    """bulk_insert_application_record Given a list of json strings and an
    `application_type` we extract key values from the json strings before
    inserting them with the remaining values into `db.models.AssessmentRecord`.

    :param application_json_strings: _description_
    :param application_type: _description_

    """
    print("Beginning bulk application insert.")
    rows = []
    if len(application_json_strings) < 1:
        print("No new submitted applications found. skipping Import...")
        return rows
    print("\n")
    # Create a list of application ids to track inserted rows
    for single_application_json in application_json_strings:
        if not is_json:
            single_application_json = json.loads(single_application_json)
        if not application_type:
            application_type = fund_round_mapping_config_with_round_id[single_application_json["round_id"]][
                "type_of_application"
            ]

        derived_values = derive_application_values(single_application_json)

        if derived_values["location_json_blob"]["error"]:
            current_app.logger.error(
                "Location key not found or invalid postcode provided for the application: %(short_id)s.",
                dict(short_id=derived_values["short_id"]),
            )

        row = {
            **derived_values,
            "jsonb_blob": single_application_json,
            "type_of_application": application_type,
        }
        try:
            stmt = postgres_insert(AssessmentRecord).values([row])

            upsert_rows_stmt = stmt.on_conflict_do_nothing(index_elements=[AssessmentRecord.application_id]).returning(
                AssessmentRecord.application_id
            )

            print(f"Attempting insert of application {row['application_id']}")
            result = db.session.execute(upsert_rows_stmt)

            # Check if the inserted application is in result
            inserted_application_ids = [item.application_id for item in result]
            if not len(inserted_application_ids):
                print(f"Application id already exist in the database: {row['application_id']}")
            rows.append(row)
            db.session.commit()
            del single_application_json
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error occurred while inserting application {row['application_id']}, error: {e}")
            raise e

    print(f"Inserted application_ids (i.e. application rows) : {[row['application_id'] for row in rows]}")
    return rows


@pytest.fixture(scope="function")
def seed_application_records(request, db):
    """Inserts test assessment_record data into the unit test DB according to
    what's supplied using the marker apps_to_insert.

    Supplies these inserted records back to the requesting test function

    """
    marker = request.node.get_closest_marker("apps_to_insert")
    if marker is None:
        apps = 1
    else:
        apps = marker.args[0]
    marker = request.node.get_closest_marker("unique_fund_round")
    if marker is None:
        unique_fund_round = False
    else:
        unique_fund_round = True

    inserted_applications = []

    random_fund_id = str(uuid4())
    random_round_id = str(uuid4())

    for app in apps:
        app_id = str(uuid4())
        app["id"] = app_id
        if unique_fund_round:
            app["fund_id"] = random_fund_id
            app["round_id"] = random_round_id
        app_flags = []
        if "flags" in app:
            app_flags = app.pop("flags")
        app_tags = []
        if "app_tags" in app:
            app_tags = app.pop("app_tags")
        inserted_application = bulk_insert_application_record([app], "COF", True)[0]
        app["flags"] = app_flags
        app["app_tags"] = app_tags
        inserted_applications.append(inserted_application)
        for f in app_flags:
            flag_update = FlagUpdate(
                justification=f["justification"],
                user_id=f["user_id"],
                status=f["status"],
                allocation=f["allocation"],
                date_created=f["date_created"],
            )
            assessment_flag = AssessmentFlag(
                application_id=app_id,
                sections_to_flag=f["sections_to_flag"],
                latest_allocation=f["allocation"],
                latest_status=f["status"],
                updates=[flag_update],
                field_ids=[],
                is_change_request=f["is_change_request"],
            )
            db.session.add(assessment_flag)
        for t in app_tags:
            tag = TagAssociation(application_id=app_id, tag_value=t)
            db.session.add(tag)
        db.session.commit()
    # Supplied the rows we inserted for tests to use in their actions
    yield inserted_applications

    AllocationAssociation.query.delete()
    FlagUpdate.query.delete()
    AssessmentFlag.query.delete()
    TagAssociation.query.delete()
    Score.query.delete()
    QaComplete.query.delete()
    CommentsUpdate.query.delete()
    Comment.query.delete()
    AssessmentRecord.query.delete()
    db.session.commit()


@pytest.fixture(scope="function")
def seed_tags(
    request,
    app,
    db,
    get_tag_types,
):
    tag_type_ids = [t["id"] for t in get_tag_types]
    tags_correct_format = [
        {
            "value": "Test tag 1",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
        {
            "value": "Test tag 2",
            "creator_user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93",
            "tag_type_id": random.choice(tag_type_ids),
        },
    ]

    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    inserted_tags = insert_tags(tags_correct_format, fund_id_test, round_id_test)
    serialiser = TagSchema()
    serialised_associated_tags = [serialiser.dump(r) for r in inserted_tags]
    yield serialised_associated_tags


@pytest.fixture(scope="function")
def seed_scoring_system(
    request,
    app,
    db,
):
    """Inserts the scoring_systems for each round_id.

    If this is the first run of the tests (before any data clearing),
    the default (pre-loaded as part of the db migrations) scoring_system
    information might still be present. To avoid FK issues we make sure
    these rows are removed first.

    """

    one_to_five_scoring_system_id = _insert_scoring_system("OneToFive", 1, 5)["id"]

    scoring_system_for_rounds = [
        {
            "round_id": "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762",
            "scoring_system_id": one_to_five_scoring_system_id,
        },
        {
            "round_id": "6af19a5e-9cae-4f00-9194-cf10d2d7c8a7",
            "scoring_system_id": one_to_five_scoring_system_id,
        },
        {
            "round_id": "888aae3d-7e2c-4523-b9c1-95952b3d1644",
            "scoring_system_id": one_to_five_scoring_system_id,
        },
        {
            "round_id": "0059aad4-5eb5-11ee-8c99-0242ac120002",
            "scoring_system_id": one_to_five_scoring_system_id,
        },
        {
            "round_id": "fc7aa604-989e-4364-98a7-d1234271435a",
            "scoring_system_id": one_to_five_scoring_system_id,
        },
        {
            "round_id": "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
            "scoring_system_id": one_to_five_scoring_system_id,
        },
        {
            "round_id": "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f",
            "scoring_system_id": one_to_five_scoring_system_id,
        },
    ]

    db.session.query(AssessmentRound).delete()
    db.session.commit()

    for scoring_system in scoring_system_for_rounds:
        insert_scoring_system_for_round_id(scoring_system["round_id"], scoring_system["scoring_system_id"])
    yield


@pytest.fixture(scope="function")
def get_tag_types(request, app, db):
    tag_type = TagType(
        id=uuid4(),
        purpose=uuid4(),
        description="Test tag type",
    )

    db.session.add(tag_type)
    db.session.commit()

    tag_types = db.session.query(TagType).all()
    if tag_types:
        serialiser = TagTypeSchema()
        serialised_tag_types = [serialiser.dump(r) for r in tag_types]
        yield serialised_tag_types


class _FlaskClientWithHost(FlaskClient):
    def open(
        self,
        *args: Any,
        buffered: bool = False,
        follow_redirects: bool = False,
        **kwargs: Any,
    ) -> TestResponse:
        if "headers" in kwargs:
            kwargs["headers"].setdefault("Host", Config.API_HOST)
        else:
            kwargs.setdefault("headers", {"Host": Config.API_HOST})
        return super().open(*args, buffered=buffered, follow_redirects=follow_redirects, **kwargs)


@pytest.fixture(scope="function")
def flask_test_client():
    app = create_app()
    app.test_client_class = _FlaskClientWithHost
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def comments_test_account(db):
    user_id = str(uuid4())
    unique_email = f"test-{user_id}@example.com"  # Make email unique
    account = Account(id=user_id, full_name="Test User", email=unique_email)
    db.session.add(account)
    db.session.commit()
    return account


@pytest.fixture
def comments_base_time():
    return datetime(2025, 6, 30, 8, 0, 0)


@pytest.fixture
def comments_data():
    return [
        # Application-level comments (sub_criteria_id=None)
        {"sub_criteria_id": None, "comment_type": CommentType.WHOLE_APPLICATION, "updates": ["App-level 1"]},
        {
            "sub_criteria_id": None,
            "comment_type": CommentType.WHOLE_APPLICATION,
            "updates": ["App-level 2", "App-level 2 update"],
        },
        # Sub-criteria comments
        {"sub_criteria_id": "SC1", "comment_type": CommentType.COMMENT, "updates": ["SC1 comment 1"]},
        {
            "sub_criteria_id": "SC1",
            "comment_type": CommentType.COMMENT,
            "updates": ["SC1 comment 2", "SC1 comment 2 update"],
        },
        {"sub_criteria_id": "SC2", "comment_type": CommentType.COMMENT, "updates": ["SC2 comment 1"]},
        {"sub_criteria_id": "SC2", "comment_type": CommentType.COMMENT, "updates": ["SC2 comment 2"]},
    ]


def create_comment_with_updates(
    db, application_id, user_id, sub_criteria_id, comment_type, update_texts, comments_base_time, account
):
    comment = Comment(
        application_id=application_id,
        user_id=user_id,
        sub_criteria_id=sub_criteria_id,
        comment_type=comment_type,
        date_created=comments_base_time,
    )
    db.session.add(comment)
    db.session.flush()

    updates = []
    for i, text in enumerate(update_texts):
        update = CommentsUpdate(
            comment_id=comment.id,
            comment=text,
            date_created=comments_base_time + timedelta(minutes=i),
        )
        db.session.add(update)
        updates.append(update)
    db.session.commit()
    return comment, updates


@pytest.fixture
def mock_comments_sub_criteria(mocker):
    mock_subcriteria_data = [
        {
            "id": "SC1",
            "name": "Sub Criteria 1",
            "themes": [],
        },
        {
            "id": "SC2",
            "name": "Sub Criteria 2",
            "themes": [],
        },
    ]
    mocker.patch(
        "pre_award.assessment_store.db.queries.comments.queries.get_all_subcriteria", return_value=mock_subcriteria_data
    )
