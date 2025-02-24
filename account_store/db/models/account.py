import uuid  # noqa
from typing import Mapping, TYPE_CHECKING

from flask import current_app
from fsd_utils.authentication.utils import get_highest_role_map
from sqlalchemy import Boolean, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db

if TYPE_CHECKING:
    from proto.common.data.models import Organisation


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

    is_magic_link = db.Column("is_magic_link", Boolean())

    proto_created_date = db.Column("proto_created_date", DateTime(), server_default=func.now())
    proto_updated_date = db.Column("proto_updated_date", DateTime(), server_default=func.now(), onupdate=func.now())

    # proto: out-scoping a user being in multiple orgs
    organisation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organisation.id"))
    organisation: Mapped["Organisation"] = relationship("Organisation")

    @property
    def highest_role_map(self) -> Mapping[str, str]:
        roles_as_strings = [r.role for r in self.roles]
        role_map = get_highest_role_map(roles_as_strings)
        current_app.logger.debug("Role map for %(id)s: %(role_map)s", dict(id=self.id, role_map=role_map))
        return role_map

    @property
    def is_platform_admin(self):
        return self.email.endswith("@communities.gov.uk") if self.email else False
