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
    upsert_question_data,
)
from proto.common.data.services.data_collection import (
    get_data_collection_instance_section_data,
    set_data_collection_instance_section_complete,
)
from proto.common.data.services.question_bank import get_data_collection_question
from proto.common.data.services.recipients import (
    get_grant_recipient_for_organisation,
    get_grant_recipients_for_organisation,
)
from proto.common.data.services.reports import (
    get_or_create_monitoring_reports_for_grant_recipient,
    get_report,
)
from proto.form_runner.expressions import build_context_injector
from proto.form_runner.form_route_helper import (
    get_next_question_for_data_collection_instance,
    get_previous_question_for_data_collection_instance,
    get_visible_questions_for_section_instance,
)
from proto.form_runner.forms import MarkAsCompleteForm, build_question_form
from proto.form_runner.helpers import (
    get_answer_text_for_question_from_section_data,
    get_answer_value_for_question_from_section_data,
)

report_blueprint = Blueprint("proto_report", __name__)


def _next_url_for_question(
    report_id,
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
        existing_answer_for_next_question = get_answer_value_for_question_from_section_data(
            question=next_question, section_data=section_instance_data
        )
        if existing_answer_for_next_question:
            goto_check_your_answers = True

    if goto_check_your_answers:
        return url_for(
            "proto_report.check_your_answers",
            report_id=report_id,
            section_slug=section_definition.slug,
        )

    return url_for(
        "proto_report.ask_question",
        report_id=report_id,
        section_slug=section_definition.slug,
        question_slug=next_question.slug,
        from_cya=from_check_your_answers,
    )


def _back_link_for_question(question, report, from_check_your_answers, section_instance_data):
    if from_check_your_answers:
        return url_for(
            "proto_report.check_your_answers",
            report_id=report.id,
            section_slug=question.section.slug,
        )

    if question.slug == question.section.questions[0].slug:
        return url_for(
            "proto_report.tasklist",
            short_name=report.reporting_round.grant.short_name,
            reporting_round_id=report.reporting_round.id,
        )

    # doesn't explicitly handle if section_instance_data is None which it should
    # it's very unlikley given how its set up right now but its fragile
    previous_question = get_previous_question_for_data_collection_instance(
        section_instance_data=section_instance_data, current_question_definition=question
    )

    return url_for(
        "proto_report.ask_question",
        report_id=report.id,
        section_slug=question.section.slug,
        question_slug=previous_question.slug,
    )


@report_blueprint.context_processor
def _grants_service_nav():
    return dict(active_navigation_tab="your_reporting")


@report_blueprint.get("/report")
@report_blueprint.get("/report/")
@is_authenticated
def report_index():
    grant_recipients = get_grant_recipients_for_organisation(g.account.organisation_id)
    return render_template(
        "report/index.html",
        grant_recipients=grant_recipients,
        organisation=g.account.organisation,
        account=g.account,
    )


@report_blueprint.get("/report/<short_name>")
@is_authenticated
def view_grant(short_name):
    grant_recipient = get_grant_recipient_for_organisation(g.account.organisation_id, short_name)

    # M&E reports are fundamentally different from applications. With an application, you click the 'apply' button
    # and that's you actively starting the process. Clicking that button will create the application in the DB and
    # create the data collection instance.
    # With M&E reports, the platform has to show you that a report is expected to be completed without any specific
    # action from a grant recipient. Without some sort of background job to automatically create the report for each
    # recipient in the DB, and associated data collection instances, we can't safely assume that these records will
    # exist. So here, we create the report and data collection instance when users visit these pages.
    grant_reports = get_or_create_monitoring_reports_for_grant_recipient(grant_recipient)
    mapped_grant_reports = {report.reporting_round_id: report for report in grant_reports}

    return render_template(
        "report/view-grant.html",
        grant_recipient=grant_recipient,
        mapped_grant_reports=mapped_grant_reports,
        account=g.account,
    )


@report_blueprint.route("/report/<short_name>/<int:reporting_round_id>", methods=["GET", "POST"])
@is_authenticated
def tasklist(short_name, reporting_round_id):
    grant_recipient = get_grant_recipient_for_organisation(g.account.organisation_id, short_name)

    grant_reports = get_or_create_monitoring_reports_for_grant_recipient(grant_recipient)
    mapped_grant_reports = {report.reporting_round_id: report for report in grant_reports}

    report = mapped_grant_reports[reporting_round_id]

    return render_template(
        "report/tasklist.html",
        report=report,
    )


@report_blueprint.route("/report/<report_id>/<section_slug>/<question_slug>", methods=["GET", "POST"])
@is_authenticated
def ask_question(report_id, section_slug, question_slug):
    account = {"email": g.account.email}
    report = get_report(report_id)
    context_injector = build_context_injector(this_collection=report.data_collection_instance)
    question = get_data_collection_question(
        report.reporting_round.data_collection_definition_id, section_slug, question_slug
    )
    form = build_question_form(report.data_collection_instance, question, context_injector)
    from_check_your_answers = request.args.get("from_cya", "False") == "True"

    if form.validate_on_submit():
        upsert_question_data(report, question, form.question.data)
        # this needs to happen after we've upserted otherwise it will be missing the latest
        # question to validate conditions
        section_instance_data = next(
            (
                section_data
                for section_data in report.data_collection_instance.section_data
                if section_data.section_id == question.section_id
            ),
            None,
        )
        return redirect(
            _next_url_for_question(
                report_id=report_id,
                section_definition=question.section,
                section_instance_data=section_instance_data,
                current_question=question,
                from_check_your_answers=from_check_your_answers,
            )
        )

    section_instance_data = next(
        (
            section_data
            for section_data in report.data_collection_instance.section_data
            if section_data.section_id == question.section_id
        ),
        None,
    )

    return render_template(
        "report/question_page.html",
        report=report,
        question=question,
        QuestionType=QuestionType,
        section=question.section,
        form=form,
        back_link=_back_link_for_question(
            question, report, from_check_your_answers, section_instance_data=section_instance_data
        ),
        account=account,
    )


@report_blueprint.route("/report/<report_id>/<section_slug>/check-your-answers", methods=["GET", "POST"])
@is_authenticated
def check_your_answers(report_id, section_slug):
    # these are workaronds for having the navigation show or not and aren't really used - this should be more generic
    account = {"email": g.account.email}
    report = get_report(id_=report_id)
    section_data = get_data_collection_instance_section_data(report.data_collection_instance, section_slug)

    form = MarkAsCompleteForm(data={"complete": "yes" if section_data and section_data.completed else None})
    if form.validate_on_submit():
        if form.complete.data is True:
            set_data_collection_instance_section_complete(section_data)

        return redirect(
            url_for(
                "proto_report.tasklist",
                short_name=report.reporting_round.grant.short_name,
                reporting_round_id=report.reporting_round_id,
            )
        )
    return render_template(
        "report/check_your_answers.html",
        report=report,
        section=section_data.section,
        section_data=section_data,
        QuestionType=QuestionType,
        context_injector=build_context_injector(this_collection=report.data_collection_instance),
        get_answer_text_for_question_from_section_data=get_answer_text_for_question_from_section_data,
        form=form,
        account=account,
        visible_questions=get_visible_questions_for_section_instance(
            section_instance_data=section_data, section_definition=section_data.section
        ),
    )
