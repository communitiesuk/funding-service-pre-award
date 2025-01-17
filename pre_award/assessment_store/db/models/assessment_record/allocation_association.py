from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from db import db

BaseModel: DefaultMeta = db.Model


class AllocationAssociation(BaseModel):
    """This class represents the association between an application and a user in
    the database. Each instance of this class links a specific application to a
    specific user, including metadata about when the association was created, its
    current active status, and a log of changes.

    Attributes:
        application_id: UUID of the application, serving as a foreign key to the assessment_records table.
        user_id: UUID of the user associated with the application.
        assigner_id: UUID of the user creating the association (usually the lead assessor).
        created_at: Timestamp of when the association was created, defaulting to the current time.
        active: Boolean indicating whether the association is active, defaulting to True.
        log: JSONB object containing a log of changes made to the association.

    Table constraints:
        The primary key is a composite key consisting of application_id and user_id, ensuring that
        each user can be associated with a specific application only once.

    """

    __tablename__ = "allocation_association"
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "assessment_records.application_id",
        ),
        nullable=False,
    )
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    assigner_id = db.Column(UUID(as_uuid=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    active = db.Column(db.Boolean(), nullable=False, default=True)
    log = db.Column(JSONB, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint("application_id", "user_id"),)
