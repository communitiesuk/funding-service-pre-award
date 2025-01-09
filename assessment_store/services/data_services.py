from typing import Dict

import requests
from flask import current_app

from config import Config
from services.notify import NotificationService, get_notification_service  # noqa: E402


def get_data(endpoint: str, payload: Dict = None):
    try:
        if payload:
            current_app.logger.info(
                "Fetching data from '{endpoint}', with payload: {payload}.",
                extra=dict(endpoint=endpoint, payload=payload),
            )
            response = requests.get(endpoint, payload)
        else:
            current_app.logger.info("Fetching data from '{endpoint}'.", extra=dict(endpoint=endpoint))
            response = requests.get(endpoint)
        if response.status_code == 200:
            if "application/json" == response.headers["Content-Type"]:
                return response.json()
            else:
                return response.content
        elif response.status_code == 204:
            current_app.logger.warning(
                "Request successful but no resources returned for endpoint '{endpoint}'.", extra=dict(endpoint=endpoint)
            )
        else:
            current_app.logger.error("Could not get data for endpoint '{endpoint}' ", extra=dict(endpoint=endpoint))
    except requests.exceptions.RequestException:
        current_app.logger.exception("Unable to get_data")


def get_account_data(account_id: str):
    return get_data(
        Config.ACCOUNT_STORE_API_HOST + Config.ACCOUNTS_ENDPOINT,
        {"account_id": account_id},
    )


def get_fund_data(fund_id: str):
    return get_data(Config.FUND_STORE_API_HOST + Config.FUND_ENDPOINT.format(fund_id=fund_id, use_short_name=False))


def create_assessment_url_for_application(application_id: str):
    return Config.ASSESSMENT_FRONTEND_HOST + Config.ASSESSMENT_APPLICATION_ENDPOINT.format(
        application_id=application_id
    )


def send_notification_email_assigned(application, user_id, assigner_id, message=None):
    _send_notification_email(
        application=application,
        user_id=user_id,
        assigner_id=assigner_id,
        message=message,
        template_id=NotificationService.ASSESSMENT_APPLICATION_ASSIGNED,
    )


def send_notification_email_unassigned(application, user_id, assigner_id, message=None):
    _send_notification_email(
        application=application,
        user_id=user_id,
        assigner_id=assigner_id,
        message=message,
        template_id=NotificationService.ASSESSMENT_APPLICATION_UNASSIGNED,
    )


def _send_notification_email(application, user_id, assigner_id, template_id: str, message=None):
    """Sends a notification email to inform the user (specified by user_id) that
    an application has been assigned to them.

    Parameters:
        application (dict): dict of application details for the application that has been assigned
        user_id (str): id of assignee and recipient of email
        assigner_id (str): id of the assigner.
        template_id (str): which template to use
        message (str): Custom message provided by assigner

    """
    user_response = get_account_data(account_id=user_id)
    assigner_response = get_account_data(account_id=assigner_id)
    fund_response = get_fund_data(fund_id=application["fund_id"])

    content = {
        "fund_name": fund_response["name"],
        "reference_number": application["short_id"],
        "project_name": application["project_name"],
        "lead_assessor_email": assigner_response["email_address"],
        "assessment_link": create_assessment_url_for_application(application_id=application["application_id"]),
    }

    content["assignment_message"] = message or ""

    try:
        get_notification_service().send_assessment_email(
            email_address=user_response["email_address"], template_id=template_id, **content
        )
    except Exception as e:
        current_app.logger.error(
            "Could not send assesment email for user: {user_id}, application {application_id}",
            extra=dict(user_id=user_id, application_id=application["application_id"]),
            exc_info=e,
        )


def get_account_name(id: str):
    url = Config.ACCOUNT_STORE_API_HOST + Config.ACCOUNTS_ENDPOINT
    params = {"account_id": id}
    # When developing locally, all comments and scores (etc) are
    # created by the local debug user by default . This user is not seeded
    # in the account store, it is not required as we circumnavigate SSO in assessment frontend.
    if id == "00000000-0000-0000-0000-000000000000":
        return "Local Debug User"
    else:
        response = get_data(url, params)
    return response["full_name"]
