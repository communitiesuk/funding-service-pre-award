import io
from datetime import datetime

import pandas as pd
from flask import send_file
from sqlalchemy import String, cast

from pre_award.account_store.db.models.account import Account
from pre_award.application_store.db.models import Applications
from pre_award.assess.services.data_services import get_sub_criteria
from pre_award.assessment_store.db.models.comment import Comment
from pre_award.assessment_store.db.models.comment.comments_update import CommentsUpdate
from pre_award.db import db


def retrieve_all_comments(fund_id, round_id):
    filters = []
    if fund_id:
        filters.append(Applications.fund_id == fund_id)
    if round_id:
        filters.append(Applications.round_id == round_id)

    results = (
        db.session.query(CommentsUpdate, Comment, Applications, Account)
        .join(Comment, CommentsUpdate.comment_id == Comment.id)
        .join(Applications, Comment.application_id == Applications.id)
        .join(Account, Comment.user_id == cast(Account.id, String))
        .filter(*filters)
        .order_by(Comment.application_id, Comment.sub_criteria_id)
        .all()
    )

    # Collect all unique sub_criteria_ids and the first application_id
    sub_criteria_ids = set()
    first_application_id = None
    for _, comment, application, _ in results:
        if comment and comment.sub_criteria_id:
            sub_criteria_ids.add(comment.sub_criteria_id)
            if not first_application_id and application and application.id:
                first_application_id = application.id

    # Build the sub_criteria_id -> name mapping using the first application_id
    sub_criteria_name_map = {}
    for sub_criteria_id in sub_criteria_ids:
        sub_criteria = get_sub_criteria(first_application_id, sub_criteria_id)
        sub_criteria_name_map[sub_criteria_id] = sub_criteria.name if sub_criteria.name else None

    comments_list = []
    for cu, comment, application, commenter_account in results:
        comments_list.append(
            {
                "Application ID": str(comment.application_id) if comment else None,
                "Application reference": application.reference if application else None,
                "Project name": application.project_name if application else None,
                "Date created": cu.date_created.strftime("%d %B %Y, %H:%M") if cu.date_created else None,
                "Comment type": (comment.comment_type.label if comment and comment.comment_type else None),
                "Sub-criteria ID": comment.sub_criteria_id if comment else None,
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
):
    output = io.BytesIO()
    df = pd.DataFrame(comments_list)
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="comments", index=False)
    output.seek(0)

    date_str = datetime.now().strftime("%d-%m-%Y")
    filename = f"comments_export_{fund_short_name.upper()}_{round_short_name.upper()}_{date_str}.xlsx"

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename,
    )
