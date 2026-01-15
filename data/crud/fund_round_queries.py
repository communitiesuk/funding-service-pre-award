from datetime import datetime, timedelta
from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import contains_eager

from data.models import Fund, Round
from pre_award.db import db
from pre_award.fund_store.db.models.event import Event, EventType


def get_fund(fund_short_name: str) -> Fund | None:
    return db.session.scalar(select(Fund).where(Fund.short_name == fund_short_name))


def get_funds_with_rounds() -> Sequence[Fund]:
    return db.session.scalars(select(Fund).join(Fund.rounds).options(contains_eager(Fund.rounds))).unique().all()


def get_round(fund_short_name: str, round_short_name: str) -> Round | None:
    round = db.session.scalar(
        select(Round)
        .join(Fund)
        .options(contains_eager(Round.fund))
        .where(Fund.short_name == fund_short_name)
        .where(Round.short_name == round_short_name)
        .where(Round.is_not_yet_open.is_(False))
    )
    return round


def get_rounds_for_application_deadline_reminders() -> Sequence[Round]:
    """
    Retrieve rounds that are eligible for sending application deadline reminder emails "now".

    `round.reminder_date` and `round.deadline` are naive timestamps in Europe/London local time. `func.now()` by
    default returns a UTC timestamp from postgres, so in order to do a correct comparison we need to tell postgres
    that the reminder_date is actually in the europe/london timezone.
    """
    return db.session.scalars(
        select(Round)
        .join(Round.fund)
        .where(
            Round.application_reminder_sent.is_(False),
            Round.send_deadline_reminder_emails.is_(True),
            func.timezone("Europe/London", Round.reminder_date) <= func.now(),
            func.timezone("Europe/London", Round.deadline) > func.now(),
        )
    ).all()


def set_application_reminder_sent(round: Round) -> None:
    round.application_reminder_sent = True
    db.session.commit()


def get_rounds_for_incomplete_application_emails() -> Sequence[Round]:
    """
    Retrieve rounds that have passed their deadline, have not yet had an event
    created for sending incomplete applications, and have 'send_incomplete_application_emails' enabled.
    """
    now = datetime.now()
    one_month_ago = now - timedelta(days=30)

    rounds = (
        db.session.query(Round)
        .filter(
            Round.deadline < now,
            Round.deadline >= one_month_ago,
            Round.send_incomplete_application_emails.is_(True),
            Round.id.notin_(
                select(Event.round_id).filter(
                    Event.type == EventType.SEND_INCOMPLETE_APPLICATIONS, Event.processed.isnot(None)
                )
            ),
        )
        .all()
    )

    return rounds


def create_event(round_id: UUID, event_type: EventType, activation_date: datetime, is_processed: bool) -> None:
    event = Event(round_id=round_id, type=event_type, activation_date=activation_date)
    if is_processed:
        event.processed = datetime.now()  # type: ignore
    db.session.add(event)
    db.session.commit()
