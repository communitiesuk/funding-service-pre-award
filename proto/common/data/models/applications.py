import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from account_store.db.models import Account
from db import db
from proto.common.data.models.types import pk_int

if TYPE_CHECKING:
    from proto.common.data.models import Organisation, ProtoGrantRecipient, Round
    from proto.common.data.models.data_collection import ProtoDataCollectionInstance


# SF notes: CREATED, SUBMITTED, AWARDED, REJECTED, CLOSED
class ApplicationStatus(str, enum.Enum):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    SUBMITTED = "submitted"
    CHANGE_REQUESTED = "change requested"
    COMPLETED = "completed"


class ApplicationSectionStatus(str, enum.Enum):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"


# please come up with a better name
class TestLiveStatus(str, enum.Enum):
    TEST = "TEST"
    LIVE = "LIVE"


class ProtoApplication(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    external_id: Mapped[uuid.UUID] = mapped_column(index=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    code: Mapped[str]
    fake: Mapped[bool]  # hack: true if this is a 'previewed' application (grant admin feature)

    round_id: Mapped[int] = mapped_column(ForeignKey("round.id"))
    round: Mapped["Round"] = relationship("Round")
    organisation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organisation.id"))
    organisation: Mapped["Organisation"] = relationship("Organisation")

    data_collection_instance_id: Mapped[pk_int] = mapped_column(ForeignKey("proto_data_collection_instance.id"))
    data_collection_instance: Mapped["ProtoDataCollectionInstance"] = relationship(
        "ProtoDataCollectionInstance", lazy="select"
    )

    submitted: Mapped[bool] = mapped_column(default=False)
    submitted_by_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("account.id"))
    submitted_by: Mapped[Account | None] = relationship("Account")

    # struggling to call this anything other than status
    test_live_status: Mapped[TestLiveStatus]

    updated_by_applicant_at: Mapped[datetime] = mapped_column(server_default=func.now())

    recipient: Mapped[Optional["ProtoGrantRecipient"]] = relationship(
        "ProtoGrantRecipient", back_populates="application"
    )

    @property
    def status(self):
        if len(self.data_collection_instance.section_data) == 0:
            return ApplicationStatus.NOT_STARTED

        return ApplicationStatus.SUBMITTED if self.submitted else ApplicationStatus.IN_PROGRESS

    @property
    def can_be_submitted(self):
        return len(self.data_collection_instance.section_data) == len(
            self.round.data_collection_definition.sections
        ) and all(sd.completed for sd in self.data_collection_instance.section_data)

    @property
    def not_started(self):
        return self.status == ApplicationStatus.NOT_STARTED

    @property
    def in_progress(self):
        return self.status == ApplicationStatus.IN_PROGRESS

    @property
    def is_submitted(self):
        return self.status == ApplicationStatus.SUBMITTED

    @property
    def completed(self):
        return self.status == ApplicationStatus.COMPLETED

    def status_for_section(self, section_id) -> ApplicationSectionStatus:
        section_data = next(
            filter(lambda sec: sec.section_id == section_id, self.data_collection_instance.section_data), None
        )
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
