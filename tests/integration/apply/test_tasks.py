from datetime import datetime, timedelta

from apply.tasks import send_incomplete_application_reminder_impl
from pre_award.application_store.db.models.application.enums import Status
from tests.integration.seeding import seed_account, seed_application, seed_fund, seed_round
from tests.pre_award.utils import AnyStringMatching


class TestSendIncompleteApplicationReminderTask:
    def _seed_round(self, session, fund, reminder_date, deadline):
        round = seed_round(session, fund, reminder_date=reminder_date, deadline=deadline)
        fund.rounds.append(round)
        session.flush()
        return round

    def test_send_incomplete_application_reminder_task_nothing_to_do(
        self, app, session, caplog, mock_notification_service_calls
    ):
        with app.app_context():
            send_incomplete_application_reminder_impl()

        assert caplog.messages == [
            "Starting to send incomplete application reminders",
            "Finished sending incomplete application reminders",
        ]

    def test_send_incomplete_application_reminder_task_emails(
        self, app, session, caplog, mock_notification_service_calls
    ):
        with app.app_context():
            fund = seed_fund(session)
            round = self._seed_round(
                session,
                fund,
                reminder_date=datetime.today() - timedelta(days=1),
                deadline=datetime.today() + timedelta(days=1),
            )
            account = seed_account(session)
            _ = seed_application(session, fund, round, account, started_at=datetime(2020, 1, 1))
            account2 = seed_account(session)
            _ = seed_application(session, fund, round, account2, started_at=datetime(2020, 1, 2))

            send_incomplete_application_reminder_impl()

            assert len(mock_notification_service_calls) == 2

            assert caplog.messages == [
                "Starting to send incomplete application reminders",
                AnyStringMatching(rf"Sent notification .+ to {account.id}"),
                AnyStringMatching(rf"Sent notification .+ to {account2.id}"),
                AnyStringMatching(r"The application reminder has been sent successfully for test fund \[round\]"),
                "Finished sending incomplete application reminders",
            ]

    def test_send_incomplete_application_reminder_task_only_sends_one_email_per_account(
        self, app, session, caplog, mock_notification_service_calls
    ):
        with app.app_context():
            fund = seed_fund(session)
            round = self._seed_round(
                session,
                fund,
                reminder_date=datetime.today() - timedelta(days=1),
                deadline=datetime.today() + timedelta(days=1),
            )
            account = seed_account(session)
            _ = seed_application(session, fund, round, account, started_at=datetime(2020, 1, 1))
            _ = seed_application(session, fund, round, account, started_at=datetime(2020, 1, 2))
            _ = seed_application(session, fund, round, account, started_at=datetime(2020, 1, 3))

            send_incomplete_application_reminder_impl()

            assert len(mock_notification_service_calls) == 1

            assert caplog.messages == [
                "Starting to send incomplete application reminders",
                AnyStringMatching(rf"Sent notification .+ to {account.id}"),
                AnyStringMatching(r"The application reminder has been sent successfully for test fund \[round\]"),
                "Finished sending incomplete application reminders",
            ]

    def test_send_incomplete_application_reminder_task_does_not_send_before_reminder_date(
        self, app, session, caplog, mock_notification_service_calls
    ):
        with app.app_context():
            fund = seed_fund(session)
            round = self._seed_round(
                session,
                fund,
                reminder_date=datetime.today() + timedelta(days=1),
                deadline=datetime.today() + timedelta(days=2),
            )
            account = seed_account(session)
            _ = seed_application(session, fund, round, account)

            send_incomplete_application_reminder_impl()

            assert len(mock_notification_service_calls) == 0

            assert caplog.messages == [
                "Starting to send incomplete application reminders",
                "Finished sending incomplete application reminders",
            ]

    def test_send_incomplete_application_reminder_task_does_not_send_for_submitted_applications(
        self, app, session, caplog, mock_notification_service_calls
    ):
        with app.app_context():
            fund = seed_fund(session)
            round = self._seed_round(
                session,
                fund,
                reminder_date=datetime.today() - timedelta(days=1),
                deadline=datetime.today() + timedelta(days=1),
            )
            account = seed_account(session)
            _ = seed_application(session, fund, round, account, status=Status.NOT_STARTED)
            account2 = seed_account(session)
            _ = seed_application(session, fund, round, account2, status=Status.SUBMITTED)
            account3 = seed_account(session)
            _ = seed_application(session, fund, round, account3, status=Status.CHANGE_RECEIVED)

            send_incomplete_application_reminder_impl()

            assert len(mock_notification_service_calls) == 1

            assert caplog.messages == [
                "Starting to send incomplete application reminders",
                AnyStringMatching(rf"Sent notification .+ to {account.id}"),
                AnyStringMatching(r"The application reminder has been sent successfully for test fund \[round\]"),
                "Finished sending incomplete application reminders",
            ]
