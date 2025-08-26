"""The module containing all code related to the `form_definition` table within
the Postgres db.

This table stores form configurations for both draft and published states.
"""

import uuid

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from pre_award.db import db

BaseModel: DefaultMeta = db.Model


class FormDefinition(BaseModel):
    """FormDefinition
    The SQLAlchemy model class used to define the `form_definition` table
    in the Postgres database.

    This table is part of the new forms architecture, enabling a centralised
    store for both draft and published form configurations.
    """

    __tablename__ = "form_definition"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    # pylint: disable=not-callable
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    published_at = Column(DateTime, nullable=True)
    name = Column(Text, unique=True, nullable=False)
    draft_json = Column(JSONB, nullable=False)
    published_json = Column(JSONB, nullable=False, default="{}")
