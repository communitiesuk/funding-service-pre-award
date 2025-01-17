from uuid import UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.sqltypes import Uuid

from db import db

db.Model.registry.update_type_annotation_map({dict: JSONB(), UUID: Uuid})  # noqa

from proto.common.data.models.fund import Fund as Fund  # noqa
from proto.common.data.models.question_bank import (  # noqa
    DataStandard as DataStandard,
    TemplateSection as TemplateSection,
    TemplateQuestion as TemplateQuestion,
    ApplicationSection as ApplicationSection,
    ApplicationQuestion as ApplicationQuestion,
)
from proto.common.data.models.round import Round as Round  # noqa
