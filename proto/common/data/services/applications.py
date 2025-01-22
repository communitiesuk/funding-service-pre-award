import random
import string

from sqlalchemy import cast, delete, func, select
from sqlalchemy.dialects.postgresql import JSONB, insert

from db import db
from proto.common.data.models import (
    ApplicationQuestion,
    ApplicationSection,
    Fund,
    ProtoApplication,
    ProtoApplicationSectionData,
    Round,
)
from proto.common.data.models.question_bank import QuestionType


def _generate_application_code():
    return "".join(random.choices(string.ascii_uppercase, k=6))


def create_application(preview: bool, round_id: int, account_id: str):
    if preview:
        db.session.execute(
            delete(ProtoApplication).filter(
                ProtoApplication.fake.is_(True),
                ProtoApplication.round_id == round_id,
                ProtoApplication.account_id == account_id,
            )
        )

    application = ProtoApplication(
        code=_generate_application_code(), fake=preview, round_id=round_id, account_id=account_id
    )
    db.session.add(application)
    db.session.commit()
    return application


def get_application(application_id: int):
    return db.session.scalars(select(ProtoApplication).filter(ProtoApplication.id == application_id)).one()


def get_applications(account_id):
    applications = db.session.scalars(select(ProtoApplication).filter(ProtoApplication.account_id == account_id)).all()
    return applications


def search_applications(short_code):
    applications = db.session.scalars(
        select(ProtoApplication).join(Round).join(Fund).filter(Fund.short_name == short_code)
    ).all()  # can use this to prove competitive vs. un-competed, only from submitted or all
    return applications


def _build_answer_dict(question: "ApplicationQuestion", answer: str) -> dict:
    if question.type == QuestionType.RADIOS:
        answer = next(filter(lambda choice: choice["value"] == answer, question.data_source))

    return {
        "answer": answer,
        "question_type": question.type,
    }


def get_current_answer_to_question(application: ProtoApplication, question: "ApplicationQuestion") -> str | dict:
    # str(question.id) because JSON keys must be strings, but our question PK col is an int
    return db.session.scalar(
        select(ProtoApplicationSectionData.data[str(question.id)]["answer"]).filter(
            ProtoApplicationSectionData.proto_application == application,
            ProtoApplicationSectionData.section_id == question.section_id,
        )
    )


def upsert_question_data(application: ProtoApplication, question: "ApplicationQuestion", answer: str):
    db_answer = _build_answer_dict(question, answer)

    db.session.execute(
        insert(ProtoApplicationSectionData)
        .values(data={question.id: db_answer}, proto_application_id=application.id, section_id=question.section_id)
        .on_conflict_do_update(
            index_elements=[ProtoApplicationSectionData.proto_application_id, ProtoApplicationSectionData.section_id],
            set_={
                ProtoApplicationSectionData.data: func.jsonb_set(
                    ProtoApplicationSectionData.data, f"{{{question.id}}}", cast(db_answer, JSONB), True
                )
            },
        )
    )
    db.session.commit()


def get_application_section_data(application_id, section_slug):
    return db.session.scalar(
        select(ProtoApplicationSectionData)
        .join(ApplicationSection)
        .filter(
            ProtoApplicationSectionData.proto_application_id == application_id,
            ApplicationSection.slug == section_slug,
        )
    )


def set_application_section_complete(section_data: ProtoApplicationSectionData):
    section_data.completed = True
    db.session.add(section_data)
    db.session.commit()
