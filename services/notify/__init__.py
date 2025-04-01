import dataclasses
import io
import os
import uuid
from datetime import datetime
from typing import Any, Literal, cast

import pytz
from flask import Flask, current_app
from fsd_utils import NotifyConstants
from notifications_python_client import NotificationsAPIClient, prepare_upload  # type: ignore[attr-defined]
from notifications_python_client.errors import APIError, TokenError


class NotificationError(Exception):
    def __init__(
        self,
        message: str = "There was a problem sending the email through GOV.UK Notify",
    ):
        self.message = message
        super().__init__(self.message)


@dataclasses.dataclass(frozen=True)
class Notification:
    id: uuid.UUID


def _format_timestamp_to_human_readable(submission_date: datetime | None) -> str | None:
    if submission_date is None:
        return submission_date

    return submission_date.strftime(f"{'%d %B %Y'} at {'%I:%M%p'}").replace("AM", "am").replace("PM", "pm")


def _format_naive_utc_timestamp_to_europe_london_readable(submission_date: str) -> str:
    UTC_timezone = pytz.timezone("UTC")
    UK_timezone = pytz.timezone("Europe/London")
    UK_datetime = UTC_timezone.localize(datetime.strptime(submission_date, "%Y-%m-%dT%H:%M:%S.%f")).astimezone(
        UK_timezone
    )

    return cast(str, _format_timestamp_to_human_readable(UK_datetime))


