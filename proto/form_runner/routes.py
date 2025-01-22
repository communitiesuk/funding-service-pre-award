from flask import redirect, render_template, request, session, url_for

from common.blueprints import Blueprint
from proto.common.data.models.question_bank import QuestionType
from proto.common.data.services.accounts import get_account
from proto.common.data.services.applications import (
    get_application,
    get_application_section_data,
    set_application_section_complete,
    upsert_question_data,
)
from proto.common.data.services.question_bank import get_application_question
from proto.form_runner.forms import MarkAsCompleteForm, build_question_form
from proto.form_runner.helpers import get_answer_text_for_question_from_section_data

runner_blueprint = Blueprint("proto_form_runner", __name__)


@runner_blueprint.get("/application/<application_id>")
def application_tasklist(application_id):
    account = get_account(session.get("magic_links_account_id"))
    application = get_application(application_id)
    return render_template("form_runner/application_tasklist.html", application=application, account=account)


def _next_url_for_question(application_id, section, current_question_slug, from_check_your_answers):
    if from_check_your_answers:
        return url_for("proto_form_runner.check_your_answers", application_id=application_id, section_slug=section.slug)

    question_slugs = [question.slug for question in section.questions]
    curr_index = question_slugs.index(current_question_slug)
    if curr_index == len(question_slugs) - 1:
        # TODO: section could have an attribute to toggle on/off 'show check-your-answers' page
        return url_for("proto_form_runner.check_your_answers", application_id=application_id, section_slug=section.slug)

    return url_for(
        "proto_form_runner.ask_application_question",
        application_id=application_id,
        section_slug=section.slug,
        question_slug=question_slugs[curr_index + 1],
    )


def _back_link_for_question(question, application_id, from_check_your_answers):
    if from_check_your_answers:
        return url_for(
            "proto_form_runner.check_your_answers", application_id=application_id, section_slug=question.section.slug
        )

    if question.slug == question.section.questions[0].slug:
        return url_for("proto_form_runner.application_tasklist", application_id=application_id)

    previous_question_index = question.section.questions.index(question) - 1

    return url_for(
        "proto_form_runner.ask_application_question",
        application_id=application_id,
        section_slug=question.section.slug,
        question_slug=question.section.questions[previous_question_index].slug,
    )


@runner_blueprint.route("/application/<application_id>/<section_slug>/<question_slug>", methods=["GET", "POST"])
def ask_application_question(application_id, section_slug, question_slug):
    account = {"email": session.get("magic_links_account_email")}
    application = get_application(application_id)
    question = get_application_question(application.round_id, section_slug, question_slug)
    form = build_question_form(application, question)
    from_check_your_answers = "from_cya" in request.args
    if form.validate_on_submit():
        upsert_question_data(application, question, form.question.data)
        return redirect(
            _next_url_for_question(application_id, question.section, question_slug, from_check_your_answers)
        )

    return render_template(
        "form_runner/question_page.html",
        application=application,
        question=question,
        QuestionType=QuestionType,
        section=question.section,
        form=form,
        back_link=_back_link_for_question(question, application_id, from_check_your_answers),
        account=account,
    )


@runner_blueprint.route("/application/<application_id>/<section_slug>/check-your-answers", methods=["GET", "POST"])
def check_your_answers(application_id, section_slug):
    # these are workaronds for having the navigation show or not and aren't really used - this should be more generic
    account = {"email": session.get("magic_links_account_email")}
    application = get_application(application_id=application_id)
    section_data = get_application_section_data(application_id, section_slug)
    form = MarkAsCompleteForm(data={"complete": "yes" if section_data and section_data.completed else None})
    if form.validate_on_submit():
        if form.complete.data is True:
            set_application_section_complete(section_data)

        return redirect(url_for("proto_form_runner.application_tasklist", application_id=application_id))
    return render_template(
        "form_runner/check_your_answers.html",
        application=application,
        section=section_data.section,
        section_data=section_data,
        QuestionType=QuestionType,
        get_answer_text_for_question_from_section_data=get_answer_text_for_question_from_section_data,
        form=form,
        account=account,
    )
