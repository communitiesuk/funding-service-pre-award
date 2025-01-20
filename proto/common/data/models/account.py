import uuid  # noqa
from typing import Mapping

from flask import current_app
from fsd_utils.authentication.utils import get_highest_role_map
from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Account(db.Model):
    id = db.Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )
    email = db.Column("email", db.String(), nullable=False, unique=True)
    full_name = db.Column("full_name", db.String(), nullable=True)
    azure_ad_subject_id = db.Column("azure_ad_subject_id", db.String(), nullable=True, unique=True)
    roles = db.relationship("Role", lazy="select", backref=db.backref("account", lazy="joined"))

    # this probably wants to be an enum, something along the lines of source: SSO, MAGIC_LINKS
    # it could actually reference the original link id that created it but we probably want a background job cleaning those up
    is_magic_link = db.Column("is_magic_link", Boolean())

    proto_created_date = db.Column("proto_created_date", DateTime(), server_default=func.now())
    proto_updated_date = db.Column("proto_updated_date", DateTime(), server_default=func.now(), onupdate=func.now())

    @property
    def highest_role_map(self) -> Mapping[str, str]:
        roles_as_strings = [r.role for r in self.roles]
        role_map = get_highest_role_map(roles_as_strings)
        current_app.logger.debug("Role map for {id}: {role_map}", extra=dict(id=self.id, role_map=role_map))
        return role_map
