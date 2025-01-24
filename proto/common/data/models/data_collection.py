from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from proto.common.data.models import DataStandard, Round, TemplateQuestion, t_data_source
from proto.common.data.models.question_bank import QuestionType
from proto.common.data.models.types import pk_int


class ProtoDataCollectionDefinition(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    round: Mapped[Optional["Round"]] = relationship("Round", back_populates="data_collection_definition")
    sections: Mapped[Optional[list["ProtoDataCollectionDefinitionSection"]]] = relationship(
        "ProtoDataCollectionDefinitionSection", back_populates="definition"
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

    section_id: Mapped[int] = mapped_column(db.ForeignKey(ProtoDataCollectionDefinitionSection.id))
    section: Mapped[ProtoDataCollectionDefinitionSection] = relationship(
        ProtoDataCollectionDefinitionSection, back_populates="questions"
    )
    template_question_id: Mapped[int | None] = mapped_column(db.ForeignKey(TemplateQuestion.id))
    template_question: Mapped[TemplateQuestion] = relationship(TemplateQuestion)
    data_standard_id: Mapped[int | None] = mapped_column(db.ForeignKey(DataStandard.id))
    data_standard: Mapped[DataStandard | None] = relationship(DataStandard)

    def __repr__(self):
        return f"<ProtoDataCollectionDefinitionQuestion {self.slug} section={self.section}>"


class ProtoDataCollectionInstance(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

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
