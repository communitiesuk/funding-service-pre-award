import enum
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import CheckConstraint, UniqueConstraint, func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from db import db
from proto.common.data.models import t_data_source

if TYPE_CHECKING:
    from proto.common.data.models.round import Round


class DataStandard(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    slug: Mapped[str] = mapped_column(unique=True)

    description: Mapped[str]

    def __repr__(self) -> str:
        return f"<DS: {self.description}>"


# Whether the sections/questions are associated with applications for funding or reporting (monitoring+evaluation) of
# funding.
class TemplateType(enum.Enum):
    APPLICATION = "application"
    REPORTING = "reporting"


class TemplateSection(db.Model):
    __table_args__ = (CheckConstraint(r"regexp_like(slug, '[a-z\-]+')", name="slug"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
    slug: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    order: Mapped[int]
    type: Mapped[TemplateType]

    template_questions: Mapped[list["TemplateQuestion"]] = relationship(
        "TemplateQuestion", back_populates="template_section"
    )

    def __repr__(self):
        return self.slug


class QuestionType(str, enum.Enum):
    TEXT_INPUT = "text input"
    TEXTAREA = "text area"
    RADIOS = "radio"


class TemplateQuestion(db.Model):
    __table_args__ = (
        CheckConstraint(r"regexp_like(slug, '[a-z\-]+')", name="slug"),
        UniqueConstraint("template_section_id", "slug", name="uq_tq_slug_for_section"),
        UniqueConstraint("template_section_id", "order", name="uq_tq_order_for_section"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    slug: Mapped[str]
    type: Mapped[QuestionType]
    title: Mapped[str]
    hint: Mapped[str | None]
    order: Mapped[int]
    data_source: Mapped[t_data_source]

    template_section_id: Mapped[int] = mapped_column(db.ForeignKey(TemplateSection.id))
    template_section: Mapped[TemplateSection] = relationship(TemplateSection, back_populates="template_questions")
    data_standard_id: Mapped[int | None] = mapped_column(db.ForeignKey(DataStandard.id))
    data_standard: Mapped[DataStandard | None] = relationship(DataStandard)

    def __repr__(self):
        return f"<TemplateQuestion {self.slug} template_section={self.template_section}>"


class ProtoDataCollectionSection(db.Model):
    __table_args__ = (
        CheckConstraint(r"regexp_like(slug, '[a-z\-]+')", name="slug"),
        UniqueConstraint("round_id", "slug", name="uq_as_slug_for_round2"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
    slug: Mapped[str]
    title: Mapped[str]
    order: Mapped[int]

    round_id: Mapped[UUID] = mapped_column(db.ForeignKey("round.id"))
    round: Mapped["Round"] = relationship("Round", back_populates="application_sections")

    questions: Mapped[list["ProtoDataCollectionQuestion"]] = relationship(
        "ProtoDataCollectionQuestion", order_by="ProtoDataCollectionQuestion.order"
    )

    def __repr__(self):
        return f"<ProtoDataCollectionSection {self.slug} fund={self.round.proto_grant.short_name}>"


class ProtoDataCollectionQuestion(db.Model):
    __table_args__ = (
        CheckConstraint(r"regexp_like(slug, '[a-z\-]+')", name="slug"),
        UniqueConstraint("section_id", "slug", name="uq_aq_slug_for_section2"),
        UniqueConstraint("section_id", "order", name="uq_aq_order_for_section2"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    slug: Mapped[str]
    type: Mapped[QuestionType]
    title: Mapped[str]
    hint: Mapped[str | None]
    order: Mapped[int]
    data_source: Mapped[t_data_source]

    section_id: Mapped[int] = mapped_column(db.ForeignKey(ProtoDataCollectionSection.id))
    section: Mapped[ProtoDataCollectionSection] = relationship(ProtoDataCollectionSection, back_populates="questions")
    template_question_id: Mapped[int | None] = mapped_column(db.ForeignKey(TemplateQuestion.id))
    template_question: Mapped[TemplateQuestion] = relationship(TemplateQuestion)
    data_standard_id: Mapped[int | None] = mapped_column(db.ForeignKey(DataStandard.id))
    data_standard: Mapped[DataStandard | None] = relationship(DataStandard)

    def __repr__(self):
        return f"<ProtoDataCollectionQuestion {self.slug} section={self.section}>"
