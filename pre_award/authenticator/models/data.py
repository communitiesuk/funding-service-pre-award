import json
import os
import urllib.parse

import requests
from flask import current_app

from pre_award.authenticator.models.round import Round
from pre_award.common.locale_selector.get_lang import get_lang
from pre_award.config import Config


def api_call(endpoint: str, method: str = "GET", params: dict = None):
    if params:
        params = {k: v for k, v in params.items() if v is not None}
    if endpoint.startswith("http"):
        if method:
            if method == "POST":
                return requests.post(endpoint, json=params)
            elif method == "GET":
                req = requests.PreparedRequest()
                req.prepare_url(endpoint, params)
                return requests.get(req.url)
    else:
        return local_api_call(endpoint, params, method)


def get_data(endpoint: str, params: dict = None):
    if params:
        params = {k: v for k, v in params.items() if v is not None}
    if endpoint.startswith("http"):
        req = requests.PreparedRequest()
        req.prepare_url(endpoint, params)
        response = requests.get(req.url)
        if response.status_code == 200:
            return response.json()
    else:
        return local_api_call(endpoint, params, "get")


def post_data(endpoint: str, params: dict = None):
    if params:
        params = {k: v for k, v in params.items() if v is not None}
    if endpoint.startswith("http"):
        response = requests.post(endpoint, json=params)
        if response.status_code in [200, 201]:
            return response.json()
    else:
        return local_api_call(endpoint, params, "post")


def put_data(endpoint: str, params: dict = None):
    if params:
        params = {k: v for k, v in params.items() if v is not None}
    if endpoint.startswith("http"):
        response = requests.put(endpoint, json=params)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            current_app.logger.error(
                "API error response of: %(response_string)s", dict(response_string=str(response.json()))
            )
    else:
        return local_api_call(endpoint, params, "put")


def local_api_call(endpoint: str, params: dict = None, method: str = "get"):
    api_data_json = os.path.join(
        Config.FLASK_ROOT,
        "tests",
        "pre_award",
        "authenticator_tests",
        "api_data",
        method.lower() + "_endpoint_data.json",
    )
    fp = open(api_data_json)
    api_data = json.load(fp)
    fp.close()
    query_params = "_"
    if params:
        query_params = urllib.parse.urlencode(params)

    if method.lower() in ["post", "put"]:
        if endpoint in api_data:
            post_dict = api_data.get(endpoint)
            if query_params in post_dict:
                return post_dict.get(query_params)
            else:
                return post_dict.get("_default")
    else:
        if params:
            endpoint = f"{endpoint}?{query_params}"

        if endpoint in api_data:
            return api_data.get(endpoint)


def get_round_data(
    fund: str,
    round: str,
    as_dict=False,
):
    url = (Config.GET_ROUND_DATA_FOR_FUND_ENDPOINT).format(fund_id=fund, round_id=round)
    params = {
        "language": get_lang(),
        "use_short_name": True,
    }
    response = get_data(endpoint=url, params=params)
    if not as_dict and response:
        return Round.from_dict(response)
    else:
        return response


def get_account_data(email: str):
    url = Config.ACCOUNT_STORE_API_HOST + "/accounts"
    params = {
        "email_address": email,
    }
    response = get_data(endpoint=url, params=params)
    return response
