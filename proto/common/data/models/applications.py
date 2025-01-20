import uuid
from enum import Enum
from typing import TYPE_CHECKING

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from proto.common.data.models.account import Account
else:
    Round = "Round"
    Account = "Account"

# Round = "Round"
from db import db
from proto.common.data.models.round import Round

# Base = declarative_base()
BaseModel: DefaultMeta = db.Model


class Language(Enum):
    en = 0
    cy = 1


class Status(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    SUBMITTED = 2
    COMPLETED = 3


# this will encapsulate the entire process through to an applicant becoming a
# grant recipient
# there's the chance that the uncompeted workflow will want to see applications immediately as they're created (potentially filtering for the ones that have started providing values)
# vs. competative funds that should only be able to see applications after the user has submitted them


# Steven _wants_ to use StrEnum but ran into a final hurdle making python upgrade to 3.11 work and can't be bothered
# class ProtoApplicationStatus(StrEnum):
class ProtoApplicationStatus(Enum):
    CREATED = "CREATED"
    APPLYING = "APPLYING"

    # this is the submitted state
    SUBMITTED = "SUBMITTED"
    CHANGES_REQUESTED = "CHANGES_RREQUESTED"
    AWARDED = "AWARDED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"


# Created -> Applying -> Submitted -> Awarded
#                        Submitted -> Rejected
#                        Submitted -> Closed
#                        Submitted -> Changes requested
#            Applying -> Changes Requested
# Created -> Applying -> Closed
# Created -> Closed


class Applications(BaseModel):
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    # foreign key accounts in
    # bring account model over
    # lookup applications by account
    # bring forms in
    # either rename or add something else form "forms", more specific name
    account_id = Column("account_id", UUID(), ForeignKey("account.id"), nullable=False)
    fund_id = Column("fund_id", db.String(), nullable=False)
    round_id = Column("round_id", UUID(), ForeignKey("round.id"), nullable=False)
    key = Column("key", db.String(), nullable=False)
    language = Column("language", ENUM(Language), nullable=True)
    reference = Column("reference", db.String(), nullable=False, unique=True)
    project_name = Column(
        "project_name",
        db.String(),
        nullable=True,
    )
    started_at = Column("started_at", DateTime(), server_default=func.now())
    status = Column("status", ENUM(Status), default="NOT_STARTED", nullable=False)
    date_submitted = Column("date_submitted", DateTime())
    last_edited = Column("last_edited", DateTime(), server_default=func.now())
    forms = relationship("Forms")
    feedbacks = relationship("Feedback")
    end_of_application_survey = relationship("EndOfApplicationSurveyFeedback")

    __table_args__ = (db.UniqueConstraint("fund_id", "round_id", "key", name="_reference"),)

    def as_dict(self):
        date_submitted = (
            (self.date_submitted if type(self.date_submitted) is str else self.date_submitted.isoformat())
            if self.date_submitted
            else "null"
        )
        return {
            "id": str(self.id),
            "account_id": self.account_id,
            "round_id": self.round_id,
            "fund_id": self.fund_id,
            "language": self.language.name if self.language else "en",
            "reference": self.reference,
            "project_name": self.project_name or None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "status": self.status.name if self.status else None,
            "last_edited": self.last_edited.isoformat()
            if self.last_edited
            else (self.started_at.isoformat() if self.started_at else None),
            "date_submitted": date_submitted,
        }

    proto_round: Mapped[Round] = relationship("Round")
    proto_account: Mapped[Account] = relationship("Account")

    proto_status = Column(SQLAlchemyEnum(ProtoApplicationStatus, name="protoapplicationstatus"))
    # this implies the fund, don't reference both! joining should be cheap here so we'll probably always return it

    # I think I'd prefer if this was somehow managed by updated_date but I can see why assessors would want to order by when the applicant submitted, for exmaple
    proto_updated_by_applicant_date = Column("proto_updated_by_applicant_date", DateTime(), server_default=func.now())

    proto_created_date = Column("proto_created_date", DateTime(), server_default=func.now())
    proto_updated_date = Column("proto_updated_date", DateTime(), server_default=func.now(), onupdate=func.now())
