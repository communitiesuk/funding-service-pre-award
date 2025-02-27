from flask import g, redirect, render_template, url_for

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.exceptions import DataValidationError, attach_validation_error_to_form
from proto.common.data.models.question_bank import TemplateType
from proto.common.data.services.grants import get_grant, get_grant_and_reporting_round
from proto.common.data.services.question_bank import (
    add_template_sections_to_data_collection_definition,
    create_question,
    create_section,
    get_section_for_data_collection_definition,
    get_template_sections_and_questions,
)
from proto.common.data.services.reporting_round import create_reporting_round, update_reporting_round
from proto.form_runner.expressions import build_autocomplete_context
from proto.manage.platform.forms.data_collection import ChooseTemplateSectionsForm, NewQuestionForm, NewSectionForm
from proto.manage.platform.forms.reporting_round import (
    CreateReportingRoundForm,
    PreviewReportForm,
    PublishReportingRoundForm,
)

reporting_rounds_blueprint = Blueprint("reporting_rounds", __name__)


@reporting_rounds_blueprint.context_processor
def _reporting_rounds_service_nav():
    return dict(active_navigation_tab="grants")


@reporting_rounds_blueprint.route("/grants/<grant_code>/create-reporting-round", methods=["GET", "POST"])
@is_authenticated(as_platform_admin=True)
def create_reporting_round_view(grant_code):
    grant = get_grant(grant_code)
    form = CreateReportingRoundForm()
    if form.validate_on_submit():
        try:
            reporting_round = create_reporting_round(
                grant_id=grant.id,
                reporting_period_starts=form.reporting_period_starts.data,
                reporting_period_ends=form.reporting_period_ends.data,
                submission_period_starts=form.submission_period_starts.data,
                submission_period_ends=form.submission_period_ends.data,
            )
        except DataValidationError as e:
            attach_validation_error_to_form(form, e)
        else:
            return redirect(
                url_for(
                    "proto_manage.platform.reporting_rounds.view_reporting_round_overview",
                    grant_code=grant_code,
                    round_ext_id=reporting_round.external_id,
                )
            )

    return render_template(
        "manage/platform/reporting_round/create_round.html",
        form=form,
        grant=grant,
        active_sub_navigation_tab="monitoring",
        back_link=url_for("proto_manage.platform.grants.view_grant_reporting_rounds", grant_code=grant_code),
    )


