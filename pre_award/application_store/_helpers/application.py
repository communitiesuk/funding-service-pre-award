from operator import itemgetter

from flask import current_app
from fsd_utils import Decision

from pre_award.application_store.config.key_report_mappings.mappings import (
    ROUND_ID_TO_KEY_REPORT_MAPPING,
)
from pre_award.application_store.db.queries.application import create_qa_base64file
from pre_award.application_store.db.queries.reporting.queries import (
    map_application_key_fields,
)
from pre_award.config import Config
from services.notify import NotificationError, get_notification_service


def order_applications(applications, order_by, order_rev):
    """
    Returns a list of ordered applications
    """
    if order_by and order_by in [
        "id",
        "status",
        "account_id",
        "assessment_deadline",
        "started_at",
        "last_edited",
    ]:
        applications = sorted(
            applications,
            key=itemgetter(order_by),
            reverse=int(order_rev),
        )
    return applications


def send_submit_notification(
    application_with_form_json,
    eoi_results,
    account,
    application_with_form_json_and_fund_name,
    application,
    round_data,
):
    application_data = create_qa_base64file(application_with_form_json_and_fund_name, True)
    del application_data["forms"]
    full_name = account.full_name

    questions = application_data.get("questions_file")
    submission_date = application_data.get("date_submitted")
    fund_name = application_data.get("fund_name")
    fund_id = application_data.get("fund_id")
    round_name = application_data.get("round_name")
    application_reference = application_data.get("reference")
    language = application_data.get("language")
    prospectus_url = application_data.get("prospectus_url", "")

    notification = None
    if eoi_results:
        eoi_decision = eoi_results["decision"]
        if not full_name:
            full_name = map_application_key_fields(
                application_with_form_json,
                ROUND_ID_TO_KEY_REPORT_MAPPING[application.round_id],
                application.round_id,
            ).get("lead_contact_name", "")

        match eoi_decision:
            case Decision.FAIL:
                return  # we don't send emails for a failure

            case Decision.PASS:
                try:
                    notification = get_notification_service().send_eoi_pass_email(
                        email_address=account.email,
                        contact_name=full_name.title() if full_name else None,
                        language=language,
                        fund_id=fund_id,
                        fund_name=fund_name,
                        application_reference=application_reference,
                        submission_date=submission_date,
                        round_name=round_name,
                        questions=questions,
                        contact_help_email=round_data.contact_email,
                    )
                except NotificationError:
                    current_app.logger.exception("Failed to send EOI Pass email")

            case Decision.PASS_WITH_CAVEATS:
                caveats = eoi_results["caveats"]
                try:
                    notification = get_notification_service().send_eoi_pass_with_caveats_email(
                        email_address=account.email,
                        contact_name=full_name.title() if full_name else None,
                        language=language,
                        fund_id=fund_id,
                        fund_name=fund_name,
                        application_reference=application_reference,
                        submission_date=submission_date,
                        round_name=round_name,
                        questions=questions,
                        caveats=caveats,
                        contact_help_email=round_data.contact_email,
                    )
                except NotificationError:
                    current_app.logger.exception("Failed to send EOI Pass (with caveats) email")

            case _:
                current_app.logger.error(
                    "Unknown eoi_decision [%(eoi_decision)s], unable to send submit notification",
                    dict(eoi_decision=eoi_decision),
                )
                return
    else:
        try:
            notification = get_notification_service().send_submit_application_email(
                email_address=account.email,
                language=language,
                fund_name=fund_name,
                application_reference=application_reference,
                submission_date=submission_date,
                round_name=round_name,
                questions=questions,
                prospectus_url=prospectus_url,
                contact_help_email=round_data.contact_email,
            )
        except NotificationError:
            current_app.logger.exception("Failed to send submitted application email")

    if notification:
        current_app.logger.info(
            "Sent notification %(notification_id)s for application %(application_reference)s",
            dict(notification_id=notification.id, application_reference=application_reference),
        )


def send_change_received_notification(fund, round_data):
    if (
        fund.short_name == "DPIF" or fund.funding_type != "UNCOMPETED"
    ):  # TODO remove DPIF conditon once we move it to COMPETITIVE funds`
        return
    get_notification_service().send_change_received_email(
        email_address=round_data.contact_email,
        fund_name=fund.name_json["en"],
        round_name=round_data.title,
        assess_url=Config.ASSESS_HOST + f"/assess/fund_dashboard/{fund.short_name}/{round_data.short_name}/",
        contact_help_email=round_data.contact_email,
    )
