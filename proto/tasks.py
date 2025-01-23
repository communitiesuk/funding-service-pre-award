import os
from contextlib import contextmanager

from invoke import task
from sqlalchemy import text

from proto.common.data.models import TemplateSection
from proto.common.data.models.question_bank import DataStandard, QuestionType, TemplateQuestion, TemplateType


@contextmanager
def _env_var(key, value):
    old_val = os.environ.get(key, "")
    os.environ[key] = value
    yield
    os.environ[key] = old_val


def insert_question_bank_data():
    from db import db

    data_standards_to_create = {
        "$github.com/communitiesuk/json.schema#person.name": DataStandard(
            slug="$github.com/communitiesuk/json.schema#person.name", description="A person's name"
        )
    }

    for ds_slug, ds_instance in data_standards_to_create.items():
        ds_id = db.session.execute(
            text("select id from data_standard where slug = :slug"), dict(slug=ds_slug)
        ).scalar_one_or_none()
        if not ds_id:
            db.session.add(ds_instance)
        else:
            ds_instance.id = ds_id
            db.session.merge(ds_instance)
        db.session.flush()

    template_sections_to_create = {
        "project-information": TemplateSection(
            slug="project-information", title="Project Information", order=1, type=TemplateType.APPLICATION
        ),
        "organisation-information": TemplateSection(
            slug="organisation-information",
            title="Organisation Information",
            order=2,
            type=TemplateType.APPLICATION,
        ),
    }
    for ts_slug, ts_instance in template_sections_to_create.items():
        ts_id = db.session.execute(
            text("select id from template_section where slug = :slug"), dict(slug=ts_slug)
        ).scalar_one_or_none()
        if not ts_id:
            db.session.add(ts_instance)
        else:
            ts_instance.id = ts_id
            db.session.merge(ts_instance)
        db.session.flush()

    template_questions_to_create = {
        "project-name": TemplateQuestion(
            slug="project-name",
            type=QuestionType.TEXT_INPUT,
            title="What is the name of your project?",
            hint=None,
            order=1,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "project-owner": TemplateQuestion(
            slug="project-owner",
            type=QuestionType.TEXT_INPUT,
            title="Who is your project's owner?",
            hint=None,
            order=2,
            data_source=None,
            data_standard_id=data_standards_to_create["$github.com/communitiesuk/json.schema#person.name"].id,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "project-about-cheese": TemplateQuestion(
            slug="project-about-cheese",
            type=QuestionType.RADIOS,
            title="Is the project about cheese?",
            hint=None,
            order=3,
            data_source=[{"value": "yes", "label": "Yes"}, {"value": "no", "label": "No"}],
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "organisation-name": TemplateQuestion(
            slug="organisation-name",
            type=QuestionType.TEXT_INPUT,
            title="What is the name of your organisation?",
            hint=None,
            order=1,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["organisation-information"].id,
        ),
        "organisation-owner": TemplateQuestion(
            slug="organisation-owner",
            type=QuestionType.TEXT_INPUT,
            title="Who is your organisation's owner?",
            hint=None,
            order=2,
            data_source=None,
            data_standard_id=data_standards_to_create["$github.com/communitiesuk/json.schema#person.name"].id,
            template_section_id=template_sections_to_create["organisation-information"].id,
        ),
    }
    for tq_slug, tq_instance in template_questions_to_create.items():
        tq_id = db.session.execute(
            text("select id from template_question where template_section_id = :template_section_id and slug = :slug"),
            dict(template_section_id=tq_instance.template_section_id, slug=tq_slug),
        ).scalar_one_or_none()
        if not tq_id:
            db.session.add(tq_instance)
        else:
            tq_instance.id = tq_id
            db.session.merge(tq_instance)
        db.session.flush()

    db.session.commit()


@task
def seed_question_bank(c):
    from app import create_app

    with _env_var("FLASK_ENV", "development"):
        app = create_app()
        with app.app_context():
            insert_question_bank_data()