class NotificationService:
    MAGIC_LINK_TEMPLATE_ID = os.environ.get("MAGIC_LINK_TEMPLATE_ID", "02a6d48a-f227-4b9a-9dd7-9e0cf203c8a2")

    EXPRESSION_OF_INTEREST_TEMPLATE_ID = {
        "54c11ec2-0b16-46bb-80d2-f210e47a8791": {
            NotifyConstants.TEMPLATE_TYPE_EOI_PASS: {
                "fund_name": "COF",
                "template_id": {
                    "en": "04db42f4-a74e-4ab3-b9e2-565592fd6f46",
                    "cy": "46915152-ee11-4bce-a0e1-ce1033078640",
                },
            },
            NotifyConstants.TEMPLATE_TYPE_EOI_PASS_W_CAVEATS: {
                "fund_name": "COF",
                "template_id": {
                    "en": "705684c7-6985-4d4c-9170-08a85f47b8e1",
                    "cy": "ead6bfc2-f3a1-468c-8d5a-87a32bf31311",
                },
            },
        },
        "4db6072c-4657-458d-9f57-9ca59638317b": {
            NotifyConstants.TEMPLATE_TYPE_EOI_PASS: {
                "fund_name": "COF25-EOI",
                "template_id": {
                    "en": "55cfe35e-f7d4-43b9-b557-8a20dd5bccda",
                    "cy": "08141b92-f7d2-4c41-b15d-6d0a0a6a85df",
                },
            },
            NotifyConstants.TEMPLATE_TYPE_EOI_PASS_W_CAVEATS: {
                "fund_name": "COF25-EOI",
                "template_id": {
                    "en": "589b5574-fd78-4904-b240-13b12b5c0109",
                    "cy": "4d010700-f5e1-41cb-a7e8-6eda2fa8b484",
                },
            },
        },
        "97e145f0-5b9a-4ed1-9e15-3e0d9fd998f0": {
            NotifyConstants.TEMPLATE_TYPE_EOI_PASS: {
                "fund_name": "CF1",
                "template_id": {
                    "en": "04db42f4-a74e-4ab3-b9e2-565592fd6f46",
                    "cy": "46915152-ee11-4bce-a0e1-ce1033078640",
                },
            },
            NotifyConstants.TEMPLATE_TYPE_EOI_PASS_W_CAVEATS: {
                "fund_name": "CF1",
                "template_id": {
                    "en": "705684c7-6985-4d4c-9170-08a85f47b8e1",
                    "cy": "ead6bfc2-f3a1-468c-8d5a-87a32bf31311",
                },
            },
        },
    }

    APPLICATION_SUBMISSION_TEMPLATE_ID_EN = os.environ.get(
        "APPLICATION_SUBMISSION_TEMPLATE_ID_EN", "6adbba70-2fde-4ca7-94cb-7f7eb264efaa"
    )
    APPLICATION_SUBMISSION_TEMPLATE_ID_CY = os.environ.get(
        "APPLICATION_SUBMISSION_TEMPLATE_ID_CY", "60bb6baa-0ef9-4059-954e-7c2744e6c63a"
    )

    APPLICATION_INCOMPLETE_TEMPLATE_ID = os.environ.get(
        "APPLICATION_INCOMPLETE_TEMPLATE_ID", "944cb37d-c9e0-4731-88f5-d752514da57f"
    )

    APPLICATION_DEADLINE_REMINDER_TEMPLATE_ID = os.environ.get(
        "APPLICATION_DEADLINE_REMINDER_TEMPLATE_ID",
        "e41cc73d-6947-4cbb-aedd-4ab2f470a2d2",
    )

    ASSESSMENT_APPLICATION_ASSIGNED = os.environ.get(
        "ASSESSMENT_APPLICATION_ASSIGNED", "d4bdc13e-93b4-48ba-8d22-71bf4f480128"
    )

    ASSESSMENT_APPLICATION_UNASSIGNED = os.environ.get(
        "ASSESSMENT_APPLICATION_UNASSIGNED", "9cfaa46c-f122-4532-a9f6-b3c773de6555"
    )

    CHANGE_RECEIVED_TEMPLATE_ID = os.environ.get("CHANGE_RECEIVED_TEMPLATE_ID", "cc1a6287-7d70-4264-84aa-0f8dbf9341dc")
    CHANGE_REQUEST_TEMPLATE_ID = os.environ.get("CHANGE_REQUEST_TEMPLATE_ID", "272d50bf-88f1-4a2c-9e38-02ea54bd389c")

    DOWNLOAD_REPORT_TEMPLATE_ID = os.environ.get("DOWNLOAD_REPORT_TEMPLATE_ID", "252e6b12-eb77-47e7-92d4-70fe9dad0fd1")

    FUNDING_SERVICE_SUPPORT_EMAIL_ADDRESS = "FundingService@communities.gov.uk"

    # E.G. "EMAIL": "GOV_NOTIFY_ID"
    REPLY_TO_EMAILS_WITH_NOTIFY_ID = {
        "LocalPlansandGreenBeltFunding@communities.gov.uk": "7bc1b42f-512d-4e43-a70a-3c06a3197f38",
        FUNDING_SERVICE_SUPPORT_EMAIL_ADDRESS: "10668b8d-9472-4ce8-ae07-4fcc7bf93a9d",
        "COF@levellingup.gov.uk": "10668b8d-9472-4ce8-ae07-4fcc7bf93a9d",
        "COF@communities.gov.uk": "10668b8d-9472-4ce8-ae07-4fcc7bf93a9d",
        "transformationfund@levellingup.gov.uk": "25286d9a-8543-41b5-a00f-331b999e51f0",
        "cyprfund@levellingup.gov.uk": "72bb79a8-2748-4404-9f01-14690bee3843",
        "digitalplanningteam@communities.gov.uk": "73eecbb1-5dbc-4653-8c58-46aa79151210",
        "digitalplanningteam@levellingup.gov.uk": "73eecbb1-5dbc-4653-8c58-46aa79151210",
        "HighStreetRentalAuctions@levellingup.gov.uk": "0874cafb-a297-4f3c-bb3f-99bc578cce4a",
        "sponsorship@communities.gov.uk": "cc80c848-a9e6-432a-bd3a-cf6fe6b77b3d",
        "chambid@communities.gov.uk": "51b1b1bb-5c4e-4faa-bca2-3e17c118c446",
    }

    def __init__(self) -> None:
        self.client: NotificationsAPIClient | None = None

    def init_app(self, app: Flask) -> None:
        app.extensions["notification_service"] = self
        app.extensions["notification_service.client"] = NotificationsAPIClient(app.config["GOV_NOTIFY_API_KEY"])  # type: ignore[no-untyped-call]

    def _send_email(
        self,
        email_address: str,
        template_id: str,
        personalisation: dict[str, Any] | None,
        govuk_notify_reference: str | None = None,
        email_reply_to_id: str | None = None,
        one_click_unsubscribe_url: str | None = None,
    ) -> Notification:
        if current_app.config["DISABLE_NOTIFICATION_SERVICE"]:
            current_app.logger.info(
                "Notification service is disabled. Would have sent email to %(email_address)s",
                dict(email_address=email_address),
            )
            return Notification(id=uuid.UUID("00000000-0000-0000-0000-000000000000"))

        try:
            notification_data = current_app.extensions["notification_service.client"].send_email_notification(
                email_address,
                template_id,
                personalisation=personalisation,
                reference=govuk_notify_reference,
                email_reply_to_id=email_reply_to_id,
                one_click_unsubscribe_url=one_click_unsubscribe_url,
            )
            return Notification(id=uuid.UUID(notification_data["id"]))
        except (TokenError, APIError) as e:
            raise NotificationError() from e

    def send_magic_link(
        self,
        email_address: str,
        magic_link_url: str,
        fund_name: str,
        contact_help_email: str,
        request_new_link_url: str,
        govuk_notify_reference: str | None = None,
    ) -> Notification:
        return self._send_email(
            email_address,
            self.MAGIC_LINK_TEMPLATE_ID,
            personalisation={
                "name of fund": fund_name,
                "link to application": magic_link_url,
                "contact details": contact_help_email,
                "request new link url": request_new_link_url,
            },
            govuk_notify_reference=govuk_notify_reference,
            email_reply_to_id=self.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(contact_help_email),
        )

    def send_eoi_pass_email(
        self,
        email_address: str,
        contact_name: str,
        language: Literal["en", "cy"],
        fund_id: str,
        fund_name: str,
        application_reference: str,
        submission_date: str,
        round_name: str,
        questions: str,
        contact_help_email: str,
        govuk_notify_reference: str | None = None,
    ) -> Notification:
        template_id = self.EXPRESSION_OF_INTEREST_TEMPLATE_ID[fund_id][NotifyConstants.TEMPLATE_TYPE_EOI_PASS][
            "template_id"
        ].get(language, "en")  # type: ignore[attr-defined]

        submission_date = _format_naive_utc_timestamp_to_europe_london_readable(submission_date)

        return self._send_email(
            email_address,
            template_id,
            personalisation={
                "name of fund": fund_name,
                "application reference": application_reference,
                "date submitted": submission_date,
                "round name": round_name,
                "question": {
                    "file": questions,
                    "filename": None,
                    "confirm_email_before_download": None,
                    "retention_period": None,
                },
                "full name": contact_name or "",
            },
            govuk_notify_reference=govuk_notify_reference,
            email_reply_to_id=self.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(contact_help_email),
        )

    def send_eoi_pass_with_caveats_email(
        self,
        email_address: str,
        contact_name: str,
        language: Literal["en", "cy"],
        fund_id: str,
        fund_name: str,
        application_reference: str,
        submission_date: str,
        round_name: str,
        questions: str,
        caveats: str,
        contact_help_email: str,
        govuk_notify_reference: str | None = None,
    ) -> Notification:
        template_id = self.EXPRESSION_OF_INTEREST_TEMPLATE_ID[fund_id][
            NotifyConstants.TEMPLATE_TYPE_EOI_PASS_W_CAVEATS
        ]["template_id"].get(language, "en")  # type: ignore[attr-defined]

        submission_date = _format_naive_utc_timestamp_to_europe_london_readable(submission_date)

        return self._send_email(
            email_address,
            template_id,
            personalisation={
                "name of fund": fund_name,
                "application reference": application_reference,
                "date submitted": submission_date,
                "round name": round_name,
                "question": {
                    "file": questions,
                    "filename": None,
                    "confirm_email_before_download": None,
                    "retention_period": None,
                },
                "caveats": caveats,
                "full name": contact_name or "",
            },
            govuk_notify_reference=govuk_notify_reference,
            email_reply_to_id=self.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(contact_help_email),
        )

    def send_submit_application_email(
        self,
        email_address: str,
        language: Literal["en", "cy"],
        fund_name: str,
        application_reference: str,
        submission_date: str,
        round_name: str,
        questions: str,
        prospectus_url: str,
        contact_help_email: str,
        govuk_notify_reference: str | None = None,
    ) -> Notification:
        template_id = (
            self.APPLICATION_SUBMISSION_TEMPLATE_ID_CY
            if language == "cy"
            else self.APPLICATION_SUBMISSION_TEMPLATE_ID_EN
        )

        submission_date = _format_naive_utc_timestamp_to_europe_london_readable(submission_date)

        return self._send_email(
            email_address,
            template_id,
            personalisation={
                "name of fund": fund_name,
                "application reference": application_reference,
                "date submitted": submission_date,
                "round name": round_name,
                "question": {
                    "file": questions,
                    "filename": None,
                    "confirm_email_before_download": None,
                    "retention_period": None,
                },
                "URL of prospectus": prospectus_url,
                "contact email": contact_help_email,
            },
            govuk_notify_reference=govuk_notify_reference,
            email_reply_to_id=self.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(contact_help_email),
        )

    def send_incomplete_application_email(
        self,
        email_address: str,
        fund_name: str,
        application_reference: str,
        round_name: str,
        questions: str,
        contact_help_email: str,
        govuk_notify_reference: str | None = None,
    ) -> Notification:
        return self._send_email(
            email_address,
            self.APPLICATION_INCOMPLETE_TEMPLATE_ID,
            personalisation={
                "name of fund": fund_name,
                "application reference": application_reference,
                "round name": round_name,
                "question": {
                    "file": questions,
                    "filename": None,
                    "confirm_email_before_download": None,
                    "retention_period": None,
                },
                "contact email": contact_help_email,
            },
            govuk_notify_reference=govuk_notify_reference,
            email_reply_to_id=self.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(contact_help_email),
        )

    def send_application_deadline_reminder_email(
        self,
        email_address: str,
        fund_name: str,
        round_name: str,
        deadline: datetime,
        contact_help_email: str | None,
        govuk_notify_reference: str | None = None,
    ) -> Notification:
        return self._send_email(
            email_address,
            self.APPLICATION_DEADLINE_REMINDER_TEMPLATE_ID,
            personalisation={
                "name of fund": fund_name,
                "round name": round_name,
                "application deadline": _format_timestamp_to_human_readable(deadline),
            },
            govuk_notify_reference=govuk_notify_reference,
            email_reply_to_id=self.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(contact_help_email),  # type: ignore[arg-type]
        )

    def send_assessment_assigned_email(
        self,
        email_address: str,
        reference_number: str,
        fund_name: str,
        project_name: str,
        assignment_message: str,
        assessment_link: str,
        lead_assessor_email: str,
        govuk_notify_reference: str | None = None,
    ) -> Notification:
        return self._send_email(
            email_address,
            self.ASSESSMENT_APPLICATION_ASSIGNED,
            personalisation={
                "fund_name": fund_name,
                "reference_number": reference_number,
                "project_name": project_name,
                "assignment message": assignment_message or "",
                "assessment link": assessment_link,
                "lead assessor email": lead_assessor_email,
            },
            govuk_notify_reference=govuk_notify_reference,
            email_reply_to_id=self.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(self.FUNDING_SERVICE_SUPPORT_EMAIL_ADDRESS),
        )

    def send_assessment_unassigned_email(
        self,
        email_address: str,
        reference_number: str,
        fund_name: str,
        project_name: str,
        assignment_message: str,
        assessment_link: str,
        lead_assessor_email: str,
        govuk_notify_reference: str | None = None,
    ) -> Notification:
        return self._send_email(
            email_address,
            self.ASSESSMENT_APPLICATION_UNASSIGNED,
            personalisation={
                "fund_name": fund_name,
                "reference_number": reference_number,
                "project_name": project_name,
                "assignment message": assignment_message or "",
                "assessment link": assessment_link,
                "lead assessor email": lead_assessor_email,
            },
            govuk_notify_reference=govuk_notify_reference,
            email_reply_to_id=self.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(self.FUNDING_SERVICE_SUPPORT_EMAIL_ADDRESS),
        )

    def send_change_received_email(
        self,
        email_address: str,
        fund_name: str,
        round_name: str,
        contact_help_email: str,
        assess_url: str,
        govuk_notify_reference: str | None = None,
    ) -> Notification:
        template_id = self.CHANGE_RECEIVED_TEMPLATE_ID

        return self._send_email(
            email_address,
            template_id,
            personalisation={
                "name of fund": fund_name,
                "round name": round_name,
                "sign in link": assess_url,
                "contact email": contact_help_email,
            },
            email_reply_to_id=self.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(self.FUNDING_SERVICE_SUPPORT_EMAIL_ADDRESS),
            govuk_notify_reference=govuk_notify_reference,
        )

    def send_requested_changes_email(
        self,
        email_address: str,
        application_reference: str,
        fund_name: str,
        round_name: str,
        application_deadline: str,
        apply_fund_url: str,
        contact_email: str,
        govuk_notify_reference: str | None = None,
    ) -> Notification:
        return self._send_email(
            email_address,
            self.CHANGE_REQUEST_TEMPLATE_ID,
            personalisation={
                "name of fund": fund_name,
                "application reference": application_reference,
                "round name": round_name,
                "contact email": contact_email,
                "sign in link": apply_fund_url,
                "application deadline": application_deadline,
            },
            govuk_notify_reference=govuk_notify_reference,
            email_reply_to_id=self.REPLY_TO_EMAILS_WITH_NOTIFY_ID.get(self.FUNDING_SERVICE_SUPPORT_EMAIL_ADDRESS),
        )

    def send_report_email(self, file_buffer: io.BytesIO) -> Notification:
        return self._send_email(
            os.getenv("NOTIFY_SEND_EMAIL", "test@example.com"),
            self.DOWNLOAD_REPORT_TEMPLATE_ID,
            personalisation={
                "link_to_file": prepare_upload(file_buffer, filename="reports.xlsx"),  # type: ignore[no-untyped-call]
            },
        )


def get_notification_service() -> NotificationService:
    return cast(NotificationService, current_app.extensions["notification_service"])
