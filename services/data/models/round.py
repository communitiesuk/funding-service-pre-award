import uuid
from datetime import datetime

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import JSON, Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.types import Boolean

from pre_award.db import db

BaseModel: DefaultMeta = db.Model


class Round(BaseModel):
    __table_args__ = (UniqueConstraint("fund_id", "short_name"),)
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    # fund_id: Mapped[UUID] = mapped_column(ForeignKey("fund.id"))
    fund_id = Column(
        "fund_id",
        UUID(as_uuid=True),
        ForeignKey("fund.id"),
        nullable=False,
    )
    title_json = Column("title_json", JSON(none_as_null=True), nullable=False, unique=False)
    short_name = Column("short_name", db.String(), nullable=False, unique=False)
    opens = Column("opens", DateTime())
    deadline = Column("deadline", DateTime())
    assessment_start = Column("assessment_start", DateTime())
    application_reminder_sent = Column(
        "application_reminder_sent",
        db.Boolean,
        default=False,
        nullable=False,
    )
    reminder_date = Column("reminder_date", DateTime())
    assessment_deadline = Column("assessment_deadline", DateTime())
    prospectus = Column("prospectus", db.String(), nullable=False, unique=False)
    privacy_notice = Column("privacy_notice", db.String(), nullable=False, unique=False)
    contact_us_banner_json = Column("contact_us_banner_json", JSON(none_as_null=True), nullable=True, unique=False)
    reference_contact_page_over_email = Column(
        "reference_contact_page_over_email",
        db.Boolean,
        default=False,
        nullable=False,
    )
    contact_email = Column("contact_email", db.String(), nullable=True, unique=False)
    contact_phone = Column("contact_phone", db.String(), nullable=True, unique=False)
    contact_textphone = Column("contact_textphone", db.String(), nullable=True, unique=False)
    support_times = Column("support_times", db.String(), nullable=False, unique=False)
    support_days = Column("support_days", db.String(), nullable=False, unique=False)
    instructions_json = Column("instructions_json", JSON(none_as_null=True), nullable=True, unique=False)
    feedback_link = Column("feedback_link", db.String(), unique=False)
    project_name_field_id = Column("project_name_field_id", db.String(), unique=False, nullable=False)
    application_guidance_json = Column(
        "application_guidance_json", JSON(none_as_null=True), nullable=True, unique=False
    )
    guidance_url = Column("guidance_url", db.String(), nullable=True, unique=False)
    all_uploaded_documents_section_available = Column(
        "all_uploaded_documents_section_available",
        Boolean,
        default=False,
        nullable=False,
    )
    application_fields_download_available = Column(
        "application_fields_download_available",
        db.Boolean,
        default=False,
        nullable=False,
    )
    display_logo_on_pdf_exports = Column(
        "display_logo_on_pdf_exports",
        db.Boolean,
        default=False,
        nullable=False,
    )
    mark_as_complete_enabled = Column(
        "mark_as_complete_enabled",
        db.Boolean,
        default=False,
        nullable=False,
    )
    is_expression_of_interest = Column(
        "is_expression_of_interest",
        db.Boolean,
        default=False,
        nullable=False,
    )
    feedback_survey_config = Column("feedback_survey_config", JSON(none_as_null=True), nullable=True, unique=False)
    eligibility_config = Column("eligibility_config", JSON(none_as_null=True), nullable=True, unique=False)
    eoi_decision_schema = Column("eoi_decision_schema ", JSON(none_as_null=True), nullable=True, unique=False)

    # def determine_round_status(round: Round):
    #     round_status = RoundStatus(
    #         past_submission_deadline=current_datetime_after_given_iso_string(round.deadline),
    #         not_yet_open=current_datetime_before_given_iso_string(round.opens),
    #         is_open=current_datetime_after_given_iso_string(round.opens)
    #         and current_datetime_before_given_iso_string(round.deadline),
    #     )
    #     return round_status

    @hybrid_property
    def is_past_submission_deadline(self):
        return datetime.now() > self.deadline
