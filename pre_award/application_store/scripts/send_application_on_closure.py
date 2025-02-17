#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime
from distutils.util import strtobool

from services.notify import get_notification_service

sys.path.insert(1, ".")

from flask import current_app  # noqa: E402

from app import create_app  # noqa: E402
from pre_award.application_store import external_services  # noqa: E402
from pre_award.application_store.db.queries import (  # noqa: E402
    get_forms_by_app_id,  # noqa: E402
    search_applications,  # noqa: E402
)
from pre_award.application_store.db.queries.application import create_qa_base64file  # noqa: E402
from pre_award.application_store.external_services.data import get_fund  # noqa: E402
from pre_award.config import Config  # noqa: E402


def send_incomplete_applications_after_deadline(
    fund_id,
    round_id,
    single_application=False,
    application_id=None,
    send_email=False,
):
    """
    Retrieves a list of unsubmitted applications and associated form and user data
    for each. Then, it uses the notification service to email the account ID for each application.

    Note:
    - To enable email notifications, set `send_email` to True.
    - To process a single application, set `single_application` to True and provide the `application_id`.

    Args:
    - fund_id (str): The ID of the fund.
    - round_id (str): The ID of the funding round.
    - single_application (bool, optional): Set to True if processing an individual application.
    - send_email (bool): Set to True or False to determine whether to send an email.
    - application_id (str, required if `single_application` is True): The application_id to process.
    """

    fund_rounds = get_fund_round(fund_id, round_id)
    deadline = datetime.strptime(fund_rounds.get("deadline"), "%Y-%m-%dT%H:%M:%S")
    if datetime.now() > deadline:
        fund_data = get_fund(fund_id)
        search_params = {
            "status_only": ["NOT_STARTED", "IN_PROGRESS", "COMPLETED"],
            "fund_id": fund_id,
            "round_id": round_id,
            "application_id": application_id if single_application else None,
        }
        matching_applications = search_applications(**search_params)

        applications_to_send = []
        for application in matching_applications:
            application = {**application, "fund_name": fund_data.name}
            try:
                application["forms"] = get_forms_by_app_id(application.get("id"))
                application["fund_id"] = fund_id
                application["round_name"] = fund_rounds.get("title")
                try:
                    account_id = external_services.get_account(account_id=application.get("account_id"))
                    application["account_email"] = account_id.email
                    application["account_name"] = account_id.full_name
                    applications_to_send.append({"application": application})
                except Exception:
                    handle_error(
                        f"Unable to retrieve account id ({application.get('account_id')}) for "
                        + f"application id {application.get('id')}",
                        send_email,
                    )
            except Exception:
                handle_error(
                    "Unable to retrieve forms for " + f"application id {application.get('id')}",
                    send_email,
                )

        current_app.logger.info(
            "Found %(matching_app_count)s applications with matching"
            " statuses. Retrieved all data for %(apps_to_send_count)s of"
            " them.",
            dict(
                matching_app_count=len(matching_applications),
                apps_to_send_count=len(applications_to_send),
            ),
        )
        if send_email:
            total_applications = len(applications_to_send)
            current_app.logger.info(
                "Send email set to true, will now send %(total_applications)s %(emails)s.",
                dict(
                    total_applications=total_applications,
                    emails="emails" if total_applications > 1 else "email",
                ),
            )
            if total_applications > 0:
                for count, application in enumerate(applications_to_send, start=1):
                    email = {
                        "email": application.get("account_email")  # noqa: B035 needs refactor
                        for application in application.values()
                    }
                    current_app.logger.info(
                        "Sending application %(count)s of %(total_applications)s to %(email)s",
                        dict(
                            count=count,
                            total_applications=total_applications,
                            email=email.get("email"),
                        ),
                    )
                    application["contact_help_email"] = fund_rounds.get("contact_email")
                    application_data = create_qa_base64file(application["application"], True)
                    notification = get_notification_service().send_incomplete_application_email(
                        email.get("email"),
                        fund_name=application_data["fund_name"],
                        application_reference=application_data["reference"],
                        round_name=application_data["round_name"],
                        questions=application_data["questions_file"],
                        contact_help_email=application["contact_help_email"],
                    )
                    current_app.logger.info(
                        "Sent notification %(notification_id)s for application %(application_reference)s",
                        dict(notification_id=notification.id, application_reference=application_data["reference"]),
                    )
                current_app.logger.info(
                    "Sent %(count)s %(emails)s",
                    dict(count=count, emails="emails" if count > 1 else "email"),
                )
                return count
            else:
                current_app.logger.warning("There are no applications to be sent.")
                return 0
        else:
            count = len(applications_to_send)
            current_app.logger.warning(
                "Send email set to false, will not send %(count)s %(emails)s.",
                dict(count=count, emails="emails" if count > 1 else "email"),
            )
            return len(applications_to_send)
    else:
        current_app.logger.warning("Current round is active")
        return -1


def handle_error(msg, throw_on_error):
    current_app.logger.error(msg)
    if throw_on_error:
        raise LookupError(msg)


def get_fund_round(fund_id, round_id):
    return external_services.get_data(
        Config.FUND_STORE_API_HOST + Config.FUND_ROUND_ENDPOINT.format(fund_id=fund_id, round_id=round_id)
    )


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fund_id", help="Provide fund id of a fund", required=True)
    parser.add_argument("--round_id", help="Provide round id of a fund", required=True)
    parser.add_argument(
        "--single_application",
        help="Whether to send just single application: True or False",
        required=True,
    )

    parser.add_argument(
        "--application_id",
        help="Provide application id if single_application is True",
        required=False,
    )
    parser.add_argument(
        "--send_email",
        help="Whether to actually send email: True or False",
        required=True,
    )
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    single_application = (
        strtobool(args.single_application)
        if args.single_application is not None and not isinstance(args.single_application, bool)
        else args.single_application
    )

    if single_application and args.application_id is None:
        error_message = "The application_id argument is required if single_application is True"
        current_app.logger.error(error_message)
        raise ValueError(error_message)

    send_incomplete_applications_after_deadline(
        fund_id=args.fund_id,
        round_id=args.round_id,
        single_application=single_application,
        application_id=args.application_id,
        send_email=strtobool(args.send_email),
    )


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        main()
