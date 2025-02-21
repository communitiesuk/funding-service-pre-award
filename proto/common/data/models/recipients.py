import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db

if TYPE_CHECKING:
    from proto.common.data.models import Fund
    from proto.common.data.models.applications import ProtoApplication


class GrantRecipientStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class ProtoGrantRecipient(db.Model):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    status: Mapped[GrantRecipientStatus] = mapped_column(index=True)

    funding_allocated: Mapped[int] = mapped_column(default=0)
    funding_paid: Mapped[int] = mapped_column(default=0)

    grant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fund.id"))
    grant: Mapped["Fund"] = relationship("Fund")

    application_id: Mapped[int | None] = mapped_column(ForeignKey("proto_application.id"), unique=True)
    application: Mapped[Optional["ProtoApplication"]] = relationship("ProtoApplication")
