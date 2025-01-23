from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from proto.common.data.models import ProtoDataCollectionSection
from proto.common.data.models.types import pk_int


class ProtoDataCollection(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    section_data: Mapped[list["ProtoDataCollectionSectionData"]] = relationship(
        "ProtoDataCollectionSectionData", passive_deletes=True, back_populates="data_collection"
    )


class ProtoDataCollectionSectionData(db.Model):
    __table_args__ = (UniqueConstraint("data_collection_id", "section_id"),)

    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    data: Mapped[dict] = mapped_column(nullable=False, default=dict)
    completed: Mapped[bool] = mapped_column(default=False)

    data_collection_id: Mapped[pk_int] = mapped_column(db.ForeignKey("proto_data_collection.id"))
    data_collection: Mapped[ProtoDataCollection] = relationship("ProtoDataCollection", back_populates="section_data")

    section_id: Mapped[int] = mapped_column(ForeignKey("proto_data_collection_section.id"))
    section: Mapped["ProtoDataCollectionSection"] = relationship("ProtoDataCollectionSection")
