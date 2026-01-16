import random
import string
import uuid
from datetime import datetime

from data.models import Fund, Round
from pre_award.account_store.db.models import Account
from pre_award.application_store.db.models import Applications
from pre_award.application_store.db.models.application.enums import Language
from pre_award.db import FundingType


def seed_fund(session, **kwargs):
    fund_kwargs = (
        dict(
            name_json={"en": "test fund"},
            title_json={},
            short_name="fund",
            description_json={},
            owner_organisation_name="",
            owner_organisation_shortname="",
            owner_organisation_logo_uri="",
            funding_type=FundingType.COMPETITIVE,
        )
        | kwargs
    )

    fund = Fund(**fund_kwargs)
    session.add(fund)
    session.flush()

    return fund


def seed_round(session, fund, send_incomplete_application_emails, send_deadline_reminder_emails, **kwargs):
    round_kwargs = (
        dict(
            fund_id=fund.id,
            title_json={"en": "round"},
            short_name="round1",
            opens=datetime(2020, 1, 1),
            reminder_date=datetime(2020, 2, 1),
            deadline=datetime(2020, 2, 29),
            assessment_start=datetime(2020, 3, 1),
            assessment_deadline=datetime(2020, 3, 31),
            application_reminder_sent=False,
            send_incomplete_application_emails=send_incomplete_application_emails,
            send_deadline_reminder_emails=send_deadline_reminder_emails,
            prospectus="",
            privacy_notice="",
            project_name_field_id="",
        )
        | kwargs
    )

    round = Round(**round_kwargs)
    session.add(round)
    session.flush()

    return round


def seed_application(session, fund, round, account, **kwargs):
    application_kwargs = (
        dict(
            fund_id=fund.id,
            round_id=round.id,
            account_id=account.id,
            key="".join(random.choices(string.ascii_uppercase, k=8)),
            language=Language.en,
            reference="".join(random.choices(string.ascii_uppercase, k=8)),
        )
        | kwargs
    )

    application = Applications(**application_kwargs)
    session.add(application)
    session.flush()

    return application


def seed_account(session, **kwargs):
    name = "".join(random.choices(string.ascii_uppercase, k=8))
    account_kwargs = (
        dict(
            email=f"{name}@test.communities.gov.uk",
            full_name=name,
            azure_ad_subject_id=uuid.uuid4(),
            roles=[],
        )
        | kwargs
    )
    account = Account(**account_kwargs)

    session.add(account)
    session.flush()

    return account
