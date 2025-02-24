from uuid import UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.sqltypes import Uuid

from db import db
from proto.common.data.models.types import t_data_source

db.Model.registry.update_type_annotation_map({dict: JSONB(), t_data_source: JSONB(), UUID: Uuid})  # noqa

from proto.common.data.models.fund import Fund as Fund  # noqa
from proto.common.data.models.round import Round as Round  # noqa

from proto.common.data.models.question_bank import (  # noqa
    DataStandard as DataStandard,
    TemplateSection as TemplateSection,
    TemplateQuestion as TemplateQuestion,
)
from proto.common.data.models.round import Round as Round  # noqa
from proto.common.data.models.reporting_round import ProtoReportingRound as ProtoReportingRound  # noqa
from proto.common.data.models.applications import (  # noqa
    ProtoApplication as ProtoApplication,
)
from proto.common.data.models.data_collection import (  # noqa
    ProtoDataCollectionDefinition as ProtoDataCollectionDefinition,
    ProtoDataCollectionInstance as ProtoDataCollectionInstance,
    ProtoDataCollectionInstanceSectionData as ProtoDataCollectionInstanceSectionData,
    ProtoDataCollectionDefinitionQuestion as ProtoDataCollectionDefinitionQuestion,
    ProtoDataCollectionDefinitionSection as ProtoDataCollectionDefinitionSection,
)
from proto.common.data.models.reports import ProtoReport as ProtoReport  # noqa
from proto.common.data.models.recipients import ProtoGrantRecipient as ProtoGrantRecipient  # noqa
from proto.common.data.models.organisation import Organisation as Organisation  # noqa
