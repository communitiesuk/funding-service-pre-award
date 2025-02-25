from dataclasses import dataclass
from typing import List

from flask import current_app

from pre_award.authenticator.models.data import get_account_data, get_data, get_round_data, post_data, put_data
from pre_award.authenticator.models.fund import FundMethods
from pre_award.authenticator.models.magic_link import MagicLinkMethods
from pre_award.config import Config
from services.notify import get_notification_service


@dataclass
class Account(object):
    id: str
    email: str
    azure_ad_subject_id: str
    full_name: str
    roles: List[str]

    @staticmethod
    def from_json(data: dict):
        return Account(
            id=data.get("account_id"),
            email=data.get("email_address"),
            azure_ad_subject_id=data.get("azure_ad_subject_id"),
            full_name=data.get("full_name"),
            roles=data.get("roles"),
        )


class AccountError(Exception):
    """Exception raised for errors in Account management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class AccountMethods(Account):
    @staticmethod
    def get_account(email: str = None, account_id: str = None, azure_ad_subject_id=None) -> Account | None:
        """
        Get an account from the account store using either
        an email address or account_id.

        Args:
            email (str, optional): The account email address
            Defaults to None.
            account_id (str, optional): The account id. Defaults to None.
            azure_ad_subject_id (str, optional): The Azure AD subject id.
            Defaults to None.

        Raises:
            TypeError: If both an email address or account id is given,
            a TypeError is raised.

        Returns:
            Account object or None
        """
        if email is account_id is azure_ad_subject_id is None:
            raise TypeError("Requires an email address, azure_ad_subject_id or account_id")

        url = Config.ACCOUNT_STORE_API_HOST + "/accounts"
        params = {
            "email_address": email,
            "azure_ad_subject_id": azure_ad_subject_id,
            "account_id": account_id,
        }
        response = get_data(url, params)

        if response and "account_id" in response:
            return Account.from_json(response)

    @staticmethod
    def update_account(
        id: str,
        email: str,
        azure_ad_subject_id: str,
        full_name: str,
        roles: list[str],
    ) -> Account | None:
        """
        Get an account corresponding to an email_address
        or create a new account if none exists

        Args:
            id (str): The account id to update
            email (str): The user's email address.
            azure_ad_subject_id (str): The user's Azure AD subject id.
            full_name (str): The user's full_name.
            roles (List[str]): Roles to update on the account record.

        Returns:
            Account object or None
        """
        url = Config.ACCOUNT_STORE_API_HOST + "/accounts/{account_id}".format(account_id=id)

        if Config.FLASK_ENV == "development" and not roles:
            account = get_account_data(email)
            roles = account.get("roles")
        params = {
            "email_address": email,
            "azure_ad_subject_id": azure_ad_subject_id,
            "full_name": full_name,
            "roles": roles or [],
        }
        response = put_data(url, params)
        if response and "account_id" in response:
            return Account.from_json(response)

    @staticmethod
    def create_account(email: str) -> Account | None:
        """
        Get an account corresponding to an email_address
        or create a new account if none exists

        Args:
            email (str): The email address we wish
            to create a new account with.

        Returns:
            Account object or None
        """
        url = Config.ACCOUNT_STORE_API_HOST + "/accounts"
        params = {"email_address": email}
        response = post_data(url, params)

        if response and "account_id" in response:
            return Account.from_json(response)
        raise AccountError(message=f"Could not create account for email '{email}'")

    @classmethod
    def create_or_update_account(
        cls,
        email: str,
        azure_ad_subject_id: str,
        full_name: str,
        roles: list[str],
    ):
        # Check to see if account already exists by azure_id or email
        account = AccountMethods.get_account(azure_ad_subject_id=azure_ad_subject_id) or AccountMethods.get_account(
            email=email
        )

        # Create account if it doesn't exist
        if not account:
            account = AccountMethods.create_account(email=email)

        if account.azure_ad_subject_id and account.azure_ad_subject_id != azure_ad_subject_id:
            raise AccountError(
                message=(
                    f"Cannot update account id: {account.id} - attempting to"
                    " update existing azure_ad_subject_id from"
                    f" {account.azure_ad_subject_id} to"
                    f" {azure_ad_subject_id} which is not allowed."
                )
            )

        # Update account with the latest roles, email and name
        account = AccountMethods.update_account(
            id=account.id,
            email=email,
            azure_ad_subject_id=azure_ad_subject_id,
            full_name=full_name,
            roles=roles,
        )

        return account

    @classmethod
    def get_magic_link(
        cls,
        email: str,
        fund_short_name: str = None,
        round_short_name: str = None,
        govuk_notify_reference: str = None,
    ) -> str:
        """
        Create a new magic link for a user
        and send it in a notification
        to their email address
        :param email: The user's account email address
        :param fund_id: The fund id
        :param round_id: The round id
        :return: The authenticator url to use the magic link (landing page)
        """
        account = cls.get_account(email)
        if not account:
            account = cls.create_account(email)
        if account:
            fund = FundMethods.get_fund(fund_short_name)
            round_for_fund = get_round_data(
                fund_short_name,
                round_short_name,
            )

            # Create a fresh link
            new_link_json = MagicLinkMethods().create_magic_link(
                account,
                fund_short_name=fund_short_name if fund_short_name else "",
                round_short_name=round_short_name if round_short_name else "",
            )
            current_app.logger.debug("Magic Link URL: %(link)s", dict(link=new_link_json.get("link")))

            get_notification_service().send_magic_link(
                email_address=account.email,
                magic_link_url=new_link_json.get("link"),
                contact_help_email=round_for_fund.contact_email,
                fund_name=fund.name,
                request_new_link_url=(
                    Config.AUTHENTICATOR_HOST
                    + Config.NEW_LINK_ENDPOINT
                    + "?fund="
                    + fund_short_name
                    + "&round="
                    + round_short_name
                ),
                govuk_notify_reference=govuk_notify_reference,
            )

            return new_link_json.get("link")
        current_app.logger.error(
            "Could not create an account (%(account)s) for email '%(email)s'", dict(account=account, email=email)
        )
        raise AccountError(message="Sorry, we couldn't create an account for this email, please contact support")
