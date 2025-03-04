from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from proto.common.data.models import (
    DataStandard,
    ProtoApplication,
    ProtoReportingRound,
    Round,
    TemplateQuestion,
    TemplateSection,
    t_data_source,
)
from proto.common.data.models.proto_score import ProtoScore
from proto.common.data.models.question_bank import ConditionCombination, QuestionType
from proto.common.data.models.types import pk_int

if TYPE_CHECKING:
    from proto.common.data.models import ProtoReport


class ProtoDataCollectionDefinition(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    round: Mapped[Optional["Round"]] = relationship("Round", back_populates="data_collection_definition")
    reporting_round: Mapped[Optional["ProtoReportingRound"]] = relationship(
        "ProtoReportingRound", back_populates="data_collection_definition"
    )
    sections: Mapped[Optional[list["ProtoDataCollectionDefinitionSection"]]] = relationship(
        "ProtoDataCollectionDefinitionSection",
        back_populates="definition",
        order_by="ProtoDataCollectionDefinitionSection.order",
    )


class ProtoDataCollectionDefinitionSection(db.Model):
    __table_args__ = (
        CheckConstraint(r"regexp_like(slug, '[a-z\-]+')", name="slug"),
        UniqueConstraint("definition_id", "slug", name="uq_as_slug_for_definition"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
    slug: Mapped[str]
    title: Mapped[str]
    order: Mapped[int]

    definition_id: Mapped[pk_int] = mapped_column(db.ForeignKey("proto_data_collection_definition.id"))
    definition: Mapped["ProtoDataCollectionDefinition"] = relationship(
        "ProtoDataCollectionDefinition", back_populates="sections"
    )

    questions: Mapped[list["ProtoDataCollectionDefinitionQuestion"]] = relationship(
        "ProtoDataCollectionDefinitionQuestion", order_by="ProtoDataCollectionDefinitionQuestion.order"
    )
    template_section_id: Mapped[int | None] = mapped_column(db.ForeignKey(TemplateSection.id))
    template_section: Mapped[TemplateSection] = relationship(TemplateSection, lazy="select")

    def __repr__(self):
        return f"<ProtoDataCollectionDefinitionSection {self.slug}>"


class ProtoDataCollectionDefinitionQuestion(db.Model):
    __table_args__ = (
        CheckConstraint(r"regexp_like(slug, '[a-z\-]+')", name="slug"),
        UniqueConstraint("section_id", "slug", name="uq_aq_slug_for_section3"),
        UniqueConstraint("section_id", "order", name="uq_aq_order_for_section3"),
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

    # question list types will either be able to define their own more ad-hoc data (like "Yes", "No")
    # or reference something managed by the platform or the grant team
    reference_data_source_id: Mapped[pk_int] = mapped_column(db.ForeignKey("data_store.id"), nullable=True)
    reference_data_source: Mapped["DataStore"] = relationship("DataStore")

    section_id: Mapped[int] = mapped_column(db.ForeignKey(ProtoDataCollectionDefinitionSection.id))
    section: Mapped[ProtoDataCollectionDefinitionSection] = relationship(
        ProtoDataCollectionDefinitionSection, back_populates="questions"
    )
    template_question_id: Mapped[int | None] = mapped_column(db.ForeignKey(TemplateQuestion.id))
    template_question: Mapped[TemplateQuestion] = relationship(TemplateQuestion)
    data_standard_id: Mapped[int | None] = mapped_column(db.ForeignKey(DataStandard.id))
    data_standard: Mapped[DataStandard | None] = relationship(DataStandard)

    conditions: Mapped[list["ProtoDataCollectionQuestionCondition"]] = relationship(
        primaryjoin="ProtoDataCollectionDefinitionQuestion.id==ProtoDataCollectionQuestionCondition.question_id",
    )
    validations: Mapped[list["ProtoDataCollectionQuestionValidation"]] = relationship(
        primaryjoin="ProtoDataCollectionDefinitionQuestion.id==ProtoDataCollectionQuestionValidation.question_id"
    )

    dependent_conditions: Mapped[list["ProtoDataCollectionQuestionCondition"]] = relationship(
        primaryjoin="ProtoDataCollectionDefinitionQuestion.id==ProtoDataCollectionQuestionCondition.depends_on_question_id",
    )
    condition_combination_type: Mapped[Optional[ConditionCombination]] = mapped_column(default=ConditionCombination.AND)

    def __repr__(self):
        return f"<ProtoDataCollectionDefinitionQuestion {self.slug} section={self.section}>"


class ProtoDataCollectionQuestionCondition(db.Model):
    __table_args__ = ()
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    question_id: Mapped[int] = mapped_column(db.ForeignKey(ProtoDataCollectionDefinitionQuestion.id))
    question: Mapped["ProtoDataCollectionDefinitionQuestion"] = relationship(
        "ProtoDataCollectionDefinitionQuestion", back_populates="conditions", foreign_keys=[question_id]
    )

    depends_on_question_id: Mapped[int] = mapped_column(
        db.ForeignKey(ProtoDataCollectionDefinitionQuestion.id), nullable=True
    )
    depends_on_question: Mapped["ProtoDataCollectionDefinitionQuestion"] = relationship(
        "ProtoDataCollectionDefinitionQuestion",
        back_populates="dependent_conditions",
        foreign_keys=[depends_on_question_id],
    )

    criteria: Mapped[dict] = mapped_column(nullable=False, default=dict)
    expression: Mapped[str]


# some validations will be a core part of question metadata (i.e is required)
# some validations will come along with the question type? (i.e is a valid date)
# additional validations will be added here
class ProtoDataCollectionQuestionValidation(db.Model):
    __table_args__ = ()
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    question_id: Mapped[int] = mapped_column(db.ForeignKey(ProtoDataCollectionDefinitionQuestion.id))
    question: Mapped["ProtoDataCollectionDefinitionQuestion"] = relationship(
        "ProtoDataCollectionDefinitionQuestion", back_populates="validations", foreign_keys=[question_id]
    )

    # these are optional, if they're not defined your answer context is your own, if they are you have access to
    # both your answer and the answer you reference - we _very_ likely want to be able to validate across
    # multiple question contexts
    # someone can think this through one day
    depends_on_question_id: Mapped[int] = mapped_column(
        db.ForeignKey(ProtoDataCollectionDefinitionQuestion.id), nullable=True
    )
    depends_on_question: Mapped["ProtoDataCollectionDefinitionQuestion"] = relationship(
        "ProtoDataCollectionDefinitionQuestion",
        foreign_keys=[depends_on_question_id],
    )

    # validations stacked in db order - they probably want an order of precednece similar to questions and sections
    expression: Mapped[str]
    message: Mapped[str]

    options: Mapped[dict] = mapped_column(nullable=False, default=dict)


class ProtoDataCollectionInstance(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    application: Mapped[ProtoApplication | None] = relationship(
        ProtoApplication, back_populates="data_collection_instance"
    )
    report: Mapped[Optional["ProtoReport"]] = relationship("ProtoReport", back_populates="data_collection_instance")

    section_data: Mapped[list["ProtoDataCollectionInstanceSectionData"]] = relationship(
        "ProtoDataCollectionInstanceSectionData", passive_deletes=True, back_populates="instance"
    )


class ProtoDataCollectionInstanceSectionData(db.Model):
    __table_args__ = (UniqueConstraint("instance_id", "section_id"),)

    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    data: Mapped[dict] = mapped_column(nullable=False, default=dict)
    completed: Mapped[bool] = mapped_column(default=False)

    instance_id: Mapped[pk_int] = mapped_column(db.ForeignKey("proto_data_collection_instance.id"))
    instance: Mapped[ProtoDataCollectionInstance] = relationship(
        "ProtoDataCollectionInstance", back_populates="section_data"
    )

    section_id: Mapped[int] = mapped_column(ForeignKey("proto_data_collection_definition_section.id"))
    section: Mapped["ProtoDataCollectionDefinitionSection"] = relationship("ProtoDataCollectionDefinitionSection")

    # I'm fairly confident backref is deprecated and should be more formally defined with `back_populates` but
    # this loads and I said i'd push in 15 minutes
    scores: Mapped[List["ProtoScore"]] = relationship("ProtoScore", backref="proto_score")


# for now assuming a simple key: value pair of id: human readable label
class DataStore(db.Model):
    __table_args__ = ()

    id: Mapped[pk_int] = mapped_column(primary_key=True)

    # calling this name maybe interefered with sql alchemy comparator?
    # no it wasn't that
    collection_name: Mapped[str]

    version: Mapped[int] = mapped_column(default=1)

    data: Mapped[list["DataStoreEntry"]] = relationship("DataStoreEntry", back_populates="data_store")

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())


class DataStoreEntry(db.Model):
    __table_args__ = ()

    id: Mapped[pk_int] = mapped_column(primary_key=True)

    data_store_id: Mapped[pk_int] = mapped_column(db.ForeignKey("data_store.id"))
    data_store: Mapped["DataStore"] = relationship("DataStore", back_populates="data")

    value: Mapped[str]
    label: Mapped[str]

    version: Mapped[int] = mapped_column(default=1)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
