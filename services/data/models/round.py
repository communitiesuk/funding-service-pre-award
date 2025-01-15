import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from pre_award.common.locale_selector.get_lang import get_lang
from pre_award.db import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


class Round(Model):
    __table_args__ = (UniqueConstraint("fund_id", "short_name"),)
    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True,
    )
    # fund_id: Mapped[UUID] = mapped_column(ForeignKey("fund.id"))
    fund_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("fund.id"),
    )
    title_json: Mapped[dict[str, str]]
    short_name: Mapped[str]
    opens: Mapped[Optional[datetime]]
    deadline: Mapped[Optional[datetime]]
    assessment_start: Mapped[Optional[datetime]]
    application_reminder_sent: Mapped[bool] = mapped_column(default=False)
    reminder_date: Mapped[Optional[datetime]]
    assessment_deadline: Mapped[Optional[datetime]]
    prospectus: Mapped[str]
    privacy_notice: Mapped[str]
    contact_us_banner_json: Mapped[Optional[dict[str, str]]]
    reference_contact_page_over_email: Mapped[bool] = mapped_column(
        default=False,
    )
    contact_email: Mapped[Optional[str]]
    contact_phone: Mapped[Optional[str]]
    contact_textphone: Mapped[Optional[str]]
    support_times: Mapped[str]
    support_days: Mapped[str]
    instructions_json: Mapped[Optional[dict[str, str]]]
    feedback_link: Mapped[Optional[str]]
    project_name_field_id: Mapped[str]
    application_guidance_json: Mapped[Optional[dict[str, str]]]
    guidance_url: Mapped[Optional[str]]
    all_uploaded_documents_section_available: Mapped[bool] = mapped_column(default=False)
    application_fields_download_available: Mapped[bool] = mapped_column(default=False)
    display_logo_on_pdf_exports: Mapped[bool] = mapped_column(default=False)
    mark_as_complete_enabled: Mapped[bool] = mapped_column(default=False)
    is_expression_of_interest: Mapped[bool] = mapped_column(default=False)
    feedback_survey_config: Mapped[Optional[dict[str, str]]]
    eligibility_config: Mapped[Optional[dict[str, str]]]
    eoi_decision_schema: Mapped[Optional[dict[str, str]]]

    @hybrid_property
    def is_past_submission_deadline(self) -> bool:
        return datetime.now() > self.deadline if self.deadline else False

    @hybrid_property
    def is_not_yet_open(self) -> bool:
        return datetime.now() < self.opens if self.opens else False

    @hybrid_property
    def is_open(self) -> bool:
        return self.opens < datetime.now() < self.deadline if self.deadline and self.opens else False

    @property
    def round_title(self) -> str:
        return self.title_json[get_lang()] or self.title_json["en"]
