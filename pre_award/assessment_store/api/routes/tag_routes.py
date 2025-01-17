from distutils.util import strtobool

from flask import Response, abort, current_app, request

from assessment_store.db.queries.assessment_records.queries import (
    associate_assessment_tags,
    select_active_tags_associated_with_assessment,
    select_all_tags_associated_with_application,
)
from assessment_store.db.queries.tags.queries import (
    get_tag_by_id,
    insert_tags,
    select_tags_for_fund_round,
    select_tags_types,
    update_tags,
)
from assessment_store.db.schemas.schemas import (
    JoinedTagAssociationSchema,
    JoinedTagSchema,
    TagAssociationSchema,
    TagSchema,
    TagTypeSchema,
)
from common.blueprints import Blueprint

assessment_tag_bp = Blueprint("assessment_tag_bp", __name__)


@assessment_tag_bp.get("/funds/<fund_id>/rounds/<round_id>/tags")
def get_tags_for_fund_round(
    fund_id,
    round_id,
):
    tag_purpose: str = request.args.get("tag_purpose", "ALL")
    tag_status: bool = (
        bool(strtobool(request.args.get("tag_status", "false"))) if "tag_status" in request.args else None
    )
    search_term: str = request.args.get("search_term", "")
    search_in: str = request.args.get("search_in", None)

    tags = select_tags_for_fund_round(fund_id, round_id, tag_purpose, tag_status, search_term, search_in)

    if tags:
        serialiser = JoinedTagSchema()
        serialised_tags = [serialiser.dump(r) for r in tags]
        return serialised_tags

    return Response(
        response=[],
        status=204,
        headers={"Content-Type": "application/json"},
    )


@assessment_tag_bp.get("/tag_types")
def get_tag_types():
    tag_types = select_tags_types()

    if tag_types:
        serialiser = TagTypeSchema()
        serialised_tag_types = [serialiser.dump(r) for r in tag_types]
        return serialised_tag_types

    return Response(response="No tags types.", status=204)


@assessment_tag_bp.post("/funds/<fund_id>/rounds/<round_id>/tags")
def add_tag_for_fund_round(fund_id, round_id):
    args = request.get_json()
    tag_value = args["value"]
    tag_type_id = args["tag_type_id"]
    creator_user_id = args["creator_user_id"]

    tags = [
        {
            "value": tag_value,
            "tag_type_id": tag_type_id,
            "creator_user_id": creator_user_id,
        }
    ]

    inserted_tags = insert_tags(tags, fund_id, round_id)

    if inserted_tags:
        serialiser = TagSchema()
        serialised_tags = [serialiser.dump(r) for r in inserted_tags]
        return serialised_tags
    current_app.logger.error("Add tags attempt failed for tags: %(tags)s.", dict(tags=tags))
    abort(404)


@assessment_tag_bp.put("/funds/<fund_id>/rounds/<round_id>/tags")
def update_tags_for_fund_round(fund_id, round_id):
    args = request.get_json()

    tags = [
        {
            "id": arg.get("id"),
            "value": arg.get("value"),
            "tag_type_id": arg.get("tag_type_id"),
            "creator_user_id": arg.get("creator_user_id"),
            "active": arg.get("active"),
        }
        for arg in args
    ]

    updated_tags = update_tags(tags, fund_id, round_id)

    if updated_tags:
        serialiser = TagSchema()
        serialised_tags = [serialiser.dump(r) for r in updated_tags]
        return serialised_tags
    current_app.logger.error("Update tags attempt failed for tags: %(tags)s.", dict(tags=tags))
    abort(404)


@assessment_tag_bp.get("/funds/<fund_id>/rounds/<round_id>/tags/<tag_id>")
def get_tag(fund_id, round_id, tag_id):
    tag = get_tag_by_id(fund_id, round_id, tag_id)
    if not tag:
        return abort(404)
    return JoinedTagSchema().dump(tag)


@assessment_tag_bp.put("/application/<application_id>/tag")
def associate_tags_with_assessment(application_id):
    args = request.get_json()
    tags = args
    current_app.logger.info("Associating tag with assessment")
    associated_tags = associate_assessment_tags(application_id, tags)

    if associated_tags:
        serialiser = TagAssociationSchema()
        serialised_associated_tags = [serialiser.dump(r) for r in associated_tags]
        return serialised_associated_tags

    return []


@assessment_tag_bp.get("/application/<application_id>/tag")
def get_active_tags_associated_with_assessment(application_id):
    current_app.logger.info(
        "Getting tags associated with assessment with application_id: %(application_id)s.",
        dict(application_id=application_id),
    )
    associated_tags = select_active_tags_associated_with_assessment(application_id)
    if associated_tags:
        serialiser = JoinedTagAssociationSchema()
        serialised_associated_tags = [serialiser.dump(r) for r in associated_tags]
        return serialised_associated_tags
    return []


@assessment_tag_bp.get("/application/<application_id>/tags")
def get_all_tags_associated_with_application(application_id):
    current_app.logger.info(
        "Getting tags associated with with application_id: %(application_id)s.", dict(application_id=application_id)
    )
    associated_tags = select_all_tags_associated_with_application(application_id)
    if associated_tags:
        serialiser = JoinedTagAssociationSchema()
        serialised_associated_tags = [serialiser.dump(r) for r in associated_tags]
        return serialised_associated_tags
    return []
