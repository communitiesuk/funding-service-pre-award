import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, Date, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean

from db import db

if TYPE_CHECKING:
    from proto.common.data.models.fund import Fund
    from proto.common.data.models.question_bank import ProtoDataCollectionSection


class Round(db.Model):
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

    # probably this should be case insensitive
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

    proto_draft: Mapped[bool] = mapped_column(default=True)

    proto_start_date = Column("proto_start_date", Date())
    proto_end_date = Column("proto_end_date", Date())

    proto_created_date = Column("proto_created_date", DateTime(), server_default=func.now())
    proto_updated_date = Column("proto_updated_date", DateTime(), server_default=func.now(), onupdate=func.now())

    # whenever we get the round we're going to want the fund information - we _might_ want to be able to override this
    # but this feels like a very sensible way around for most of applies use case
    proto_grant: Mapped["Fund"] = relationship("Fund", lazy=False)
    application_sections: Mapped[list["ProtoDataCollectionSection"]] = relationship(
        "ProtoDataCollectionSection", lazy="joined", order_by="ProtoDataCollectionSection.order"
    )

    def __repr__(self):
        return f"<Round {self.short_name}: {self.title_json['en']}>"

    @property
    def status(self):
        today = datetime.date.today()
        now = datetime.datetime.utcnow()

        if self.proto_draft:
            return "draft"

        if today < self.proto_start_date:
            return "waiting to open"

        if today < self.proto_end_date:
            return "applications open"

        if self.assessment_start and now < self.assessment_start:
            return "waiting for assessment to start"

        if self.assessment_deadline and now < self.assessment_deadline:
            return "assessment open"

        return "closed"

    @property
    def status_colour(self):
        # Design system tag colours: https://design-system.service.gov.uk/components/tag/#additional-colours
        match self.status:
            case "draft":
                return "grey"
            case "waiting to open":
                return "yellow"
            case "applications open":
                return "green"
            case "waiting for assessment to start":
                return "green"
            case "assessment open":
                return "green"

        return "grey"

    @property
    def is_draft(self):
        return self.proto_draft is True
