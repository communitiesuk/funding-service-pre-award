import pytest

from pre_award.authenticator.models.account import Account, AccountMethods
from pre_award.authenticator.models.fund import Fund
from pre_award.authenticator.models.round import Round
from tests.pre_award.utils import AnyStringMatching

test_user_id = "test_id"
test_user_email = "john@example.com"
test_user_full_name = "John Doe"
azure_ad_subject_id = "test_azure_id"
roles = []


@pytest.fixture(scope="function")
def mock_get_account(mocker, request):
    new_account = request.node.get_closest_marker("new_account")

    mocker.patch(
        "pre_award.authenticator.models.account.AccountMethods.get_account",
        return_value=Account.from_json(
            {
                "account_id": test_user_id,
                "email_address": test_user_email,
                "full_name": test_user_full_name,
                "azure_ad_subject_id": azure_ad_subject_id,
                "roles": roles,
            }
        )
        if not new_account
        else None,
    )
    yield


@pytest.fixture(scope="function")
def mock_create_account(mocker):
    mocker.patch(
        "pre_award.authenticator.models.account.post_data",
        return_value={
            "account_id": test_user_id,
            "email_address": test_user_email,
            "azure_ad_subject_id": azure_ad_subject_id,
        },
    )
    yield


@pytest.fixture(scope="function")
def mock_update_account(mocker):
    mocker.patch(
        "pre_award.authenticator.models.account.put_data",
        return_value={
            "account_id": test_user_id,
            "email_address": "john.Doe@example.com",
            "full_name": test_user_full_name,
            "azure_ad_subject_id": azure_ad_subject_id,
            "roles": ["COF_Lead_Assessor", "NSTF_Lead_Assessor"],
        },
    )
    yield


class TestAccountMethods(object):
    def test_create_or_update_existing_account(self, mock_get_account, mock_update_account):
        result = AccountMethods.create_or_update_account(
            email="john.Doe@example.com",
            azure_ad_subject_id="test_azure_id",
            full_name="John Doe",
            roles=["COF_Lead_Assessor", "NSTF_Lead_Assessor"],
        )
        assert result.id == test_user_id
        assert result.email == "john.Doe@example.com"
        assert result.full_name == test_user_full_name
        assert result.roles == ["COF_Lead_Assessor", "NSTF_Lead_Assessor"]
        assert result.azure_ad_subject_id == azure_ad_subject_id

    @pytest.mark.new_account(True)
    def test_create_or_update_new_account(self, mock_get_account, mock_create_account, mock_update_account):
        result = AccountMethods.create_or_update_account(
            email="john.Doe@example.com",
            azure_ad_subject_id="test_azure_id",
            full_name="John Doe",
            roles=["COF_Lead_Assessor", "NSTF_Lead_Assessor"],
        )
        assert result.id == test_user_id
        assert result.email == "john.Doe@example.com"
        assert result.full_name == test_user_full_name
        assert result.roles == ["COF_Lead_Assessor", "NSTF_Lead_Assessor"]
        assert result.azure_ad_subject_id == azure_ad_subject_id

    def test_create_account(self, mock_create_account):
        result = AccountMethods.create_account(
            email="john@example.com",
        )
        assert result.email == "john@example.com"

    def test_create_magic_link(
        self,
        mocker,
        mock_get_account,
        authenticator_test_client,
        mock_redis_magic_links,
        mock_notification_service_calls,
    ):
        mocker.patch(
            "pre_award.authenticator.models.account.FundMethods.get_fund",
            return_value=Fund(
                name="test fund",
                fund_title="hello",
                short_name="COF",
                identifier="asdfasdf",
                description="asdfasdfasdf",
            ),
        )
        mocker.patch(
            "pre_award.authenticator.models.account.get_round_data", return_value=Round(contact_email="asdf@asdf.com")
        )

        result = AccountMethods.get_magic_link(
            email=test_user_email,
            fund_short_name="COF",
            round_short_name="R1W1",
            govuk_notify_reference="1f829816-b7e5-4cf7-bbbb-1b062e5ee399",
        )
        assert result.endswith("?fund=COF&round=R1W1")
        assert mock_notification_service_calls == [
            mocker.call(
                "john@example.com",
                "02a6d48a-f227-4b9a-9dd7-9e0cf203c8a2",
                personalisation={
                    "name of fund": "test fund",
                    "link to application": AnyStringMatching(
                        r"https://authenticator.communities.gov.localhost:4004/service/magic-links/landing/[A-Za-z]{8}\?fund=COF&round=R1W1"
                    ),
                    "contact details": "asdf@asdf.com",
                    "request new link url": "https://authenticator.communities.gov.localhost:4004/service/magic-links/new?fund=COF&round=R1W1",
                },
                govuk_notify_reference="1f829816-b7e5-4cf7-bbbb-1b062e5ee399",
                email_reply_to_id=None,
            )
        ]
