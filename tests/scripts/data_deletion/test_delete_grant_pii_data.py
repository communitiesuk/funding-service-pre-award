from datetime import datetime, timedelta

from click.testing import CliRunner

from data.models import PiiDeletionLog
from pre_award.application_store.db.models import Applications, Eligibility, EndOfApplicationSurveyFeedback, Feedback
from pre_award.application_store.db.models.application.enums import PiiDeletionScope, Status
from pre_award.application_store.db.models.forms.forms import Forms
from pre_award.application_store.db.models.research.research import ResearchSurvey
from pre_award.assessment_store.db.queries.assessment_records._helpers import FIELD_DEFAULT_VALUE
from pre_award.db import db
from scripts.data_deletion.delete_grant_pii_data import delete_application_pii, delete_pii

PAST_DEADLINE = datetime.now() - timedelta(days=365 * 20)  # long enough ago that any retention has expired
RECENT_DEADLINE = datetime.now() - timedelta(days=1)  # closed, but no retention period will have passed


def invoke(app, mocker, args, input=None, run_by="test-runner@example.com"):
    # pytest-flask's autouse `_push_request_context` fixture already pushes an app context for the
    # whole duration of any test that uses the `app` fixture. Pushing a second one here would bind a
    # *different* Flask-SQLAlchemy scoped session, so objects created by the test fixtures (under the
    # outer context) would come back as "attached to a different session" as soon as the script
    # touched them under this inner context.
    mocker.patch("scripts.data_deletion.delete_grant_pii_data.get_run_by", return_value=run_by)
    mocker.patch("scripts.data_deletion.delete_grant_pii_data.list_files_in_folder", return_value=["file1.pdf"])
    mock_delete_file = mocker.patch("scripts.data_deletion.delete_grant_pii_data.delete_file_from_aws")
    runner = CliRunner()
    result = runner.invoke(delete_pii, args, input=input)
    return result, mock_delete_file


def assert_application_pii_deleted(application_id):
    assert db.session.query(Forms).filter(Forms.application_id == application_id).count() == 0
    assert db.session.query(Feedback).filter(Feedback.application_id == application_id).count() == 0
    assert db.session.query(Eligibility).filter(Eligibility.application_id == application_id).count() == 0
    assert db.session.query(ResearchSurvey).filter(ResearchSurvey.application_id == application_id).count() == 0
    assert (
        db.session.query(EndOfApplicationSurveyFeedback)
        .filter(EndOfApplicationSurveyFeedback.application_id == application_id)
        .count()
        == 0
    )
    application = db.session.get(Applications, application_id)
    assert application.is_deleted is True
    assert application.project_name == ""


def assert_application_pii_retained(application_id):
    assert db.session.query(Forms).filter(Forms.application_id == application_id).count() == 1
    application = db.session.get(Applications, application_id)
    assert application.is_deleted is False
    assert application.project_name != ""


def get_latest_pii_deletion_log(round_id) -> PiiDeletionLog:
    return (
        db.session.query(PiiDeletionLog)
        .filter(PiiDeletionLog.round_id == round_id)
        .order_by(PiiDeletionLog.deletion_timestamp.desc())
        .first()
    )


