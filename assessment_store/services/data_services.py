from typing import Dict

import requests
from flask import current_app

from config import Config


def get_data(endpoint: str, payload: Dict = None):
    try:
        if payload:
            current_app.logger.info(
                "Fetching data from '%(endpoint)s', with payload: %(payload)s.",
                dict(endpoint=endpoint, payload=payload),
            )
            response = requests.get(endpoint, payload)
        else:
            current_app.logger.info("Fetching data from '%(endpoint)s'.", dict(endpoint=endpoint))
            response = requests.get(endpoint)
        if response.status_code == 200:
            if "application/json" == response.headers["Content-Type"]:
                return response.json()
            else:
                return response.content
        elif response.status_code == 204:
            current_app.logger.warning(
                "Request successful but no resources returned for endpoint '%(endpoint)s'.", dict(endpoint=endpoint)
            )
        else:
            current_app.logger.error("Could not get data for endpoint '%(endpoint)s' ", dict(endpoint=endpoint))
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
