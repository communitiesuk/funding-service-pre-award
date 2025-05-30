from __future__ import annotations

import json
import random
import string
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, List
from urllib.parse import urljoin

from flask import current_app
from flask_redis import FlaskRedis

from pre_award.authenticator.security.utils import create_token
from pre_award.config import Config

if TYPE_CHECKING:
    from pre_award.authenticator.models.account import Account as Account


@dataclass
class MagicLink:
    account_id: str
    iat: int
    exp: int
    token: str
    link: str
    redirect_url: str
    key: str


class MagicLinkError(Exception):
    """Exception raised for errors in Magic Link management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class MagicLinkMethods(object):
    @property
    def redis_mlinks(self) -> FlaskRedis:
        """
        A FlaskRedis client connection to the magic links redis instance
        :return: FlaskRedis instance
        """
        from app import redis_mlinks

        return redis_mlinks

    @property
    def links(self) -> List:
        """
        All magic link keys as a list, for the search endpoint
        :return: A list of keys from the magic links redis instance
        """
        links = [link.decode("utf-8") for link in self.redis_mlinks.keys("*")]
        return links

    @staticmethod
    def _make_short_key(prefix=None) -> tuple:
        """
        Creates a short string to act as the magic link key
        :return: Random string
        """
        letters = string.ascii_letters
        short_key = "".join(random.choice(letters) for i in range(8))
        if prefix and prefix[-1] != ":":
            prefix = prefix + ":"
        return prefix + short_key, short_key

    @staticmethod
    def _make_link_json(account: Account, redirect_url: str):
        """
        Creates a json dict of minimal link claims and generates a
        signed token of those claims and adds the token as value
        on the returned dict
        :param account: An Account object holding the user's details
        :param redirect_url: String url to redirect to
        :return: A dictionary containing the link claims and signed token
        """
        new_link_json = {
            "accountId": account.id,
            "iat": int(datetime.now().timestamp()),
            "exp": int(
                (
                    datetime.now()
                    + timedelta(
                        seconds=Config.MAGIC_LINK_EXPIRY_SECONDS + 60,
                    )
                ).timestamp()
            ),
            "redirectUrl": redirect_url,
        }
        new_link_json.update({"token": create_token(new_link_json)})
        return new_link_json

    def _set_unique_keyed_record(self, value: str, prefix=None, max_tries: int = 6) -> tuple | None:
        """
        Attempts up to max_tries to save the record with a unique short key
        that doesn't already exist (and returns None if it fails)
        :param value: A string value
        :param prefix: A string key prefix
        :param max_tries: An integer of the maximum tries
        :return: The unique short key for the link hash (or None)
        """
        for _ in range(max_tries):
            prefixed_key, unique_key = self._make_short_key(prefix)
            created = self.redis_mlinks.setex(
                prefixed_key,
                Config.MAGIC_LINK_EXPIRY_SECONDS,
                value,
            )
            if created:
                return prefixed_key, unique_key
        return None

    @staticmethod
    def get_user_record_key(account_id: str):
        return ":".join(
            [
                Config.MAGIC_LINK_USER_PREFIX,
                account_id,
            ]
        )

    def _create_user_record(self, account: Account, link_redis_key: str):
        """
        Creates a record with a key of {MAGIC_LINK_USER_PREFIX}:{account.id}
        with a value of the created magic link redis record key,
        to act as a reference of the link record against the account id
        for management processes, to ensure that only one link can exist
        for a user at any one time
        :param account: Account instance of user
        :param link_redis_key: String of the currently active key
        :return: 1 if successfully created, or 0 if not
        """
        prefixed_user_key = self.get_user_record_key(account.id)
        created = self.redis_mlinks.setex(
            prefixed_user_key,
            Config.MAGIC_LINK_EXPIRY_SECONDS,
            link_redis_key,
        )
        return created

    def clear_existing_user_record(self, account_id: str):
        """
        Checks to see if the account has an existing redis record
        and deletes it and its associated link if so
        :param account_id: Account id of the user
        :return: True if existing link is cleared
        """
        user_record_key = ":".join([Config.MAGIC_LINK_USER_PREFIX, account_id])
        existing_link_key = self.redis_mlinks.get(user_record_key)
        if existing_link_key:
            self.redis_mlinks.delete(existing_link_key)
            self.redis_mlinks.delete(user_record_key)
            return True

    def create_magic_link(
        self,
        account: Account,
        redirect_url: str = None,
        fund_short_name: str = None,
        round_short_name: str = None,
    ) -> dict:
        """
        Creates a new magic link for an account, with an optional redirect_url

        :param account: The account to create a magic link for
        :param redirect_url: (str, optional) An optional redirect_url
        :return:
        """
        current_app.logger.info("Creating magic link for %(account)s", dict(account=account))

        if not redirect_url:
            redirect_url = urljoin(
                Config.APPLICANT_FRONTEND_HOST, f"/account?fund={fund_short_name}&round={round_short_name}"
            )

        new_link_json = self._make_link_json(account, redirect_url)

        redis_key, link_key = self._set_unique_keyed_record(
            json.dumps(new_link_json),
            Config.MAGIC_LINK_RECORD_PREFIX,
        )

        # If link key successfully saved, create user record then return
        if link_key:
            self._create_user_record(account, redis_key)

            if fund_short_name and round_short_name:
                magic_link_url = (
                    Config.AUTHENTICATOR_HOST
                    + Config.MAGIC_LINK_LANDING_PAGE
                    + link_key
                    + "?fund="
                    + fund_short_name
                    + "&round="
                    + round_short_name
                )

            else:
                magic_link_url = Config.AUTHENTICATOR_HOST + Config.MAGIC_LINK_LANDING_PAGE + link_key

            new_link_json.update(
                {
                    "key": link_key,
                    "link": magic_link_url,
                }
            )
            current_app.logger.info("Magic link created for %(account)s", dict(account=account))
            return new_link_json

        current_app.logger.error("Magic link for account %(account)s could not be created", dict(account=account))
        raise MagicLinkError(message="Could not create a magic link")
