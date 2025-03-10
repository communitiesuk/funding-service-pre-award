from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.db import db


def get_assessments_by_round(round_id: UUID) -> Sequence[AssessmentRecord]:
    return db.session.scalars(
        select(AssessmentRecord).where(
            AssessmentRecord.round_id == round_id,
            AssessmentRecord.is_withdrawn.is_(False),
        )
    ).all()
