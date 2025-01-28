from sqlalchemy import select

from db import db
from proto.common.data.models import (
    ProtoDataCollectionDefinitionQuestion,
    ProtoDataCollectionDefinitionSection,
    TemplateQuestion,
    TemplateSection,
)
from proto.common.data.models.data_collection import ProtoDataCollectionDefinition
from proto.common.data.models.question_bank import TemplateType
from proto.common.helpers import make_url_slug


def get_template_sections_and_questions(template_type: TemplateType):
    template_sections = (
        db.session.scalars(
            select(TemplateSection)
            .join(TemplateQuestion)
            .filter(TemplateSection.type == template_type)
            .order_by(TemplateSection.order)
        )
        .unique()
        .all()
    )
    return template_sections


def get_section_for_data_collection_definition(data_collection_definition, section_id):
    return db.session.scalars(
        select(ProtoDataCollectionDefinitionSection)
        .join(ProtoDataCollectionDefinition)
        .filter(
            ProtoDataCollectionDefinition.id == data_collection_definition.id,
            ProtoDataCollectionDefinitionSection.id == section_id,
        )
    ).one()


def create_question(**kwargs):
    kwargs["slug"] = make_url_slug(kwargs["title"])
    question = ProtoDataCollectionDefinitionQuestion(**kwargs)
    db.session.add(question)
    db.session.commit()


def create_section(**kwargs):
    kwargs["slug"] = make_url_slug(kwargs["title"])
    section = ProtoDataCollectionDefinitionSection(**kwargs)
    db.session.add(section)
    db.session.commit()


def add_template_sections_to_data_collection_definition(round, template_section_ids):
    template_sections = (
        db.session.scalars(
            select(TemplateSection)
            .join(TemplateQuestion)
            .filter(TemplateSection.id.in_(template_section_ids), TemplateSection.type == TemplateType.APPLICATION)
        )
        .unique()
        .all()
    )

    if not round.data_collection_definition:
        round.data_collection_definition = ProtoDataCollectionDefinition()
        db.session.add(round.data_collection_definition)
        db.session.flush()

    sections = []
    for template_section in template_sections:
        section = ProtoDataCollectionDefinitionSection(
            slug=template_section.slug,
            title=template_section.title,
            order=template_section.order,
            definition_id=round.data_collection_definition_id,
        )
        db.session.add(section)
        sections.append(section)

        for template_question in template_section.template_questions:
            question = ProtoDataCollectionDefinitionQuestion(
                slug=template_question.slug,
                type=template_question.type,
                title=template_question.title,
                hint=template_question.hint,
                order=template_question.order,
                data_source=template_question.data_source,
                data_standard_id=template_question.data_standard_id,
                section_id=section.id,
                template_question_id=template_question.id,
            )
            section.questions.append(question)

    db.session.commit()


def get_application_question(data_collection_definition_id, section_slug, question_slug):
    return db.session.scalar(
        select(ProtoDataCollectionDefinitionQuestion)
        .join(ProtoDataCollectionDefinitionSection)
        .join(ProtoDataCollectionDefinition)
        .filter(
            ProtoDataCollectionDefinition.id == data_collection_definition_id,
            ProtoDataCollectionDefinitionQuestion.slug == question_slug,
            ProtoDataCollectionDefinitionSection.slug == section_slug,
        )
    )


# def get_application_question(grant_code, round_code, question_id):
#     question = db.session.scalar(
#         select(DataCollectionQuestion)
#         .join(Round)
#         .join(Fund)
#         .filter(DataCollectionQuestion.id == question_id
#         , Round.short_name == round_code, Fund.short_name == grant_code)
#     ).one()
#     return question
