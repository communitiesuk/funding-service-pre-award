import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, UniqueConstraint, func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from db import db
from proto.common.data.models import t_data_source
from proto.common.data.models.types import pk_int

if TYPE_CHECKING:
    pass


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
    TEXT_INPUT = "TEXT_INPUT"
    TEXTAREA = "TEXTAREA"
    RADIOS = "RADIOS"
    NUMBER = "NUMBER"
    POUNDS_AND_PENCE = "POUNDS_AND_PENCE"

    # this shouldn't be a question type, need to work
    # out how this relates to radios/ checkboxes/ selects/ etc.
    # could use an internal list of data or a reference
    LIST_AUTOCOMPLETE = "LIST_AUTOCOMPLETE"


class ValidationType(str, enum.Enum):
    GREATER_THAN = "Greater than"
    LESS_THAN = "Less than"
    EQUAL_TO = "Equal to"


class ConditionCombination(str, enum.Enum):
    AND = "and"  # All conditions that apply to this question must evaluate to 'True' in order to show it
    OR = "or"  # Any single condition that applies to this question must evaluate to 'True' in order to show it


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

    reference_data_source_id: Mapped[pk_int] = mapped_column(db.ForeignKey("data_store.id"), nullable=True)
    reference_data_source: Mapped["DataStore"] = relationship("DataStore")  # noqa

    template_section_id: Mapped[int] = mapped_column(db.ForeignKey(TemplateSection.id))
    template_section: Mapped[TemplateSection] = relationship(TemplateSection, back_populates="template_questions")
    data_standard_id: Mapped[int | None] = mapped_column(db.ForeignKey(DataStandard.id))
    data_standard: Mapped[DataStandard | None] = relationship(DataStandard)

    conditions: Mapped[list["TemplateQuestionCondition"]] = relationship(
        primaryjoin="TemplateQuestion.id==TemplateQuestionCondition.question_id",
    )
    validations: Mapped[list["TemplateValidation"]] = relationship(
        primaryjoin="TemplateQuestion.id==TemplateValidation.question_id"
    )

    dependent_conditions: Mapped[list["TemplateQuestionCondition"]] = relationship(
        primaryjoin="TemplateQuestion.id==TemplateQuestionCondition.depends_on_question_id",
    )
    condition_combination_type: Mapped[Optional[ConditionCombination]] = mapped_column(default=ConditionCombination.AND)

    def __repr__(self):
        return f"<TemplateQuestion {self.slug} template_section={self.template_section}>"


# opted to just copy this here for now following precedent
# we could decide if theres any de-duping we want to do around these
# when they're all in
class TemplateQuestionCondition(db.Model):
    __table_args__ = ()
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    question_id: Mapped[int] = mapped_column(db.ForeignKey(TemplateQuestion.id))
    question: Mapped["TemplateQuestion"] = relationship(
        "TemplateQuestion", back_populates="conditions", foreign_keys=[question_id]
    )

    depends_on_question_id: Mapped[int] = mapped_column(db.ForeignKey(TemplateQuestion.id), nullable=True)
    depends_on_question: Mapped["TemplateQuestion"] = relationship(
        "TemplateQuestion",
        back_populates="dependent_conditions",
        foreign_keys=[depends_on_question_id],
    )
    # depends_on_section_id: Mapped[int] = mapped_column(db.ForeignKey(TemplateSection.id), nullable=True)
    # depends_on_section: Mapped["TemplateQuestion"] = relationship(
    #     "TemplateSection",
    #     #back_populates="dependent_conditions",
    #     foreign_keys=[depends_on_section_id],
    # )

    criteria: Mapped[dict] = mapped_column(nullable=False, default=dict)
    expression: Mapped[str]


class TemplateValidation(db.Model):
    __table_args__ = ()
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    question_id: Mapped[int] = mapped_column(db.ForeignKey(TemplateQuestion.id))
    question: Mapped["TemplateQuestion"] = relationship(
        "TemplateQuestion", back_populates="validations", foreign_keys=[question_id]
    )

    depends_on_question_id: Mapped[int] = mapped_column(db.ForeignKey(TemplateQuestion.id), nullable=True)
    depends_on_question: Mapped["TemplateQuestion"] = relationship(
        "TemplateQuestion",
        foreign_keys=[depends_on_question_id],
    )

    # validations stacked in db order - they probably want an order of precednece similar to questions and sections
    expression: Mapped[str]
    message: Mapped[str]

    options: Mapped[dict] = mapped_column(nullable=False, default=dict)
