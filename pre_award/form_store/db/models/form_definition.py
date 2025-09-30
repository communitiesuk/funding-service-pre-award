"""The module containing all code related to the `form_definition` table within
the Postgres db.

This table stores form configurations for both draft and published states.
"""

import re
import uuid
from typing import Any

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from pre_award.db import db

BaseModel: DefaultMeta = db.Model


def url_path_to_display_name(text: str) -> str:
    return re.sub(r"[-_]", " ", text).capitalize()


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
    url_path = Column(Text, unique=True, nullable=False)
    display_name = Column(Text, nullable=True)
    draft_json = Column(JSONB, nullable=False)
    published_json = Column(JSONB, nullable=False, default="{}")

    def as_dict(self) -> dict[str, Any]:
        """
        Convert FormDefinition to dictionary with metadata only (no JSON configurations).
        Use this for list endpoints where you don't need the full form JSON.
        """
        return {
            "id": str(self.id),
            "url_path": self.url_path,
            "display_name": self.display_name
            if self.display_name is not None
            else url_path_to_display_name(self.url_path),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "is_published": bool(self.published_json and self.published_json != {}),
        }

    def as_dict_with_draft_json(self) -> dict[str, Any]:
        """
        Return form metadata with draft configuration.
        Use this for GET /forms/{url_path}/draft endpoint.
        """
        result = self.as_dict()
        result["draft_json"] = self.draft_json
        return result

    def as_dict_with_published_json(self) -> dict[str, Any]:
        """
        Return form metadata with published configuration.
        Use this for GET /forms/{url_path}/published endpoint.
        """
        result = self.as_dict()
        result["published_json"] = self.published_json
        return result
