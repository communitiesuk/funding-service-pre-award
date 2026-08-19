import pytest
from sqlalchemy.orm import scoped_session, sessionmaker

from pre_award.application_store.db.models import Applications, Eligibility, EndOfApplicationSurveyFeedback, Feedback
from pre_award.application_store.db.models.forms.forms import Forms
from pre_award.application_store.db.models.research.research import ResearchSurvey
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from tests.integration.seeding import seed_account, seed_application, seed_fund, seed_round


@pytest.fixture(autouse=True)
def session(db):
    """
    Wrap each test in its own DB transaction (via a savepoint) that's rolled back afterwards, matching
    the pattern already used in tests/integration/conftest.py. Without this, every test in this
    directory shares one long-lived session against the same test DB with no isolation between tests.
    """
    old_session = db.session

    connection = db.engine.connect()
    transaction = connection.begin()

    db.session = session = scoped_session(
        session_factory=sessionmaker(bind=connection, join_transaction_mode="create_savepoint")
    )

    try:
        yield session
    finally:
        session.remove()
        transaction.rollback()
        connection.close()

    db.session = old_session


@pytest.fixture
def make_fund_round(app, db, session):
    """
    Creates a real Fund + Round row so that data.crud.fund_round_queries.get_round(fund_short_name,
    round_short_name) - the lookup the PII deletion script depends on - can find it. Round.opens must
    be in the past for Round.is_not_yet_open to evaluate to False in SQL (a NULL opens value would
    make that comparison NULL, not False, and the round would never be found) - seed_round's default
    opens=datetime(2020, 1, 1) already satisfies this.
    """

    def _make(fund_short_name, round_short_name, deadline, pii_deleted_for_applications=None):
        fund = seed_fund(session, short_name=fund_short_name)
        round_obj = seed_round(
            session,
            fund,
            send_incomplete_application_emails=True,
            send_deadline_reminder_emails=True,
            short_name=round_short_name,
            deadline=deadline,
            pii_deleted_for_applications=pii_deleted_for_applications,
        )
        # seed_fund/seed_round only flush (send the INSERTs, don't commit). Under the savepoint-backed
        # `session` fixture above, an uncommitted flush is not yet a durable savepoint boundary - so
        # the *first* db.session.rollback() the script itself performs (e.g. one application failing)
        # would silently wipe out this fixture data too, not just the failed application's changes.
        # Committing here first establishes the fund/round as a baseline the script's own
        # commits/rollbacks can't touch.
        session.commit()
        return round_obj

    return _make


@pytest.fixture
def make_application(app, db, session):
    """
    Seeds an Applications row (via the shared seed_application helper) plus one row in each of the
    application-store PII child tables: Forms, Feedback, Eligibility, ResearchSurvey,
    EndOfApplicationSurveyFeedback - the tables the PII deletion script is expected to clear.
    """

    def _make(round_obj, status, project_name: str = "Test Org") -> Applications:
        account = seed_account(session)
        application = seed_application(
            session,
            round_obj.fund,
            round_obj,
            account,
            project_name=project_name,
            status=status,
        )

        session.add(Forms(application_id=application.id, json=[{"some": "answer"}], name="a-form"))
        session.add(
            Feedback(
                application_id=application.id,
                fund_id=str(round_obj.fund_id),
                round_id=str(round_obj.id),
                section_id="section-1",
                feedback_json={"comment": "some feedback"},
            )
        )
        session.add(
            Eligibility(
                form_id="eligibility-form",
                answers={"question": "answer"},
                eligible=True,
                application_id=application.id,
            )
        )
        session.add(
            ResearchSurvey(
                application_id=application.id,
                fund_id=str(round_obj.fund_id),
                round_id=str(round_obj.id),
                data={"survey": "answer"},
            )
        )
        session.add(
            EndOfApplicationSurveyFeedback(
                application_id=application.id,
                fund_id=str(round_obj.fund_id),
                round_id=str(round_obj.id),
                page_number=1,
                data={"more_detail": "some detail"},
            )
        )
        # see the comment in make_fund_round above: commit so this fixture data survives the script's
        # own later rollbacks, rather than just flushing.
        session.commit()
        return application

    return _make


@pytest.fixture
def make_assessment_record(app, db, session):
    def _make(application: Applications, round_obj) -> AssessmentRecord:
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
        session.add(assessment_record)
        session.commit()
        return assessment_record

    return _make
