import uuid

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import db

BaseModel: DefaultMeta = db.Model


class TagAssociation(BaseModel):
    __tablename__ = "tag_association"
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "assessment_records.application_id",
        ),
    )
    associated = db.Column(db.Boolean(), nullable=False, default=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"))
    user_id = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    tag = relationship("Tag")
