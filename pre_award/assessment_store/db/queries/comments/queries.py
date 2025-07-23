"""Queries which are performed on the `scores` table.

Joins allowed.

"""

import io
from collections import defaultdict
from datetime import datetime
from typing import Dict

import pandas as pd
from flask import send_file
from sqlalchemy import String, and_, cast, nullsfirst, select

from pre_award.account_store.db.models.account import Account
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.models.comment.comments import Comment
from pre_award.assessment_store.db.models.comment.comments_update import CommentsUpdate
from pre_award.assessment_store.db.models.comment.enums import CommentType
from pre_award.assessment_store.db.schemas import CommentMetadata
from pre_award.assessment_store.services.data_services import get_all_subcriteria
from pre_award.db import db


def get_comments_from_db(
    application_id: str = None,
    sub_criteria_id: str = None,
    theme_id: str = None,
    comment_id: str = None,
    comment_type: CommentType = None,
) -> list[dict]:
    """Retrieve comments based on provided criteria.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param theme_id: Optional theme_id, if not supplied returns all
        comments for subcriteria.
    :param comment_id: The stringified comment UUID.
    :return: List of dictionaries representing comments.

    """
    # Create a base query to retrieve Comment objects ordered by date_created
    query = db.session.query(Comment).order_by(Comment.date_created.desc())
    filters = []

    if comment_id:
        # Filter the query to retrieve only the comment with the given comment_id
        filters.append(Comment.id == comment_id)
    elif application_id:
        filters.append(Comment.application_id == application_id)
        if sub_criteria_id:
            filters.append(Comment.sub_criteria_id == sub_criteria_id)
        if theme_id:
            filters.append(Comment.theme_id == theme_id)

    if comment_type:
        filters.append(Comment.comment_type == comment_type)

    # Combine multiple filters using logical AND using the `and_` function from SQLAlchemy
    query = query.filter(and_(*filters))

    comment_rows = query.all()
    metadata_serializer = CommentMetadata()
    comment_metadatas = [metadata_serializer.dump(comment_row) for comment_row in comment_rows]

    return comment_metadatas


def create_comment(
    application_id: str,
    sub_criteria_id: str,
    comment: str,
    comment_type: str,
    user_id: str,
    theme_id: str,
) -> Dict:
    """create_comment_for_application_sub_crit executes a query on comments which
    creates a comment for the given application_id and sub_criteria_id.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param comment: The comment string.
    :param comment_type: The type of comment for ENUM.
    :param date_created: The date_created.
    :param user_id: The stringified user_id.
    :return: dictionary.

    """
    comment_update = CommentsUpdate(comment=comment)

    comment = Comment(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        comment_type=comment_type,
        user_id=user_id,
        theme_id=theme_id,
        updates=[comment_update],
    )
    db.session.add(comment)
    db.session.commit()
    metadata_serialiser = CommentMetadata()
    comment_metadata = metadata_serialiser.dump(comment)

    return comment_metadata


def update_comment(
    comment: str,
    comment_id: str,
) -> Dict:
    """update_comment executes a query on comments which updates a comment for the
    given comment id.

    :param comment: The comment string.
    :param comment_id: The comment id.
    :return: dictionary.

    """
    stmt = select(Comment).where(Comment.id == comment_id)
    comment_to_update = db.session.scalars(stmt).one()

    comment_update = CommentsUpdate(comment_id=comment_id, comment=comment)
    comment_to_update.updates.append(comment_update)

    db.session.add(comment_to_update)
    db.session.commit()
    metadata_serialiser = CommentMetadata()
    comment_metadata = metadata_serialiser.dump(comment_to_update)

    return comment_metadata


def get_sub_criteria_to_has_comment_map(application_id: str) -> dict:
    stmt = (
        select(Comment.sub_criteria_id).select_from(Comment).where(Comment.application_id == application_id).distinct()
    )

    result = db.session.execute(stmt).fetchall()

    sub_criteria_to_has_comment_map = defaultdict(lambda: False)
    for (sub_criteria_id,) in result:
        sub_criteria_to_has_comment_map[sub_criteria_id] = True

    return sub_criteria_to_has_comment_map


