from typing import Dict

from flask import request

from pre_award.assessment_store.db.queries.comments import create_comment, get_comments_for_display, update_comment
from pre_award.common.blueprints import Blueprint

assessment_comment_bp = Blueprint("assessment_comment_bp", __name__)


@assessment_comment_bp.get("/comment")
def get_comments() -> Dict:
    application_id = request.args.get("application_id")
    sub_criteria_id = request.args.get("sub_criteria_id")
    theme_id = request.args.get("theme_id")
    comment_id = request.args.get("comment_id")
    comment_type = request.args.get("comment_type")

    comment_metadatas = get_comments_for_display(
        application_id, sub_criteria_id, theme_id, comment_id, comment_type=comment_type
    )

    return comment_metadatas


@assessment_comment_bp.post("/comment")
def post_comments() -> Dict:
    """post_comments Function used by the post endpoint `/comment`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param comment: The comment to be added.
    :param user_id: The stringified user_id UUID.
    :param comment_type: The comment_type.
    :param theme_id: The stringified theme UUID.
    :return: A dictionary.

    """
    args = request.get_json()
    application_id = args["application_id"]
    sub_criteria_id = args["sub_criteria_id"]
    comment = args["comment"]
    comment_type = args["comment_type"]

    user_id = args["user_id"]
    theme_id = args["theme_id"]

    created_comment = create_comment(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        comment=comment,
        comment_type=comment_type,
        user_id=user_id,
        theme_id=theme_id,
    )

    return created_comment


@assessment_comment_bp.put("/comment")
def put_comments() -> Dict:
    """put_comments Function used by the put endpoint `/comment`.

    :param comment: The comment to be updated.
    :param comment_id: The stringified comment_id UUID.
    :return: A dictionary.

    """
    args = request.get_json()
    comment = args["comment"]
    comment_id = args["comment_id"]

    updated_comment = update_comment(
        comment=comment,
        comment_id=comment_id,
    )

    return updated_comment
