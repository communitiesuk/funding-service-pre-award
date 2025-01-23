import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from proto.common.data.models.types import pk_int

if TYPE_CHECKING:
    from account_store.db.models import Account
    from proto.common.data.models import Round
    from proto.common.data.models.data_collection import ProtoDataCollection


class ReportStatus(str, enum.Enum):
    CREATED = "created"
    PENDING_SIGN_OFF = "pending sign off"  # section 151
    SUBMITTED = "submitted"
    CLOSED = "closed"


class ReportSectionStatus(str, enum.Enum):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"


class ProtoReport(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    code: Mapped[str]
    fake: Mapped[bool]  # hack: true if this is a 'previewed' application (grant admin feature)

    round_id: Mapped[int] = mapped_column(ForeignKey("round.id"))
    round: Mapped["Round"] = relationship("Round")
    account_id: Mapped[str] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = relationship("Account")

    data_collection_id: Mapped[pk_int] = mapped_column(ForeignKey("proto_data_collection.id"))
    data_collection: Mapped["ProtoDataCollection"] = relationship("ProtoDataCollection", lazy="select")

    updated_by_reporter_at: Mapped[datetime] = mapped_column(server_default=func.now())

    @property
    def status(self):
        if len(self.data_collection.section_data) == 0:
            return ReportSectionStatus.NOT_STARTED

        # TODO: WIP

        return ReportSectionStatus.IN_PROGRESS

    @property
    def can_be_submitted(self):
        return len(self.data_collection.section_data) == len(self.round.application_sections) and all(
            sd.completed for sd in self.data_collection.section_data
        )

    @property
    def not_started(self):
        return self.status == ReportSectionStatus.NOT_STARTED

    @property
    def in_progress(self):
        return self.status == ReportSectionStatus.IN_PROGRESS

    @property
    def completed(self):
        return self.status == ReportSectionStatus.COMPLETED

    def status_for_section(self, section_id) -> ReportSectionStatus:
        section_data = next(filter(lambda sec: sec.section_id == section_id, self.data_collection.section_data), None)
        if section_data is None:
            return ReportSectionStatus.NOT_STARTED
        elif section_data.completed is False:
            return ReportSectionStatus.IN_PROGRESS
        return ReportSectionStatus.COMPLETED

    def section_not_started(self, section_id) -> bool:
        return self.status_for_section(section_id) == ReportSectionStatus.NOT_STARTED

    def section_in_progress(self, section_id) -> bool:
        return self.status_for_section(section_id) == ReportSectionStatus.IN_PROGRESS

    def section_completed(self, section_id) -> bool:
        return self.status_for_section(section_id) == ReportSectionStatus.COMPLETED
