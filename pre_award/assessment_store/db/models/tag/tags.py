import re
import uuid

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, ForeignKey, Index, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.event import listens_for
from sqlalchemy.orm import relationship, validates

from db import db

BaseModel: DefaultMeta = db.Model


class Tag(BaseModel):
    __tablename__ = "tags"
    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )
    value = Column(
        db.String(255),
        nullable=False,
        unique=False,
    )
    active = Column(db.Boolean(), nullable=False, default=True)
    type_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "tag_types.id",
        ),
        nullable=False,
    )
    fund_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )
    round_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )
    creator_user_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )
    created_at = Column(db.DateTime(timezone=True), server_default=func.now())
    # last_edited_user_id = Column(
    #     UUID(as_uuid=True),
    #     nullable=False,
    # )
    # last_edited = Column(db.DateTime(timezone=True), server_default=func.now())
    tag_type = relationship("TagType", lazy="selectin")
    __table_args__ = (
        Index(
            "tag_value_round_id_ix",
            text("lower(value)"),
            "round_id",
            unique=True,
        ),
    )

    def __repr__(self):
        return f"<Tag {self.value}>"

    @validates("value")
    def validate_value(self, key, value):
        # Remove leading and trailing whitespace
        value = value.strip()

        # Define the pattern using a regular expression
        pattern = r"^[\'\-\w\s]+$"

        # Check if the value matches the pattern
        if not re.match(pattern, value):
            raise ValueError(
                "Invalid value. The value should only contain apostrophes, hyphens, letters, digits, and spaces."
            )

        return value


@listens_for(Tag, "before_insert")
@listens_for(Tag, "before_update")
def validate_tag(mapper, connection, target):
    # Trigger attribute-level validation only for the 'value' column
    value = target.value
    target.validate_value("value", value)
