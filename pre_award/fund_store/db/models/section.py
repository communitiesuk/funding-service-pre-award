from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import JSON, Column, ForeignKey, Index, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import foreign, relationship, remote
from sqlalchemy_utils import LtreeType

from pre_award.db import db

BaseModel: DefaultMeta = db.Model


# section_field_table = Table(
#     "section_field",
#     metadata,
#     Column("section_id", ForeignKey("section.id"), primary_key=True),
#     Column("field_id", ForeignKey("assessment_field.id"), primary_key=True),
#     Column("display_order", Integer, nullable=False, unique=False),
# )


class SectionField(BaseModel):
    __tablename__ = "section_field"
    section_id = Column(ForeignKey("section.id"), primary_key=True)
    field_id = Column(ForeignKey("assessment_field.id"), primary_key=True)
    display_order = Column("display_order", Integer, nullable=False, unique=False)
    field = relationship("AssessmentField")


class AssessmentField(BaseModel):
    id = Column(db.String, primary_key=True, nullable=False, unique=True)
    field_type = Column(
        "field_type",
        db.String(),
        nullable=False,
        unique=False,
    )
    display_type = Column("display_type", db.String(), nullable=False, unique=False)
    title = Column("title", db.String(), nullable=False, unique=False)
    # sections = relationship(
    #     "Section", secondary=section_field_table, back_populates="fields"
    # )


class Section(BaseModel):
    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        nullable=False,
    )
    title_json = Column(
        "title_json",
        JSON(none_as_null=True),
        nullable=False,
        unique=False,
    )
    requires_feedback = Column(
        "requires_feedback",
        db.Boolean,
        default=False,
        nullable=False,
    )

    # title_content_id = mapped_column(Integer, nullable=True)
    # title_translations = relationship("Translation", primaryjoin=
    # "Section.title_content_id == Translation.content_id", viewonly=True)
    # title_translations = relationship("Translation",
    # primaryjoin="and_(foreign(
    # Section.title_content_id) == Translation.content_id,
    # Translation.language.like('%'))",
    # viewonly=True)
    round_id = Column(
        UUID(as_uuid=True),
        ForeignKey("round.id"),
        nullable=False,
    )
    weighting = Column(
        Integer,
        nullable=True,
    )
    path = Column(LtreeType, nullable=False)
    __table_args__ = (Index("ix_sections_path", path, postgresql_using="gist"),)
    fields = relationship("SectionField", order_by=SectionField.display_order, viewonly=True)
    # fields = relationship(
    #     "AssessmentField",
    #     secondary=section_field_table,
    #     back_populates="sections",
    # )
    parent = relationship(
        "Section",
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref="children",
        viewonly=True,
        order_by="Section.path",
    )

    form_name = relationship("FormName")

    def __str__(self):
        return self.title_json.get("en")

    def __repr__(self):
        return "Section({})".format(self.title_json)
