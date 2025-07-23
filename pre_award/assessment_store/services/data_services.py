import copy
from typing import Dict

import requests
from flask import abort, current_app

from pre_award.config import Config  # noqa: E402


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


def get_all_subcriteria(fund_id, round_id, language):
    sub_criterias = []
    display_config = copy.deepcopy(Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"])
    for section in display_config["scored_criteria"] + display_config["unscored_sections"]:
        for sub_criteria in section["sub_criteria"]:
            for theme in sub_criteria["themes"]:
                for answer in theme["answers"]:
                    answer["form_name"] = (
                        answer["form_name"][language] if isinstance(answer["form_name"], dict) else answer["form_name"]
                    )
                    if "path" in answer:
                        answer["path"] = (
                            answer["path"][language] if isinstance(answer["path"], dict) else answer["path"]
                        )
            sub_criterias.append(sub_criteria)
    return sub_criterias


def return_subcriteria_from_mapping(sub_criteria_id, fund_id, round_id, language):
    current_app.logger.info(
        "Finding sub criteria data in config for: %(sub_criteria_id)s", dict(sub_criteria_id=sub_criteria_id)
    )
    display_config = copy.deepcopy(Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"])
    sub_criterias = get_all_subcriteria(fund_id, round_id, language)
    matching_sub_criteria = list(
        filter(
            lambda sub_criteria: sub_criteria["id"] == sub_criteria_id,
            sub_criterias,
        )
    )
    if len(matching_sub_criteria) == 1:
        sub_crit = matching_sub_criteria[0]

        is_scored = False
        for criteria in display_config["scored_criteria"]:
            for sub_criteria in criteria["sub_criteria"]:
                if sub_criteria_id == sub_criteria["id"]:
                    is_scored = True
        sub_crit["is_scored"] = is_scored

        return sub_crit
    elif len(matching_sub_criteria) > 1:
        current_app.logger.error(
            "sub_criteria: '%(sub_criteria_id)s' duplicated.", dict(sub_criteria_id=sub_criteria_id)
        )
        raise ValueError(f"sub_criteria: '{sub_criteria_id}' duplicated.")
    else:
        current_app.logger.warning(
            "sub_criteria: '%(sub_criteria_id)s' not found.", dict(sub_criteria_id=sub_criteria_id)
        )
        abort(404, description=f"sub_criteria: '{sub_criteria_id}' not found.")
