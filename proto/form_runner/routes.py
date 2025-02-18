from flask import g, redirect, render_template, request, url_for

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.models import (
    ProtoDataCollectionDefinitionQuestion,
    ProtoDataCollectionDefinitionSection,
    ProtoDataCollectionInstanceSectionData,
)
from proto.common.data.models.question_bank import QuestionType
from proto.common.data.services.applications import (
    get_application,
    get_application_section_data,
    set_application_section_complete,
    upsert_question_data,
)
from proto.common.data.services.question_bank import get_application_question
from proto.form_runner.form_route_helper import (
    get_next_question_for_data_collection_instance,
    get_visible_questions_for_section_instance,
)
from proto.form_runner.forms import MarkAsCompleteForm, build_question_form
from proto.form_runner.helpers import get_answer_text_for_question_from_section_data

runner_blueprint = Blueprint("proto_form_runner", __name__)


@runner_blueprint.context_processor
def _grants_service_nav():
    return dict(active_navigation_tab="your_grants")


def _next_url_for_question(
    application_external_id,
    section_definition: ProtoDataCollectionDefinitionSection,
    section_instance_data: ProtoDataCollectionInstanceSectionData,
    current_question: ProtoDataCollectionDefinitionQuestion,
    from_check_your_answers: bool,
):
    next_question = get_next_question_for_data_collection_instance(
        section_instance_data=section_instance_data, current_question_definition=current_question
    )

    goto_check_your_answers = False
    if next_question is None:
        # TODO: section could have an attribute to toggle on/off 'show check-your-answers' page
        goto_check_your_answers = True

    elif from_check_your_answers:
        existing_answer_for_next_question = get_answer_text_for_question_from_section_data(
            question=next_question, section_data=section_instance_data
        )
        if existing_answer_for_next_question:
            goto_check_your_answers = True

    if goto_check_your_answers:
        return url_for(
            "proto_form_runner.check_your_answers",
            application_external_id=application_external_id,
            section_slug=section_definition.slug,
        )

    return url_for(
        "proto_form_runner.ask_application_question",
        application_external_id=application_external_id,
        section_slug=section_definition.slug,
        question_slug=next_question.slug,
        from_cya=from_check_your_answers,
    )


def _back_link_for_question(question, application_external_id, from_check_your_answers):
    if from_check_your_answers:
        return url_for(
            "proto_form_runner.check_your_answers",
            application_external_id=application_external_id,
            section_slug=question.section.slug,
        )

    if question.slug == question.section.questions[0].slug:
        return url_for("proto_apply.application.application_tasklist", application_external_id=application_external_id)

    previous_question_index = question.section.questions.index(question) - 1

    return url_for(
        "proto_form_runner.ask_application_question",
        application_external_id=application_external_id,
        section_slug=question.section.slug,
        question_slug=question.section.questions[previous_question_index].slug,
    )


@runner_blueprint.route(
    "/application/<application_external_id>/<section_slug>/<question_slug>", methods=["GET", "POST"]
)
@is_authenticated
def ask_application_question(application_external_id, section_slug, question_slug):
    account = {"email": g.account.email}
    application = get_application(application_external_id)
    question = get_application_question(application.round.data_collection_definition_id, section_slug, question_slug)
    form = build_question_form(application, question)
    from_check_your_answers = "from_cya" in request.args
    if form.validate_on_submit():
        upsert_question_data(application, question, form.question.data)
        section_instance_data = next(
            section_data
            for section_data in application.data_collection_instance.section_data
            if section_data.section_id == question.section_id
        )
        return redirect(
            _next_url_for_question(
                application_external_id=application_external_id,
                section_definition=question.section,
                section_instance_data=section_instance_data,
                current_question=question,
                from_check_your_answers=from_check_your_answers,
            )
        )

    return render_template(
        "form_runner/question_page.html",
        application=application,
        question=question,
        QuestionType=QuestionType,
        section=question.section,
        form=form,
        back_link=_back_link_for_question(question, application_external_id, from_check_your_answers),
        account=account,
    )


@runner_blueprint.route(
    "/application/<application_external_id>/<section_slug>/check-your-answers", methods=["GET", "POST"]
)
@is_authenticated
def check_your_answers(application_external_id, section_slug):
    # these are workaronds for having the navigation show or not and aren't really used - this should be more generic
    account = {"email": g.account.email}
    application = get_application(external_id=application_external_id)
    section_data = get_application_section_data(application, section_slug)
    form = MarkAsCompleteForm(data={"complete": "yes" if section_data and section_data.completed else None})
    if form.validate_on_submit():
        if form.complete.data is True:
            set_application_section_complete(section_data)

        return redirect(
            url_for("proto_apply.application.application_tasklist", application_external_id=application_external_id)
        )
    return render_template(
        "form_runner/check_your_answers.html",
        application=application,
        section=section_data.section,
        section_data=section_data,
        QuestionType=QuestionType,
        get_answer_text_for_question_from_section_data=get_answer_text_for_question_from_section_data,
        form=form,
        account=account,
        visible_questions=get_visible_questions_for_section_instance(
            section_instance_data=section_data, section_definition=section_data.section
        ),
    )
