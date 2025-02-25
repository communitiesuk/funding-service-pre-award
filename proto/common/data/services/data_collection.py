from sqlalchemy import select

from db import db
from proto.common.data.models import ProtoDataCollectionDefinitionSection, ProtoDataCollectionInstanceSectionData


def get_data_collection_instance_section_data(data_collection_instance, section_slug):
    return db.session.scalar(
        select(ProtoDataCollectionInstanceSectionData)
        .join(ProtoDataCollectionDefinitionSection)
        .filter(
            ProtoDataCollectionInstanceSectionData.instance_id == data_collection_instance.id,
            ProtoDataCollectionDefinitionSection.slug == section_slug,
        )
    )


def set_data_collection_instance_section_complete(section_data: ProtoDataCollectionInstanceSectionData):
    section_data.completed = True
    db.session.add(section_data)
    db.session.commit()
