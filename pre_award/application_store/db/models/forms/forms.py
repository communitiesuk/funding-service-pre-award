import uuid

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy_json import NestedMutableJson
from sqlalchemy_utils.types import UUIDType

from pre_award.application_store.db.models.application.applications import Applications
from pre_award.application_store.db.models.forms.enums import Status
from pre_award.db import db

BaseModel: DefaultMeta = db.Model


class Forms(BaseModel):
    __table_args__ = (db.UniqueConstraint("id", "name"),)
    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    application_id = db.Column("application_id", db.ForeignKey(Applications.id, ondelete="CASCADE"), nullable=False)
    application = db.relationship("Applications", back_populates="forms")
    json = db.Column("json", NestedMutableJson)
    status = db.Column("status", db.Enum(Status), default="NOT_STARTED", nullable=False)
    name = db.Column("name", db.String(), nullable=False)
    has_completed = db.Column("has_completed", db.Boolean(), default=False)

    def as_json(self):
        return {
            "status": self.status.name,
            "name": self.name,
            "questions": self.json,
        }
