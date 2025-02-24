import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class Organisation(db.Model):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    name: Mapped[str]

    # Proto shortcut - would be more flexible in reality
    domain: Mapped[str]
