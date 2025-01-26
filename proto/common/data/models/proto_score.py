import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apply.models.account import Account
from db import db

if TYPE_CHECKING:
    from account_store.db.models import Account
    from proto.common.data.models.applications import ProtoApplication
    from proto.common.data.models.data_collection import ProtoDataCollectionInstanceSectionData


class ProtoScore(db.Model):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = relationship("Account")

    application_id: Mapped[int] = mapped_column(ForeignKey("proto_application.id"))
    application: Mapped["ProtoApplication"] = relationship("ProtoApplication")

    section_id: Mapped[int] = mapped_column(ForeignKey("proto_data_collection_instance_section_data.id"))
    section: Mapped["ProtoDataCollectionInstanceSectionData"] = relationship("ProtoDataCollectionInstanceSectionData")

    score: Mapped[int]
    reason: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