@reporting_rounds_blueprint.get("/grants/<grant_code>/reporting-rounds/<round_ext_id>")
@is_authenticated(as_platform_admin=True)
def view_reporting_round_overview(grant_code, round_ext_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    return render_template(
        "manage/platform/reporting_round/view_round_overview.html",
        grant=grant,
        round=reporting_round,
        back_link=url_for("proto_manage.platform.grants.view_grant_reporting_rounds", grant_code=grant_code),
        active_sub_navigation_tab="monitoring",
    )


@reporting_rounds_blueprint.get("/grants/<grant_code>/reporting-rounds/<round_ext_id>/data-collection")
@is_authenticated(as_platform_admin=True)
def view_reporting_round_data_collection(grant_code, round_ext_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    form = PreviewReportForm(
        submit_label="Preview report",
        data={"round_id": reporting_round.id, "organisation_id": g.account.organisation_id},
    )
    return render_template(
        "manage/platform/reporting_round/view_round_data_collection.html",
        grant=grant,
        round=reporting_round,
        form=form,
        back_link=url_for("proto_manage.platform.grants.view_grant_reporting_rounds", grant_code=grant_code),
        active_sub_navigation_tab="monitoring",
    )


@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/configuration", methods=["GET", "POST"]
)
@is_authenticated(as_platform_admin=True)
def view_reporting_round_configuration(grant_code, round_ext_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    form = PublishReportingRoundForm()
    if form.validate_on_submit():
        update_reporting_round(reporting_round, preview=False)
        return redirect(
            url_for(
                "proto_manage.platform.reporting_rounds.view_reporting_round_overview",
                grant_code=grant_code,
                round_ext_id=round_ext_id,
            )
        )
    return render_template(
        "manage/platform/reporting_round/view_round_configuration.html",
        grant=grant,
        round=reporting_round,
        form=form,
        back_link=url_for("proto_manage.platform.grants.view_grant_reporting_rounds", grant_code=grant_code),
        active_sub_navigation_tab="monitoring",
    )


@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/choose-from-question-bank", methods=["GET", "POST"]
)
@is_authenticated(as_platform_admin=True)
def choose_from_question_bank(grant_code, round_ext_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    template_sections = get_template_sections_and_questions(template_type=TemplateType.REPORTING)
    form = ChooseTemplateSectionsForm(template_sections)

    if form.validate_on_submit():
        add_template_sections_to_data_collection_definition(reporting_round, form.sections.data)
        return redirect(
            url_for(
                "proto_manage.platform.reporting_rounds.view_reporting_round_data_collection",
                grant_code=grant_code,
                round_ext_id=round_ext_id,
            )
        )

    return render_template(
        "manage/platform/choose_from_question_bank.html",
        grant=grant,
        reporting_round=reporting_round,
        form=form,
        back_link=url_for(
            "proto_manage.platform.reporting_rounds.view_reporting_round_data_collection",
            grant_code=grant_code,
            round_ext_id=round_ext_id,
        ),
        active_sub_navigation_tab="monitoring",
    )


@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/create-section", methods=["GET", "POST"]
)
@is_authenticated(as_platform_admin=True)
def create_section_view(grant_code, round_ext_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    form = NewSectionForm(
        data={"order": max(asec.order for asec in reporting_round.data_collection_definition.sections) + 1}
    )

    if form.validate_on_submit():
        create_section(
            definition_id=reporting_round.data_collection_definition.id,
            **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}},
        )
        return redirect(
            url_for(
                "proto_manage.platform.reporting_rounds.view_reporting_round_data_collection",
                grant_code=grant_code,
                round_ext_id=round_ext_id,
            )
        )

    return render_template(
        "manage/platform/create_section.html",
        grant=grant,
        reporting_round=reporting_round,
        form=form,
        active_sub_navigation_tab="monitoring",
    )


@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/sections/<section_id>/create-question",
    methods=["GET", "POST"],
)
@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/sections/<section_id>/questions/<question_id>",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def create_question_view(grant_code, round_ext_id, section_id, question_id=None):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    section = get_section_for_data_collection_definition(reporting_round.data_collection_definition, section_id)
    form = NewQuestionForm(data={"order": (max(q.order for q in section.questions) if section.questions else 0) + 1})

    if form.validate_on_submit():
        create_question(
            section_id=section.id,
            **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token", "mandatory"}},
        )
        return redirect(
            url_for(
                "proto_manage.platform.reporting_rounds.view_reporting_round_data_collection",
                grant_code=grant_code,
                round_ext_id=round_ext_id,
            )
        )
    autocomplete_context = build_autocomplete_context(grant, reporting_round.data_collection_definition)
    return render_template(
        "manage/platform/create_question.html",
        grant=grant,
        reporting_round=reporting_round,
        section=section,
        form=form,
        autocomplete_context=autocomplete_context,
        active_sub_navigation_tab="monitoring",
    )


@reporting_rounds_blueprint.post("/grants/<grant_code>/reporting-rounds/<round_ext_id>/preview-report")
@is_authenticated(as_platform_admin=True)
def preview_report(grant_code, round_ext_id):
    # form = PreviewApplicationForm(submit_label=None)
    # if form.validate_on_submit():
    #     application = create_application(
    #         preview=True, reporting_round_id=form.reporting_round_id.data, account_id=form.account_id.data
    #     )
    #     return redirect(url_for("proto_apply.application.application_tasklist",
    #     application_external_id=application.external_id))
    #
    # raise Exception(f"Failed to start application: {form.data}")
    return "hi"
