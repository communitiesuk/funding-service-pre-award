from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from pre_award.application_store.db.models import Applications
from pre_award.application_store.db.models.application.enums import Status
from pre_award.db import db


def get_unsubmitted_applications_for_round(round_id: UUID) -> Sequence[Applications]:
    return db.session.scalars(
        select(Applications)
        .where(
            Applications.round_id == str(round_id),
            Applications.status.in_([Status.NOT_STARTED, Status.IN_PROGRESS, Status.COMPLETED]),
        )
        .order_by(Applications.started_at)
    ).all()
