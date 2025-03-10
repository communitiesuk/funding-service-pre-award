from typing import List, Sequence
from uuid import UUID

from sqlalchemy import select

from pre_award.application_store.db.models import Applications
from pre_award.application_store.db.models.application.enums import Status
from pre_award.db import db


def get_applications_for_round_by_status(round_id: UUID, statuses: List[Status]) -> Sequence[Applications]:
    return db.session.scalars(
        select(Applications)
        .where(
            Applications.round_id == str(round_id),
            Applications.status.in_(statuses),
        )
        .order_by(Applications.started_at)
    ).all()
