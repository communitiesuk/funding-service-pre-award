import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from proto.common.data.models.types import pk_int

if TYPE_CHECKING:
    from proto.common.data.models import ProtoDataCollectionDefinition
    from proto.common.data.models.fund import Fund


class ProtoReportingRound(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    external_id: Mapped[uuid.UUID] = mapped_column(index=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    preview: Mapped[bool] = mapped_column(default=True)

    reporting_period_starts: Mapped[datetime]
    reporting_period_ends: Mapped[datetime]
    submission_period_starts: Mapped[datetime]
    submission_period_ends: Mapped[datetime]

    grant_id: Mapped[UUID] = mapped_column(ForeignKey("fund.id"))
    grant: Mapped["Fund"] = relationship()

    data_collection_definition_id: Mapped[pk_int | None] = mapped_column(
        ForeignKey("proto_data_collection_definition.id")
    )
    data_collection_definition: Mapped[Optional["ProtoDataCollectionDefinition"]] = relationship(
        "ProtoDataCollectionDefinition", back_populates="reporting_round"
    )

    # Only one reporting round allowed to exist in preview state at a time.
    __table_args__ = (Index("only_one_preview_round", "preview", unique=True, postgresql_where=preview.is_(True)),)

    def __repr__(self):
        return f"<ReportingRound {self.external_id}>"

    @property
    def title(self):
        return (
            self.reporting_period_starts.strftime("%d %B %Y") + " - " + self.reporting_period_ends.strftime("%d %B %Y")
        )

    @property
    def status(self):
        today = datetime.today()

        if self.preview:
            return "in preview"

        if today < self.submission_period_starts:
            return "waiting to open"

        if today < self.submission_period_ends:
            return "open"

        return "closed"

    @property
    def status_colour(self):
        # Design system tag colours: https://design-system.service.gov.uk/components/tag/#additional-colours
        match self.status:
            case "in preview":
                return "orange"
            case "waiting to open":
                return "yellow"
            case "open":
                return "green"

        return "grey"

    @property
    def is_draft(self):
        return self.preview is True
