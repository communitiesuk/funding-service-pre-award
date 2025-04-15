from datetime import datetime
from typing import cast

from flask import current_app
from invoke import Context, task  # type: ignore[attr-defined]

from app import create_app
from data.crud.accounts import get_account
from data.crud.applications import get_applications_for_round_by_status
from data.crud.fund_round_queries import (
    create_event,
    get_rounds_for_application_deadline_reminders,
    get_rounds_with_passed_deadline,
    set_application_reminder_sent,
)
from pre_award.application_store.db.models.application.enums import Status
from pre_award.application_store.db.queries.application.queries import create_qa_base64file, get_application
from pre_award.fund_store.db.models.event import EventType
from services.notify import NotificationError, get_notification_service


def send_application_deadline_reminders_impl() -> None:
    """
    Sends an email to each account that has one or more incomplete applications for an application round
    that has reminders enabled.
    """
    current_app.logger.info("Starting to send incomplete application reminders")

    rounds_for_reminders = get_rounds_for_application_deadline_reminders()
    for round in rounds_for_reminders:
        incomplete_applications = get_applications_for_round_by_status(
            round.id, [Status.NOT_STARTED, Status.IN_PROGRESS, Status.COMPLETED]
        )
        notified_accounts = set()
        for application in incomplete_applications:
            account_id = str(application.account_id)
            if account_id in notified_accounts:
                continue

            notified_accounts.add(account_id)
            account = get_account(account_id)
            if not account:
                continue

            try:
                notification = get_notification_service().send_application_deadline_reminder_email(
                    email_address=account.email,
                    fund_name=round.fund.name_json["en"],
                    round_name=round.title_json["en"],
                    deadline=cast(datetime, round.deadline),
                    contact_help_email=round.contact_email,
                )
                current_app.logger.info(
                    "Sent notification %(notification_id)s to %(account_id)s",
                    dict(notification_id=notification.id, account_id=account.id),
                )
            except NotificationError:
                current_app.logger.exception(
                    (
                        "Error sending application deadline reminder to %(account_id)s "
                        "for fund_id=%(fund_id)s round=%(round_id)s]"
                    ),
                    dict(account_id=account.id, fund_id=round.fund_id, round_id=round.id),
                )

        set_application_reminder_sent(round)
        current_app.logger.info(
            "The application reminder has been sent successfully for %(fund_name)s [%(round_name)s]",
            dict(fund_name=round.fund.name_json["en"], round_name=round.title_json["en"]),
        )

    current_app.logger.info("Finished sending incomplete application reminders")


@task
def send_application_deadline_reminders(c: Context) -> None:
    app = create_app()
    with app.app_context():
        send_application_deadline_reminders_impl()


def send_incomplete_application_emails_impl() -> None:
    rounds_with_passed_deadline = get_rounds_with_passed_deadline()
    incomplete_statuses = [Status.NOT_STARTED, Status.IN_PROGRESS, Status.COMPLETED]

    for round in rounds_with_passed_deadline:
        applications = get_applications_for_round_by_status(round.id, incomplete_statuses)

        for application in applications:
            application_with_form_json = get_application(application.id, as_json=True, include_forms=True)

            try:
                account_id = str(application.account_id)
                account = get_account(account_id)
                if not account:
                    continue

                application_data = create_qa_base64file(application_with_form_json, True)

                notification = get_notification_service().send_unsubmitted_application_email(
                    email_address=account.email,
                    application_reference=str(application.reference),
                    fund_name=round.fund.name_json["en"],
                    round_name=round.title_json["en"],
                    application_data=application_data,
                    contact_help_email=round.contact_email,
                )
                current_app.logger.info(
                    "Sent incomplete application notification %(notification_id)s to %(account_id)s",
                    dict(notification_id=notification.id, account_id=account_id),
                )
            except NotificationError:
                current_app.logger.exception(
                    (
                        "Error sending incomplete application notification to %(account_id)s "
                        "for fund_id=%(fund_id)s round=%(round_id)s]"
                    ),
                    dict(account_id=account_id, fund_id=round.fund_id, round_id=round.id),
                )
        create_event(round.id, EventType.SEND_INCOMPLETE_APPLICATIONS, datetime.now(), True)


@task
def send_incomplete_application_emails(c: Context) -> None:
    app = create_app()
    with app.app_context():
        send_incomplete_application_emails_impl()
