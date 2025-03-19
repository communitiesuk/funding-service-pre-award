import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import contains_eager

from data.models import Fund, Round
from pre_award.application_store.db.models.application.applications import Applications
from pre_award.application_store.db.models.application.enums import Status
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
            func.timezone("Europe/London", Round.reminder_date) <= func.now(),
            func.timezone("Europe/London", Round.deadline) > func.now(),
        )
    ).all()


def set_application_reminder_sent(round: Round) -> None:
    round.application_reminder_sent = True
    db.session.commit()


def get_rounds_with_passed_deadline() -> Sequence[Round]:
    """
    Retrieve rounds that have passed their deadline but have not yet had an event
    created for sending incomplete applications.
    """
    now = datetime.now()
    one_month_ago = now - timedelta(days=30)

    rounds_with_passed_deadline = (
        db.session.query(Round).filter(Round.deadline < now, Round.deadline >= one_month_ago).all()
    )

    rounds_without_event = [
        round
        for round in rounds_with_passed_deadline
        if not db.session.query(Event)
        .filter(Event.round_id == round.id, Event.type == EventType.SEND_INCOMPLETE_APPLICATIONS)
        .first()
    ]

    return rounds_without_event


def get_passed_round_applications(round: Round) -> Sequence[Applications]:
    """
    Retrieve applications for the given round_ids where the status is
    in ["NOT_STARTED", "IN_PROGRESS", "COMPLETED"].
    """
    applications = (
        db.session.query(Applications)
        .filter(
            Applications.round_id == str(round.id),
            Applications.status.in_([Status.NOT_STARTED, Status.IN_PROGRESS, Status.COMPLETED]),
        )
        .all()
    )
    return applications


def extract_questions_and_answers(data_list: List[Dict[str, Any]]) -> str:
    """
    Function to build a string of questions and answers of application forms
    """
    result = []
    for data in data_list:
        for question in data["questions"]:
            if question["category"] == "FabDefault":
                for field in question["fields"]:
                    question_text = field["title"]
                    answer = field["answer"]
                    if isinstance(answer, str):
                        answer = strip_html_tags(answer)
                    result.append(f"{question_text}: {answer}")
    return ",\n".join(result)


def strip_html_tags(text: str) -> str:
    """Remove HTML tags from a string."""
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


def create_event(round_id: UUID, event_type: EventType, activation_date: datetime) -> None:
    event = Event(round_id=round_id, type=event_type, activation_date=activation_date)
    db.session.add(event)
    db.session.commit()
