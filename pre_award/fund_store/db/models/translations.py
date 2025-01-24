from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, Integer

from pre_award.db import db

BaseModel: DefaultMeta = db.Model


class Translation(BaseModel):
    content_id = Column(
        "content_id",
        Integer,
        primary_key=True,
        nullable=False,
    )
    language = Column("language", db.String(), nullable=False, unique=False, primary_key=True)
    text = Column("text", db.String(), nullable=False, unique=False)
