"""Queries which are performed on the `scores` table.

Joins allowed.

"""

from sqlalchemy import func

from assessment_store.db.models.score import Score
from assessment_store.db.schemas.schemas import ProgressSchema
from db import db


def get_progress_for_app(application_ids=None):
    subq = (
        db.session.query(
            Score.application_id,
            func.count(func.distinct(Score.sub_criteria_id)).label("scored_sub_criterias"),
        )
        .group_by(Score.application_id)
        .subquery()
    )

    results = (
        db.session.query(subq.c.application_id, subq.c.scored_sub_criterias)
        .filter(subq.c.application_id.in_(application_ids))
        .all()
    )

    metadata_serialiser = ProgressSchema()

    progress_metadatas = [
        metadata_serialiser.dump({"application_id": app_id, "scored_sub_criterias": score_count})
        for app_id, score_count in results
    ]

    return progress_metadatas
