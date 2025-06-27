import io

import pandas as pd
from flask import send_file

from pre_award.application_store.db.models import Applications
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
        db.session.query(CommentsUpdate, Comment)
        .join(Comment, CommentsUpdate.comment_id == Comment.id)
        .join(Applications, Comment.application_id == Applications.id)
        .filter(*filters)
        .all()
    )

    comments_list = []
    for cu, comment in results:
        comments_list.append(
            {
                "comments_update_id": str(cu.id),
                "comment_id": str(cu.comment_id),
                "comment": cu.comment,
                "date_created": cu.date_created.strftime("%d %B %Y, %H:%M") if cu.date_created else None,
                "application_id": str(comment.application_id) if comment else None,
                # "comment_type": str(comment.comment_type) if comment and comment.comment_type else None,
                "comment_type": (comment.comment_type.label if comment and comment.comment_type else None),
                "sub_criteria_id": comment.sub_criteria_id if comment else None,
                "theme_id": comment.theme_id if comment else None,
                "user_id": comment.user_id if comment else None,
            }
        )

    return comments_list


def export_comments_to_excel(comments_list, filename="comments_export.xlsx"):
    output = io.BytesIO()
    df = pd.DataFrame(comments_list)
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="comments", index=False)
    output.seek(0)

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename,
    )
