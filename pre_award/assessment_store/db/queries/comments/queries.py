"""Queries which are performed on the `comments` table."""

import io
from collections import defaultdict
from datetime import datetime

import pandas as pd
from flask import send_file
from sqlalchemy import String, and_, cast, nullsfirst, select

from pre_award.account_store.db.models.account import Account
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.models.comment.comments import Comment
from pre_award.assessment_store.db.models.comment.comments_update import CommentsUpdate
from pre_award.assessment_store.db.models.comment.enums import CommentType
from pre_award.assessment_store.services.data_services import get_all_subcriteria
from pre_award.db import db


def get_comments(
    application_id: str = None,
    sub_criteria_id: str = None,
    theme_id: str = None,
    comment_id: str = None,
    comment_type: CommentType = None,
    fund_id: str = None,
    round_id: str = None,
) -> list[dict]:
    """Get comments with all related data. Works for both display and export."""

    # Build the base query
    query = (
        db.session.query(CommentsUpdate, Comment, AssessmentRecord, Account)
        .join(Comment, CommentsUpdate.comment_id == Comment.id)
        .join(AssessmentRecord, Comment.application_id == AssessmentRecord.application_id)
        .join(Account, Comment.user_id == cast(Account.id, String))
        .order_by(Comment.application_id, nullsfirst(Comment.sub_criteria_id), CommentsUpdate.date_created)
    )

    # Apply filters
    filters = []
    if comment_id:
        filters.append(Comment.id == comment_id)
    elif application_id:
        filters.append(Comment.application_id == application_id)
        if sub_criteria_id:
            filters.append(Comment.sub_criteria_id == sub_criteria_id)
        if theme_id:
            filters.append(Comment.theme_id == theme_id)

    if comment_type:
        filters.append(Comment.comment_type == comment_type)
    if fund_id:
        filters.append(AssessmentRecord.fund_id == fund_id)
    if round_id:
        filters.append(AssessmentRecord.round_id == round_id)

    if filters:
        query = query.filter(and_(*filters))

    results = query.all()

    # Get sub-criteria names if we have any
    sub_criteria_name_map = {}
    if results and results[0][2]:  # if we have assessment records
        first_record = results[0][2]
        language = first_record.language or "en"
        all_subcriteria = get_all_subcriteria(first_record.fund_id, first_record.round_id, language)
        sub_criteria_name_map = {sc["id"]: sc["name"] for sc in all_subcriteria}

    # Return rich data structure
    return [
        {
            "comment_update_id": cu.id,
            "comment_id": comment.id,
            "application_id": str(comment.application_id),
            "sub_criteria_id": comment.sub_criteria_id,
            "theme_id": comment.theme_id,
            "comment_type": comment.comment_type.name if comment.comment_type else None,
            "comment_text": cu.comment,
            "date_created": cu.date_created,
            "user_id": comment.user_id,
            "user_name": account.full_name,
            "user_email": account.email,
            "application_reference": assessment_record.short_id,
            "project_name": assessment_record.project_name,
            "sub_criteria_name": sub_criteria_name_map.get(comment.sub_criteria_id),
        }
        for cu, comment, assessment_record, account in results
    ]


def format_comments_for_display(comments_data: list[dict]) -> list[dict]:
    """Format comment data for web display - groups updates by comment."""
    comments_by_id = defaultdict(lambda: {"updates": []})

    for item in comments_data:
        comment_id = item["comment_id"]
        if not comments_by_id[comment_id].get("id"):
            # First time seeing this comment - set the main fields
            comments_by_id[comment_id].update(
                {
                    "id": comment_id,
                    "application_id": item["application_id"],
                    "sub_criteria_id": item["sub_criteria_id"],
                    "theme_id": item["theme_id"],
                    "comment_type": item["comment_type"],
                    "user_id": item["user_id"],
                    "date_created": item["date_created"].isoformat() if item["date_created"] else None,
                }
            )

        # Add this update
        comments_by_id[comment_id]["updates"].append(
            {
                "id": item["comment_update_id"],
                "comment": item["comment_text"],
                "date_created": item["date_created"].isoformat() if item["date_created"] else None,
            }
        )

    return list(comments_by_id.values())


def format_comments_for_export(comments_data: list[dict]) -> list[dict]:
    """Format comment data for Excel export - one row per update."""
    return [
        {
            "Application ID": item["application_id"],
            "Application reference": item["application_reference"],
            "Project name": item["project_name"],
            "Date created": item["date_created"].strftime("%d %B %Y, %H:%M") if item["date_created"] else None,
            "Comment type": item["comment_type"],
            "Sub-criteria name": item["sub_criteria_name"],
            "Commenter name": item["user_name"],
            "Commenter email": item["user_email"],
            "Comment": item["comment_text"],
        }
        for item in comments_data
    ]


def create_comment(
    application_id: str, sub_criteria_id: str, comment: str, comment_type: str, user_id: str, theme_id: str
) -> dict:
    """Create a new comment."""
    comment_update = CommentsUpdate(comment=comment)
    comment_obj = Comment(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        comment_type=comment_type,
        user_id=user_id,
        theme_id=theme_id,
        updates=[comment_update],
    )
    db.session.add(comment_obj)
    db.session.commit()
    return format_comments_for_display(get_comments(comment_id=comment_obj.id))[0]


def update_comment(comment: str, comment_id: str) -> dict:
    """Update an existing comment."""
    stmt = select(Comment).where(Comment.id == comment_id)
    comment_to_update = db.session.scalars(stmt).one()
    comment_update = CommentsUpdate(comment_id=comment_id, comment=comment)
    comment_to_update.updates.append(comment_update)
    db.session.add(comment_to_update)
    db.session.commit()
    return format_comments_for_display(get_comments(comment_id=comment_id))[0]


def get_sub_criteria_to_has_comment_map(application_id: str) -> dict[str, bool]:
    """Get a mapping of sub_criteria_id to whether it has comments."""
    stmt = select(Comment.sub_criteria_id).where(Comment.application_id == application_id).distinct()
    result = db.session.execute(stmt).fetchall()
    sub_criteria_to_has_comment_map = defaultdict(lambda: False)
    for (sub_criteria_id,) in result:
        sub_criteria_to_has_comment_map[sub_criteria_id] = True
    return sub_criteria_to_has_comment_map


def export_comments_to_excel(
    comments_list: list[dict], fund_short_name: str, round_short_name: str, application_id: str | None = None
):
    """Export comments to Excel format."""
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

    if not comments_list:
        df = pd.DataFrame(columns=columns)
    else:
        df = pd.DataFrame(comments_list, columns=columns)

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="comments", index=False)
    output.seek(0)

    date_str = datetime.now().strftime("%d-%m-%Y")
    if application_id:
        filename = f"comments_export_{fund_short_name.upper()}_{round_short_name.upper()}_Application_ID_{application_id}_{date_str}.xlsx"  # noqa: E501
    else:
        filename = f"comments_export_{fund_short_name.upper()}_{round_short_name.upper()}_{date_str}.xlsx"

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename,
    )


def get_comments_for_display(
    application_id=None, sub_criteria_id=None, theme_id=None, comment_id=None, comment_type=None
):
    """Get comments formatted for display."""
    raw_data = get_comments(application_id, sub_criteria_id, theme_id, comment_id, comment_type)
    return format_comments_for_display(raw_data)


def get_comments_for_export(fund_id, round_id, application_id=None):
    """Get comments formatted for export."""
    raw_data = get_comments(fund_id=fund_id, round_id=round_id, application_id=application_id)
    return format_comments_for_export(raw_data)
