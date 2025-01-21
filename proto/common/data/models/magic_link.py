import uuid
from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class MagicLink(db.Model):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str]
    path: Mapped[str]
    token: Mapped[str] = mapped_column(index=True, unique=True)
    used: Mapped[bool] = mapped_column(default=False)
    expires_date: Mapped[datetime] = mapped_column(server_default=func.now() + timedelta(hours=1))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
