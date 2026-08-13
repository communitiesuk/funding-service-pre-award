import uuid
from datetime import datetime, timedelta

import pytest

from data.models import Fund, Round
from pre_award.application_store.db.models import Applications, Eligibility, EndOfApplicationSurveyFeedback, Feedback
from pre_award.application_store.db.models.application.enums import Status
from pre_award.application_store.db.models.forms.forms import Forms
from pre_award.application_store.db.models.research.research import ResearchSurvey
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.db import FundingType


@pytest.fixture()
def make_fund_round(app, db):
    """
    Creates a real Fund + Round row so that data.crud.fund_round_queries.get_round(fund_short_name,
    round_short_name) - the lookup the PII deletion script depends on - can find it. Round.opens must
    be in the past for Round.is_not_yet_open to evaluate to False in SQL (a NULL opens value would
    make that comparison NULL, not False, and the round would never be found).
    """

    def _make(
        fund_short_name: str,
        round_short_name: str,
        deadline: datetime,
        pii_deleted_for_applications=None,
    ) -> Round:
        # Fund.short_name is globally unique and this fixture is called from many tests sharing the
        # same test DB (no per-test transaction rollback), so reuse an existing fund with this
        # short_name rather than always inserting a new one.
        fund = db.session.query(Fund).filter(Fund.short_name == fund_short_name).one_or_none()
        if fund is None:
            fund = Fund(
                id=uuid.uuid4(),
                name_json={"en": "Test fund"},
                title_json={"en": "Test fund"},
                short_name=fund_short_name,
                description_json={"en": "Test fund"},
                welsh_available=False,
                owner_organisation_name="Test department",
                owner_organisation_shortname="TD",
                owner_organisation_logo_uri=None,
                funding_type=FundingType.COMPETITIVE,
            )
            db.session.add(fund)
            db.session.commit()

        round_obj = Round(
            id=uuid.uuid4(),
            fund_id=fund.id,
            title_json={"en": "Test round"},
            short_name=round_short_name,
            opens=datetime.now() - timedelta(days=365),
            deadline=deadline,
            prospectus="http://example.com/prospectus",
            privacy_notice="http://example.com/privacy",
            project_name_field_id="project_name_field",
            pii_deleted_for_applications=pii_deleted_for_applications,
        )
        db.session.add(fund)
        db.session.add(round_obj)
        db.session.commit()
        return round_obj

    return _make


@pytest.fixture()
def make_application(app, db):
    """
    Directly constructs an Applications row (plus a form, and one row in each of the
    application-store PII child tables: Feedback, Eligibility, ResearchSurvey,
    EndOfApplicationSurveyFeedback) linked to it by application_id. Bypasses the HTTP-backed
    create_application()/add_new_forms() query helpers (which require mocking an external fund/round
    service) since Applications/Forms are plain declarative models we can populate directly.
    """

    def _make(round_obj: Round, status: Status, project_name: str = "Test Org") -> Applications:
        application = Applications(
            id=uuid.uuid4(),
            account_id=str(uuid.uuid4()),
            fund_id=str(round_obj.fund_id),
            round_id=str(round_obj.id),
            key=str(uuid.uuid4())[:8],
            language="en",
            reference=f"TEST-{uuid.uuid4()}",
            project_name=project_name,
            status=status,
            is_deleted=False,
        )
        db.session.add(application)
        db.session.commit()

        db.session.add(Forms(application_id=application.id, json=[{"some": "answer"}], name="a-form"))
        db.session.add(
            Feedback(
                application_id=application.id,
                fund_id=str(round_obj.fund_id),
                round_id=str(round_obj.id),
                section_id="section-1",
                feedback_json={"comment": "some feedback"},
            )
        )
        db.session.add(
            Eligibility(
                form_id="eligibility-form",
                answers={"question": "answer"},
                eligible=True,
                application_id=application.id,
            )
        )
        db.session.add(
            ResearchSurvey(
                application_id=application.id,
                fund_id=str(round_obj.fund_id),
                round_id=str(round_obj.id),
                data={"survey": "answer"},
            )
        )
        db.session.add(
            EndOfApplicationSurveyFeedback(
                application_id=application.id,
                fund_id=str(round_obj.fund_id),
                round_id=str(round_obj.id),
                page_number=1,
                data={"more_detail": "some detail"},
            )
        )
        db.session.commit()
        return application

    return _make


@pytest.fixture()
def make_assessment_record(app, db):
    def _make(application: Applications, round_obj: Round) -> AssessmentRecord:
        assessment_record = AssessmentRecord(
            application_id=str(application.id),
            short_id="A123",
            type_of_application="test",
            project_name=application.project_name,
            funding_amount_requested=1000.0,
            round_id=round_obj.id,
            fund_id=round_obj.fund_id,
            asset_type="test",
            jsonb_blob={"forms": [{"name": "a-form"}], "project_name": application.project_name},
            location_json_blob={"postcode": "AB1 2CD"},
        )
        db.session.add(assessment_record)
        db.session.commit()
        return assessment_record

    return _make
