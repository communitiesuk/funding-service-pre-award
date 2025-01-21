import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from proto.common.data.models.types import pk_int

if TYPE_CHECKING:
    from account_store.db.models import Account
    from proto.common.data.models import ApplicationSection, Round


# SF notes: CREATED, SUBMITTED, AWARDED, REJECTED, CLOSED
class ApplicationStatus(str, enum.Enum):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    CHANGE_REQUESTED = "change requested"
    COMPLETED = "completed"


class ApplicationSectionStatus(str, enum.Enum):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"


class ProtoApplication(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    code: Mapped[str]
    fake: Mapped[bool]  # hack: true if this is a 'previewed' application (grant admin feature)

    round_id: Mapped[int] = mapped_column(ForeignKey("round.id"))
    round: Mapped["Round"] = relationship("Round")
    account_id: Mapped[str] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = relationship("Account")

    section_data: Mapped[list["ProtoApplicationSectionData"]] = relationship(
        "ProtoApplicationSectionData", passive_deletes=True
    )

    updated_by_applicant_at: Mapped[datetime] = mapped_column(server_default=func.now())

    @property
    def status(self):
        if len(self.section_data) == 0:
            return ApplicationStatus.NOT_STARTED

        # TODO: WIP

        return ApplicationStatus.IN_PROGRESS

    @property
    def can_be_submitted(self):
        return len(self.section_data) == len(self.round.application_sections) and all(
            sd.completed for sd in self.section_data
        )

    @property
    def not_started(self):
        return self.status == ApplicationStatus.NOT_STARTED

    @property
    def in_progress(self):
        return self.status == ApplicationStatus.IN_PROGRESS

    @property
    def completed(self):
        return self.status == ApplicationStatus.COMPLETED

    def status_for_section(self, section_id) -> ApplicationSectionStatus:
        section_data = next(filter(lambda sec: sec.section_id == section_id, self.section_data), None)
        if section_data is None:
            return ApplicationSectionStatus.NOT_STARTED
        elif section_data.completed is False:
            return ApplicationSectionStatus.IN_PROGRESS
        return ApplicationSectionStatus.COMPLETED

    def section_not_started(self, section_id) -> bool:
        return self.status_for_section(section_id) == ApplicationSectionStatus.NOT_STARTED

    def section_in_progress(self, section_id) -> bool:
        return self.status_for_section(section_id) == ApplicationSectionStatus.IN_PROGRESS

    def section_completed(self, section_id) -> bool:
        return self.status_for_section(section_id) == ApplicationSectionStatus.COMPLETED


class ProtoApplicationSectionData(db.Model):
    __table_args__ = (UniqueConstraint("proto_application_id", "section_id"),)

    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    data: Mapped[dict] = mapped_column(nullable=False, default=dict)
    completed: Mapped[bool] = mapped_column(default=False)

    proto_application_id: Mapped[int] = mapped_column(ForeignKey("proto_application.id", ondelete="CASCADE"))
    proto_application: Mapped["Round"] = relationship("ProtoApplication")

    section_id: Mapped[int] = mapped_column(ForeignKey("application_section.id"))
    section: Mapped["ApplicationSection"] = relationship("ApplicationSection")
