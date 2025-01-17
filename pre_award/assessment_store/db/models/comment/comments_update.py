"""The module containing all code related to the `comments` table within the
Postgres db."""

import uuid

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID

from db import db


class CommentsUpdate(db.Model):
    """CommentsUpdate The sqlalchemy-flask model class used to define the
    `comments_update` table in the Postgres database."""

    __tablename__ = "comments_update"

    id = Column("id", UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    comment_id = Column(
        "comment_id",
        UUID(as_uuid=True),
        ForeignKey("comments.comment_id"),
    )

    comment = Column("comment", db.Text(), nullable=False)

    date_created = Column("date_created", db.DateTime(), server_default=func.now())