def retrieve_all_comments(fund_id, round_id, application_id=None):
    filters = []
    if fund_id:
        filters.append(AssessmentRecord.fund_id == fund_id)
    if round_id:
        filters.append(AssessmentRecord.round_id == round_id)
    if application_id:
        filters.append(AssessmentRecord.application_id == application_id)

    results = (
        db.session.query(CommentsUpdate, Comment, AssessmentRecord, Account)
        .join(Comment, CommentsUpdate.comment_id == Comment.id)
        .join(AssessmentRecord, Comment.application_id == AssessmentRecord.application_id)
        .join(Account, Comment.user_id == cast(Account.id, String))
        .filter(*filters)
        .order_by(Comment.application_id, nullsfirst(Comment.sub_criteria_id), CommentsUpdate.date_created)
        .all()
    )

    # Collect all unique sub_criteria_ids and the first assessment record
    sub_criteria_ids = set()
    first_assessment_record: AssessmentRecord = None
    for _, comment, assessment_record, _ in results:
        if comment and comment.sub_criteria_id:
            sub_criteria_ids.add(comment.sub_criteria_id)
            if not first_assessment_record and assessment_record:
                first_assessment_record = assessment_record

    # Build the sub_criteria_id -> name mapping using the first assessment record
    sub_criteria_name_map = {}
    if sub_criteria_ids and first_assessment_record:
        language = first_assessment_record.language if first_assessment_record.language else "en"
        all_subcriteria = get_all_subcriteria(
            first_assessment_record.fund_id, first_assessment_record.round_id, language
        )
        sub_criteria_name_map = {
            sub_criteria["id"]: sub_criteria["name"]
            for sub_criteria in all_subcriteria
            if sub_criteria["id"] in sub_criteria_ids
        }

    comments_list = build_comments_list(results, sub_criteria_name_map)

    return comments_list


def build_comments_list(results, sub_criteria_name_map):
    """Build a list of comment dictionaries from query results."""
    comments_list = []
    for cu, comment, assessment_record, commenter_account in results:
        comments_list.append(
            {
                "Application ID": str(comment.application_id) if comment else None,
                "Application reference": assessment_record.short_id if assessment_record else None,
                "Project name": assessment_record.project_name if assessment_record else None,
                "Date created": cu.date_created.strftime("%d %B %Y, %H:%M") if cu.date_created else None,
                "Comment type": (comment.comment_type.label if comment and comment.comment_type else None),
                "Sub-criteria name": sub_criteria_name_map.get(comment.sub_criteria_id)
                if comment and comment.sub_criteria_id
                else None,
                "Commenter name": commenter_account.full_name if commenter_account else None,
                "Commenter email": commenter_account.email if commenter_account else None,
                "Comment": cu.comment,
            }
        )
    return comments_list


def export_comments_to_excel(
    comments_list,
    fund_short_name,
    round_short_name,
    application_id=None,
):
    output = io.BytesIO()

    columns = [
        "Application ID",
        "Application reference",
        "Project name",
        "Date created",
        "Comment type",
        "Sub-criteria name",
        "Commenter name",
        "Commenter email",
        "Comment",
    ]

    # If comments_list is empty, create an empty DataFrame with columns
    if not comments_list:
        df = pd.DataFrame(columns=columns)
    else:
        df = pd.DataFrame(comments_list, columns=columns)
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="comments", index=False)
    output.seek(0)

    date_str = datetime.now().strftime("%d-%m-%Y")
    if application_id:
        filename = (
            f"comments_export_{fund_short_name.upper()}_{round_short_name.upper()}"
            f"_Application_ID_{application_id}_{date_str}.xlsx"
        )
    else:
        filename = f"comments_export_{fund_short_name.upper()}_{round_short_name.upper()}_{date_str}.xlsx"
    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename,
    )
