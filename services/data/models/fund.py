import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pre_award.common.locale_selector.get_lang import get_lang
from pre_award.db import FundingType, db
from services.data.models.round import Round

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


class Fund(Model):
    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True,
    )
    name_json: Mapped[dict[str, str]]
    title_json: Mapped[dict[str, str]]
    short_name: Mapped[str] = mapped_column(unique=True)
    description_json: Mapped[dict[str, str]]
    rounds: Mapped[List["Round"]] = relationship("Round")
    welsh_available: Mapped[bool] = mapped_column(default=False, nullable=False)
    owner_organisation_name: Mapped[str]
    owner_organisation_shortname: Mapped[str]
    owner_organisation_logo_uri: Mapped[Optional[str]]
    funding_type: Mapped[FundingType] = mapped_column(
        Enum(
            FundingType,
            name="fundingtype",
            create_constraint=True,
            validate_strings=True,
        )
    )
    ggis_scheme_reference_number: Mapped[Optional[str]]

    @property
    def fund_name(self) -> str:
        return self.name_json[get_lang()] or self.name_json["en"]

    @property
    def fund_title(self) -> str:
        return self.title_json[get_lang()] or self.title_json["en"]
