from sqlalchemy import select

from db import db
from proto.common.data.models import (
    ApplicationQuestion,
    ApplicationSection,
    Round,
    TemplateQuestion,
    TemplateSection,
)
from proto.common.data.models.question_bank import TemplateType


def get_application_template_sections_and_questions():
    template_sections = (
        db.session.scalars(
            select(TemplateSection)
            .join(TemplateQuestion)
            .filter(TemplateSection.type == TemplateType.APPLICATION)
            .order_by(TemplateSection.order)
        )
        .unique()
        .all()
    )
    return template_sections


def get_section_for_round(round, section_id):
    return db.session.scalars(
        select(ApplicationSection).join(Round).filter(Round.id == round.id, ApplicationSection.id == section_id)
    ).one()


def create_question(**kwargs):
    question = ApplicationQuestion(**kwargs)
    db.session.add(question)
    db.session.commit()


def create_section(**kwargs):
    section = ApplicationSection(**kwargs)
    db.session.add(section)
    db.session.commit()


def add_template_sections_to_application_round(round_id, template_section_ids):
    template_sections = (
        db.session.scalars(
            select(TemplateSection)
            .join(TemplateQuestion)
            .filter(TemplateSection.id.in_(template_section_ids), TemplateSection.type == TemplateType.APPLICATION)
        )
        .unique()
        .all()
    )

    sections = []
    for template_section in template_sections:
        section = ApplicationSection(
            slug=template_section.slug, title=template_section.title, order=template_section.order, round_id=round_id
        )
        db.session.add(section)
        sections.append(section)

        for template_question in template_section.template_questions:
            question = ApplicationQuestion(
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


def get_application_question(round_id, section_slug, question_slug):
    return db.session.scalar(
        select(ApplicationQuestion)
        .join(ApplicationSection)
        .join(Round)
        .filter(
            ApplicationQuestion.slug == question_slug, ApplicationSection.slug == section_slug, Round.id == round_id
        )
    )


# def get_application_question(grant_code, round_code, question_id):
#     question = db.session.scalar(
#         select(ApplicationQuestion)
#         .join(Round)
#         .join(Fund)
#         .filter(ApplicationQuestion.id == question_id, Round.short_name == round_code, Fund.short_name == grant_code)
#     ).one()
#     return question
