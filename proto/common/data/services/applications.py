import random
import string
import uuid

from sqlalchemy import case, cast, delete, func, select
from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.orm import joinedload

from apply.models.account import Account
from db import db
from proto.common.data.models import (
    Fund,
    ProtoApplication,
    ProtoDataCollectionDefinitionQuestion,
    ProtoDataCollectionDefinitionSection,
    ProtoDataCollectionInstanceSectionData,
    Round,
)
from proto.common.data.models.applications import TestLiveStatus
from proto.common.data.models.data_collection import ProtoDataCollectionInstance
from proto.common.data.models.fund import FundingType
from proto.common.data.models.proto_comment import ProtoComment
from proto.common.data.models.proto_score import ProtoScore
from proto.common.data.models.question_bank import QuestionType


def _generate_application_code():
    return "".join(random.choices(string.ascii_uppercase, k=6))


def create_application(preview: bool, round_id: int, organisation_id: uuid.UUID):
    if preview:
        db.session.execute(
            delete(ProtoApplication).filter(
                ProtoApplication.fake.is_(True),
                ProtoApplication.round_id == round_id,
                ProtoApplication.organisation_id == organisation_id,
            )
        )

    application = ProtoApplication(
        code=_generate_application_code(),
        fake=preview,
        round_id=round_id,
        organisation_id=organisation_id,
        data_collection_instance=ProtoDataCollectionInstance(),
        # this should be based on if the _round_ is "preview" - the round can only
        # not be "preview" if the grant is "live"
        # will need to reconcile with how this works with fake later but assumption
        # would be all fake applications are test
        test_live_status=TestLiveStatus.TEST,
    )
    db.session.add(application)
    db.session.commit()
    return application


def get_application(external_id: uuid.UUID):
    return db.session.scalars(select(ProtoApplication).filter(ProtoApplication.external_id == external_id)).one()


def get_applications(organisation_id, short_code):
    applications = db.session.scalars(
        select(ProtoApplication)
        .join(Round)
        .join(Fund)
        .filter(
            ProtoApplication.organisation_id == organisation_id,
            Fund.short_name == short_code,
            ProtoApplication.fake.is_(False),
        )
    ).all()
    return applications


def search_applications(short_code):
    applications = db.session.scalars(
        select(ProtoApplication)
        .join(Round)
        .join(Fund)
        .filter(
            Fund.short_name == short_code,
            case((Fund.funding_type == FundingType.COMPETITIVE, ProtoApplication.submitted), else_=True),
        )
    ).all()
    return applications


def get_application_grants(organisation_id):
    grants = (
        db.session.scalars(
            select(Fund)
            .options(joinedload(Fund.rounds))
            .join(Round)
            .join(ProtoApplication)
            .filter(ProtoApplication.organisation_id == organisation_id)
        )
        .unique()
        .all()
    )
    return grants


def _build_answer_dict(question: "ProtoDataCollectionDefinitionQuestion", answer: str) -> dict:
    if question.type == QuestionType.RADIOS:
        answer = next(filter(lambda choice: choice["value"] == answer, question.data_source))

    return {
        "answer": answer,
        "question_type": question.type,
    }


def get_current_answer_to_question(
    application: ProtoApplication, question: "ProtoDataCollectionDefinitionQuestion"
) -> str | dict:
    # str(question.id) because JSON keys must be strings, but our question PK col is an int
    return db.session.scalar(
        select(ProtoDataCollectionInstanceSectionData.data[str(question.id)]["answer"]).filter(
            ProtoDataCollectionInstanceSectionData.instance_id == application.data_collection_instance_id,
            ProtoDataCollectionInstanceSectionData.section_id == question.section_id,
        )
    )


def upsert_question_data(application: ProtoApplication, question: "ProtoDataCollectionDefinitionQuestion", answer: str):
    db_answer = _build_answer_dict(question, answer)

    db.session.execute(
        insert(ProtoDataCollectionInstanceSectionData)
        .values(
            data={question.id: db_answer},
            instance_id=application.data_collection_instance_id,
            section_id=question.section_id,
        )
        .on_conflict_do_update(
            index_elements=[
                ProtoDataCollectionInstanceSectionData.instance_id,
                ProtoDataCollectionInstanceSectionData.section_id,
            ],
            set_={
                ProtoDataCollectionInstanceSectionData.data: func.jsonb_set(
                    ProtoDataCollectionInstanceSectionData.data, f"{{{question.id}}}", cast(db_answer, JSONB), True
                )
            },
        )
    )
    db.session.commit()


def get_application_section_data(application, section_slug):
    return db.session.scalar(
        select(ProtoDataCollectionInstanceSectionData)
        .join(ProtoDataCollectionDefinitionSection)
        .filter(
            ProtoDataCollectionInstanceSectionData.instance_id == application.data_collection_instance_id,
            ProtoDataCollectionDefinitionSection.slug == section_slug,
        )
    )


def set_application_section_complete(section_data: ProtoDataCollectionInstanceSectionData):
    section_data.completed = True
    db.session.add(section_data)
    db.session.commit()


def submit_application(application: ProtoApplication):
    application.submitted = True
    db.session.add(application)
    db.session.commit()


# this could probably be fetched with a clever join alongside the application but
# I'm just going to do it here for now, there may be a method we want to get both comments
# and scores by application or section
# we almost definitely want to access this from the application model to make
# route handler code clean
def get_comments(application_id, section_id=None):
    filters = [ProtoComment.application_id == application_id]
    if section_id:
        filters.append(ProtoComment.section_id == section_id)
    comments = db.session.scalars(select(ProtoComment).filter(*filters)).all()
    return comments


def add_comment(
    application: ProtoApplication, account: Account, comment: str, section: ProtoDataCollectionDefinitionSection = None
):
    comment = ProtoComment(
        account_id=account.id,
        application_id=application.id,
        section_id=section.id if section else None,
        comment=comment,
    )
    db.session.add(comment)
    db.session.commit()
    return comment


def score_application(
    application: ProtoApplication,
    account: Account,
    score: int,
    reason: str,
    section: ProtoDataCollectionDefinitionSection,
):
    score = ProtoScore(
        account_id=account.id, application_id=application.id, section_id=section.id, score=score, reason=reason
    )
    db.session.add(score)
    db.session.commit()
    return score