class TestDeleteGrantPiiData:
    def test_round_not_found_exits_cleanly(self, app, db, mocker):
        result, _ = invoke(app, mocker, ["--fund", "NOPE", "--round", "NOPE", "--env", "dev"])
        assert result.exit_code == 0
        assert "No round found" in result.output

    def test_round_still_open_exits_cleanly(self, app, mocker, make_fund_round):
        make_fund_round("LOTR", "OPEN1", deadline=datetime.now() + timedelta(days=30))
        result, _ = invoke(app, mocker, ["--fund", "LOTR", "--round", "OPEN1", "--env", "dev"])
        assert result.exit_code == 0
        assert "still open" in result.output

    def test_already_fully_deleted_exits_cleanly(self, app, mocker, make_fund_round):
        make_fund_round("LOTR", "DONE1", deadline=PAST_DEADLINE, pii_deleted_for_applications=PiiDeletionScope.ALL)
        result, _ = invoke(app, mocker, ["--fund", "LOTR", "--round", "DONE1", "--env", "dev"])
        assert result.exit_code == 0
        assert "already completed for ALL applications" in result.output

    def test_retention_not_yet_passed_exits_cleanly_without_crash(self, app, mocker, make_fund_round, make_application):
        round_obj = make_fund_round("LOTR", "FRESH1", deadline=RECENT_DEADLINE)
        make_application(round_obj, Status.SUBMITTED)
        result, _ = invoke(app, mocker, ["--fund", "LOTR", "--round", "FRESH1", "--env", "dev"])
        assert result.exit_code == 0
        assert "No applications are currently eligible for deletion" in result.output

    def test_dry_run_makes_no_changes(self, app, mocker, make_fund_round, make_application):
        round_obj = make_fund_round("LOTR", "DRY1", deadline=PAST_DEADLINE)
        application = make_application(round_obj, Status.NOT_STARTED)

        result, mock_delete_file = invoke(
            app,
            mocker,
            ["--fund", "LOTR", "--round", "DRY1", "--env", "dev", "--dry-run"],
            input="B\n",
        )

        assert result.exit_code == 0
        assert "DRY RUN" in result.output
        mock_delete_file.assert_not_called()
        application_after = db.session.get(Applications, application.id)
        assert application_after.is_deleted is False
        db.session.refresh(round_obj)
        assert round_obj.pii_deleted_for_applications is None

    def test_real_run_deletes_application_pii_and_assessment_record(
        self, app, mocker, make_fund_round, make_application, make_assessment_record
    ):
        round_obj = make_fund_round("LOTR", "REAL1", deadline=PAST_DEADLINE)
        application = make_application(round_obj, Status.NOT_STARTED)
        assessment_record = make_assessment_record(application, round_obj)

        result, mock_delete_file = invoke(
            app,
            mocker,
            ["--fund", "LOTR", "--round", "REAL1", "--env", "dev", "--no-dry-run"],
            input="B\nLOTR-REAL1\n",
        )

        assert result.exit_code == 0, result.output
        assert_application_pii_deleted(application.id)
        mock_delete_file.assert_called_once_with(f"{application.id}/file1.pdf")

        db.session.refresh(assessment_record)
        assert assessment_record.is_deleted is True
        assert assessment_record.jsonb_blob["forms"] == []
        # location_json_blob keeps its dict shape (several templates/sort lambdas read specific keys
        # off it unconditionally) but the potential PII value is replaced with the app's existing placeholder, not left
        # as the real postcode.
        assert assessment_record.location_json_blob["postcode"] == FIELD_DEFAULT_VALUE
        assert "AB1 2CD" not in assessment_record.location_json_blob.values()

        db.session.refresh(round_obj)
        # this round has zero submitted applications, so only the (non-empty) unsubmitted scope is
        # marked complete — a scope with nothing in it is left untouched rather than vacuously "done".
        assert round_obj.pii_deleted_for_applications == PiiDeletionScope.UN_SUBMITTED
        assert "PiiDeletionLog entry created" in result.output

        log_entry = get_latest_pii_deletion_log(round_obj.id)
        assert log_entry.deleted_application_ids == [str(application.id)]
        assert log_entry.retained_application_ids == []
        assert log_entry.failed_application_ids == []

    def test_confirmation_mismatch_aborts_without_deleting(self, app, mocker, make_fund_round, make_application):
        round_obj = make_fund_round("LOTR", "ABORT1", deadline=PAST_DEADLINE)
        application = make_application(round_obj, Status.NOT_STARTED)

        result, mock_delete_file = invoke(
            app,
            mocker,
            ["--fund", "LOTR", "--round", "ABORT1", "--env", "dev", "--no-dry-run"],
            input="B\nWRONG-CONFIRMATION\n",
        )

        assert result.exit_code == 0
        assert "Confirmation did not match" in result.output
        mock_delete_file.assert_not_called()
        assert_application_pii_retained(application.id)

    def test_exclude_application_retains_that_application_only(self, app, mocker, make_fund_round, make_application):
        round_obj = make_fund_round("LOTR", "EXCL1", deadline=PAST_DEADLINE)
        keep = make_application(round_obj, Status.NOT_STARTED, project_name="Keep Me")
        delete = make_application(round_obj, Status.NOT_STARTED, project_name="Delete Me")

        result, _ = invoke(
            app,
            mocker,
            [
                "--fund",
                "LOTR",
                "--round",
                "EXCL1",
                "--env",
                "dev",
                "--no-dry-run",
                "--exclude-application",
                str(keep.id),
            ],
            input="B\nLOTR-EXCL1\n",
        )

        assert result.exit_code == 0, result.output
        assert_application_pii_retained(keep.id)
        assert_application_pii_deleted(delete.id)

        # the unsubmitted scope was NOT fully processed this run (one application was retained), so the
        # round-level completion flag must not claim it was.
        db.session.refresh(round_obj)
        assert round_obj.pii_deleted_for_applications is None

        log_entry = get_latest_pii_deletion_log(round_obj.id)
        assert log_entry.deleted_application_ids == [str(delete.id)]
        assert log_entry.retained_application_ids == [str(keep.id)]
        assert log_entry.failed_application_ids == []

    def test_exclude_application_accepts_multiple_repeated_flags(self, app, mocker, make_fund_round, make_application):
        round_obj = make_fund_round("LOTR", "EXCLMULTI1", deadline=PAST_DEADLINE)
        keep_1 = make_application(round_obj, Status.NOT_STARTED, project_name="Keep Me 1")
        keep_2 = make_application(round_obj, Status.NOT_STARTED, project_name="Keep Me 2")
        delete = make_application(round_obj, Status.NOT_STARTED, project_name="Delete Me")

        result, _ = invoke(
            app,
            mocker,
            [
                "--fund",
                "LOTR",
                "--round",
                "EXCLMULTI1",
                "--env",
                "dev",
                "--no-dry-run",
                "--exclude-application",
                str(keep_1.id),
                "--exclude-application",
                str(keep_2.id),
            ],
            input="B\nLOTR-EXCLMULTI1\n",
        )

        assert result.exit_code == 0, result.output
        assert_application_pii_retained(keep_1.id)
        assert_application_pii_retained(keep_2.id)
        assert_application_pii_deleted(delete.id)

    def test_exclude_application_not_in_scope_warns_but_continues(self, app, mocker, make_fund_round, make_application):
        round_obj = make_fund_round("LOTR", "EXCLWARN1", deadline=PAST_DEADLINE)
        application = make_application(round_obj, Status.NOT_STARTED)
        unrelated_id = "00000000-0000-0000-0000-000000000000"

        result, _ = invoke(
            app,
            mocker,
            [
                "--fund",
                "LOTR",
                "--round",
                "EXCLWARN1",
                "--env",
                "dev",
                "--no-dry-run",
                "--exclude-application",
                unrelated_id,
            ],
            input="B\nLOTR-EXCLWARN1\n",
        )

        assert result.exit_code == 0, result.output
        assert f"WARNING: excluded application {unrelated_id}" in result.output
        assert_application_pii_deleted(application.id)

    def test_invalid_exclude_application_id_aborts_before_round_lookup(self, app, mocker, make_fund_round):
        make_fund_round("LOTR", "BADEXCL1", deadline=PAST_DEADLINE)
        result, mock_delete_file = invoke(
            app,
            mocker,
            ["--fund", "LOTR", "--round", "BADEXCL1", "--env", "dev", "--exclude-application", "not-a-uuid"],
        )
        # type=click.UUID validates at argument-parsing time, before the command body runs at all —
        # so this is a Click usage error (exit code 2), not one of the script's own graceful exits.
        assert result.exit_code == 2
        assert "is not a valid UUID" in result.output
        mock_delete_file.assert_not_called()

    def test_failed_application_does_not_block_others_or_advance_round_flag(
        self, app, mocker, make_fund_round, make_application
    ):
        round_obj = make_fund_round("LOTR", "FAIL1", deadline=PAST_DEADLINE)
        ok_application = make_application(round_obj, Status.NOT_STARTED)
        bad_application = make_application(round_obj, Status.NOT_STARTED)

        mocker.patch("scripts.data_deletion.delete_grant_pii_data.get_run_by", return_value="test-runner@example.com")
        mocker.patch("scripts.data_deletion.delete_grant_pii_data.list_files_in_folder", return_value=[])
        mocker.patch("scripts.data_deletion.delete_grant_pii_data.delete_file_from_aws")

        def flaky_delete_application_pii(application):
            if str(application.id) == str(bad_application.id):
                raise RuntimeError("simulated failure")
            return delete_application_pii(application)

        mocker.patch(
            "scripts.data_deletion.delete_grant_pii_data.delete_application_pii",
            side_effect=flaky_delete_application_pii,
        )

        runner = CliRunner()
        result = runner.invoke(
            delete_pii,
            ["--fund", "LOTR", "--round", "FAIL1", "--env", "dev", "--no-dry-run"],
            input="B\nLOTR-FAIL1\n",
        )

        assert result.exit_code == 0, result.output
        assert "failed to fully delete application" in result.output
        assert_application_pii_deleted(ok_application.id)
        assert_application_pii_retained(bad_application.id)

        db.session.refresh(round_obj)
        # one application in the unsubmitted scope failed, so the round must not be marked complete
        assert round_obj.pii_deleted_for_applications is None

        log_entry = get_latest_pii_deletion_log(round_obj.id)
        assert log_entry.deleted_application_ids == [str(ok_application.id)]
        assert log_entry.retained_application_ids == []
        assert log_entry.failed_application_ids == [str(bad_application.id)]

    def test_s3_failure_leaves_db_rows_untouched_for_retry(self, app, mocker, make_fund_round, make_application):
        """
        If S3 cleanup fails, the DB commit for that application must never have happened - otherwise
        its is_deleted=True would be permanent, and a future run's inventory query (which only looks
        at is_deleted=False applications) would never pick it up again to finish the S3 cleanup.
        """
        round_obj = make_fund_round("LOTR", "S3FAIL1", deadline=PAST_DEADLINE)
        ok_application = make_application(round_obj, Status.NOT_STARTED)
        s3_bad_application = make_application(round_obj, Status.NOT_STARTED)

        mocker.patch("scripts.data_deletion.delete_grant_pii_data.get_run_by", return_value="test-runner@example.com")
        mocker.patch("scripts.data_deletion.delete_grant_pii_data.list_files_in_folder", return_value=["file1.pdf"])

        def flaky_delete_file_from_aws(file_key):
            if str(s3_bad_application.id) in file_key:
                raise RuntimeError("simulated S3 failure")

        mocker.patch(
            "scripts.data_deletion.delete_grant_pii_data.delete_file_from_aws",
            side_effect=flaky_delete_file_from_aws,
        )

        runner = CliRunner()
        result = runner.invoke(
            delete_pii,
            ["--fund", "LOTR", "--round", "S3FAIL1", "--env", "dev", "--no-dry-run"],
            input="B\nLOTR-S3FAIL1\n",
        )

        assert result.exit_code == 0, result.output
        assert "failed to fully delete application" in result.output
        assert_application_pii_deleted(ok_application.id)
        # the application whose S3 cleanup failed must be fully intact — not partially deleted — so a
        # future run's inventory query picks it up again and can complete the job cleanly.
        assert_application_pii_retained(s3_bad_application.id)

        db.session.refresh(round_obj)
        # one application in the unsubmitted scope failed, so the round must not be marked complete
        assert round_obj.pii_deleted_for_applications is None

        log_entry = get_latest_pii_deletion_log(round_obj.id)
        assert log_entry.deleted_application_ids == [str(ok_application.id)]
        assert log_entry.retained_application_ids == []
        assert log_entry.failed_application_ids == [str(s3_bad_application.id)]
