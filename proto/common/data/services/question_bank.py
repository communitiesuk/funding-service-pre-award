from sqlalchemy import select

from db import db
from proto.common.data.models import (
    ProtoDataCollectionDefinitionQuestion,
    ProtoDataCollectionDefinitionSection,
    Round,
    TemplateQuestion,
    TemplateSection,
)
from proto.common.data.models.data_collection import (
    ProtoDataCollectionDefinition,
    ProtoDataCollectionQuestionCondition,
    ProtoDataCollectionQuestionValidation,
)
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
    # fixme: last minute hack fix
    if isinstance(round, Round):
        template_type = TemplateType.APPLICATION
    else:
        template_type = TemplateType.REPORTING

    template_sections = (
        db.session.scalars(
            select(TemplateSection)
            .join(TemplateQuestion)
            .filter(TemplateSection.id.in_(template_section_ids), TemplateSection.type == template_type)
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
            template_section_id=template_section.id,
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
                condition_combination_type=template_question.condition_combination_type,
            )
            section.questions.append(question)

        def _get_question_from_different_section(
            section_instance: ProtoDataCollectionDefinitionSection, template_question: TemplateQuestion
        ):
            # This assumes that the question that a condition depends on has been created first.
            # Which should be true since we respect question ordering...
            target_section = next(
                s
                for s in section_instance.definition.sections
                if s.template_section_id == template_question.template_section_id
            )
            depends_on_question = next(
                q for q in target_section.questions if q.template_question_id == template_question.id
            )
            return depends_on_question

        # now that new questions all exist

        for template_question in template_section.template_questions:
            for template_validation in template_question.validations:
                question = next(
                    q for q in section.questions if q.template_question_id == template_validation.question.id
                )
                depends_on_question = (
                    _get_question_from_different_section(section, template_validation.depends_on_question)
                    if template_validation.depends_on_question
                    else None
                )
                validation = ProtoDataCollectionQuestionValidation(
                    question=question,
                    depends_on_question=depends_on_question,
                    expression=template_validation.expression,
                    message=template_validation.message,
                )
                question.validations.append(validation)

            for template_condition in template_question.conditions:
                question = next(
                    q for q in section.questions if q.template_question_id == template_condition.question.id
                )
                depends_on_question = (
                    next(
                        q
                        for q in section.questions
                        if q.template_question_id == template_condition.depends_on_question.id
                    )
                    if template_section.id == template_condition.depends_on_question.template_section_id
                    else _get_question_from_different_section(section, template_condition.depends_on_question)
                )
                condition = ProtoDataCollectionQuestionCondition(
                    question=question,
                    depends_on_question=depends_on_question,
                    criteria=template_condition.criteria,
                    expression=template_condition.expression,
                )
                question.conditions.append(condition)

    db.session.commit()


def get_data_collection_question(data_collection_definition_id, section_slug, question_slug):
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
