import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Literal, Optional

from alembic_utils.pg_extension import PGExtension
from fsd_utils.simple_utils.date_utils import (
    current_datetime_after_given_iso_string,
    current_datetime_before_given_iso_string,
)
from sqlalchemy import ColumnElement, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.utils.date_time_utils import get_now_UK_time_without_tzinfo
from pre_award.common.locale_selector.get_lang import get_lang
from pre_award.db import FundingType, db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model

ltree_extension = PGExtension(
    schema="public",
    signature="ltree",
)
citext_extension = PGExtension(schema="public", signature="citext")


class Fund(Model):
    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True,
    )
    name_json: Mapped[dict[Literal["en", "cy"], str]]
    title_json: Mapped[dict[Literal["en", "cy"], str]]
    short_name: Mapped[str] = mapped_column(CITEXT, nullable=False, unique=True)
    description_json: Mapped[dict[Literal["en", "cy"], str]]
    rounds: Mapped[List["Round"]] = relationship("Round", back_populates="fund")
    welsh_available: Mapped[bool] = mapped_column(default=False, nullable=False)
    owner_organisation_name: Mapped[str]
    owner_organisation_shortname: Mapped[str]
    owner_organisation_logo_uri: Mapped[Optional[str]]
    funding_type: Mapped[FundingType] = mapped_column(
        Enum(
            FundingType,
            name="fundingtype",
            create_constraint=True,
            validate_strings=True,
        )
    )
    ggis_scheme_reference_number: Mapped[Optional[str]]

    @property
    def name(self) -> str:
        return self.name_json[get_lang()] or self.name_json["en"]

    @property
    def title(self) -> str:
        return self.title_json[get_lang()] or self.title_json["en"]


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
    fund: Mapped[Fund] = relationship(lazy=True, back_populates="rounds")
    title_json: Mapped[dict[Literal["en", "cy"], str]]
    short_name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    opens: Mapped[Optional[datetime]]  # In Europe/London timezone, stored without tzinfo
    deadline: Mapped[Optional[datetime]]  # In Europe/London timezone, stored without tzinfo
    assessment_start: Mapped[Optional[datetime]]  # In Europe/London timezone, stored without tzinfo
    application_reminder_sent: Mapped[bool] = mapped_column(default=False)
    reminder_date: Mapped[Optional[datetime]]  # In Europe/London timezone, stored without tzinfo
    send_incomplete_application_emails: Mapped[bool] = mapped_column(default=True, nullable=False)

    assessment_deadline: Mapped[Optional[datetime]]  # In Europe/London timezone, stored without tzinfo
    prospectus: Mapped[str]
    privacy_notice: Mapped[str]
    contact_email: Mapped[Optional[str]]
    instructions_json: Mapped[Optional[dict[str, str]]]
    feedback_link: Mapped[Optional[str]]
    project_name_field_id: Mapped[str]
    application_guidance_json: Mapped[Optional[dict[str, Any]]]
    guidance_url: Mapped[Optional[str]]
    all_uploaded_documents_section_available: Mapped[bool] = mapped_column(default=False)
    application_fields_download_available: Mapped[bool] = mapped_column(default=False)
    display_logo_on_pdf_exports: Mapped[bool] = mapped_column(default=False)
    mark_as_complete_enabled: Mapped[bool] = mapped_column(default=False)
    is_expression_of_interest: Mapped[bool] = mapped_column(default=False)
    feedback_survey_config: Mapped[Optional[dict[str, Any]]]
    eligibility_config: Mapped[Optional[dict[str, Any]]]
    eoi_decision_schema: Mapped[Optional[dict[str, Any]]]

    @hybrid_property
    def _is_past_submission_deadline(self) -> bool:
        if self.deadline:
            result = current_datetime_after_given_iso_string(self.deadline.isoformat())
            return bool(result)
        return False

    @_is_past_submission_deadline.expression
    def is_past_submission_deadline(cls) -> ColumnElement[bool]:
        return func.timezone("Europe/London", func.now()) > cls.deadline

    @hybrid_property
    def _is_not_yet_open(self) -> bool:
        if self.opens:
            result = current_datetime_before_given_iso_string(self.opens.isoformat())
            return bool(result)
        return False

    @_is_not_yet_open.expression
    def is_not_yet_open(cls) -> ColumnElement[bool]:
        return func.timezone("Europe/London", func.now()) < cls.opens

    @hybrid_property
    def _is_open(self) -> bool:
        return (
            self.opens < get_now_UK_time_without_tzinfo() < self.deadline if (self.deadline and self.opens) else False
        )

    @_is_open.expression
    def is_open(cls) -> ColumnElement[bool]:
        return cls.opens < func.timezone("Europe/London", func.now()) < cls.deadline

    @property
    def title(self) -> str | None:
        if not self.title_json:
            return None
        return self.title_json[get_lang()] or self.title_json["en"]

    @property
    def instructions(self) -> str | None:
        if not self.instructions_json:
            return None

        return self.instructions_json.get(get_lang(), self.instructions_json.get("en"))
