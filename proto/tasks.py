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
        "user.schema.json#properties/full_name": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/user.schema.json#properties/full_name",
            description="A person's name",
        ),
        "organisation.schema.json#properties/name": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/organisation.schema.json#properties/name",
            description="The organisation name",
        ),
        "organisation.schema.json#properties/type": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/organisation.schema.json#properties/type",
            description="The organisation type",
        ),
        "risk.schema.json#properties/risk_title": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/risk.schema.json#properties/risk_title",
            description="A short description of the risk",
        ),
        "risk.schema.json#properties/risk_description": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/risk.schema.json#properties/risk_description",
            description="The details of the risk",
        ),
        "risk.schema.json#properties/risk_category": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/risk.schema.json#properties/principal_risk_category",
            description="The primary categorisation of the risk",
        ),
    }
    for _, ds_instance in data_standards_to_create.items():
        ds_id = db.session.scalar(text("select id from data_standard where slug = :slug"), dict(slug=ds_instance.slug))
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
        "risk-information": TemplateSection(
            slug="risk-information",
            title="Risks",
            order=3,
            type=TemplateType.APPLICATION,
        ),
        # Hack - possibly would de-dupe this if we were doing it for real
        "monitoring-risk-information": TemplateSection(
            slug="monitoring-risk-information",  # hack - maybe should be unique on slug+type
            title="Risks",
            order=1,
            type=TemplateType.REPORTING,
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
        "project-about": TemplateQuestion(
            slug="project-about",
            type=QuestionType.TEXTAREA,
            title="What is your project about?",
            hint="Give a brief summary of your project, including what you hope to achieve",
            order=2,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "risk-name": TemplateQuestion(
            slug="organisation-name",
            type=QuestionType.TEXT_INPUT,
            title="What is the name of your organisation?",
            hint=None,
            order=1,
            data_source=None,
            data_standard_id=data_standards_to_create["organisation.schema.json#properties/name"].id,
            template_section_id=template_sections_to_create["organisation-information"].id,
        ),
        "organisation-kind": TemplateQuestion(
            slug="organisation-kind",
            type=QuestionType.RADIOS,
            title="What kind of organisation are you in?",
            hint=None,
            order=2,
            data_source=[
                {"value": "charity", "label": "Charity"},
                {"value": "local-authority", "label": "Local Authority"},
                {"value": "limited-company", "label": "Limited company"},
                {"value": "other", "label": "Other"},
            ],
            data_standard_id=data_standards_to_create["organisation.schema.json#properties/type"].id,
            template_section_id=template_sections_to_create["organisation-information"].id,
        ),
        "organisation-owner": TemplateQuestion(
            slug="organisation-owner",
            type=QuestionType.TEXT_INPUT,
            title="Who is your organisation's owner?",
            hint=None,
            order=3,
            data_source=None,
            data_standard_id=data_standards_to_create["user.schema.json#properties/full_name"].id,
            template_section_id=template_sections_to_create["organisation-information"].id,
        ),
        "risk-title": TemplateQuestion(
            slug="risk-title",
            type=QuestionType.TEXT_INPUT,
            title="What is the risk to your project?",
            hint="Summarise the risk in a single sentence",
            order=1,
            data_source=None,
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_title"].id,
            template_section_id=template_sections_to_create["risk-information"].id,
        ),
        "risk-description": TemplateQuestion(
            slug="risk-description",
            type=QuestionType.TEXTAREA,
            title="Tell us more about the risk to your project.",
            hint="""<p class="govuk-hint">
            You should cover:
            <ul class="govuk-list govuk-list--bullet govuk-hint">
            <li>What could go wrong?</li>
            <li>What could cause things to go wrong></li>
            <li>What would the outcome be if it did go wrong?</li>
            </ul>
            </p>""",
            order=2,
            data_source=None,
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_description"].id,
            template_section_id=template_sections_to_create["risk-information"].id,
        ),
        "risk-category": TemplateQuestion(
            slug="risk-category",
            type=QuestionType.RADIOS,
            title="What is the main category for this risk?",
            hint=None,
            order=3,
            data_source=[
                {"value": val, "label": val}
                for val in [
                    "Arms length bodies",
                    "Commercial",
                    "Financial",
                    "Governance",
                    "Information and data",
                    "Legal",
                    "Local Government delivery",
                    "People",
                    "Project delivery",
                    "Resilience",
                    "Security",
                    "Strategy",
                    "Systems and infrastructure",
                ]
            ],
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_category"].id,
            template_section_id=template_sections_to_create["risk-information"].id,
        ),
        "monitoring-risk-title": TemplateQuestion(
            slug="risk-title",
            type=QuestionType.TEXT_INPUT,
            title="What is the risk to your project?",
            hint="Summarise the risk in a single sentence",
            order=1,
            data_source=None,
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_title"].id,
            template_section_id=template_sections_to_create["monitoring-risk-information"].id,
        ),
        "monitoring-risk-description": TemplateQuestion(
            slug="risk-description",
            type=QuestionType.TEXTAREA,
            title="Tell us more about the risk to your project.",
            hint="""<p class="govuk-hint">
            You should cover:
            <ul class="govuk-list govuk-list--bullet govuk-hint">
            <li>What could go wrong?</li>
            <li>What could cause things to go wrong></li>
            <li>What would the outcome be if it did go wrong?</li>
            </ul>
            </p>""",
            order=2,
            data_source=None,
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_description"].id,
            template_section_id=template_sections_to_create["monitoring-risk-information"].id,
        ),
        "monitoring-risk-category": TemplateQuestion(
            slug="risk-category",
            type=QuestionType.RADIOS,
            title="What is the main category for this risk?",
            hint=None,
            order=3,
            data_source=[
                {"value": val, "label": val}
                for val in [
                    "Arms length bodies",
                    "Commercial",
                    "Financial",
                    "Governance",
                    "Information and data",
                    "Legal",
                    "Local Government delivery",
                    "People",
                    "Project delivery",
                    "Resilience",
                    "Security",
                    "Strategy",
                    "Systems and infrastructure",
                ]
            ],
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_category"].id,
            template_section_id=template_sections_to_create["monitoring-risk-information"].id,
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
