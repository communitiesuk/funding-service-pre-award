from flask import g, redirect, render_template, session, url_for
from flask_babel import lazy_gettext as _l

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.exceptions import DataValidationError, attach_validation_error_to_form
from proto.common.data.models.question_bank import QuestionType, TemplateType
from proto.common.data.services.grants import get_grant, get_grant_and_reporting_round
from proto.common.data.services.question_bank import (
    add_template_sections_to_data_collection_definition,
    create_question,
    create_question_condition,
    create_question_validation,
    create_section,
    ensure_round_has_data_collection_definition,
    get_data_collection_definition_question,
    get_section_for_data_collection_definition,
    get_template_sections_and_questions,
    update_question,
    update_question_condition,
    update_question_validation,
)
from proto.common.data.services.recipients import get_grant_recipient_for_organisation
from proto.common.data.services.reporting_round import create_reporting_round, update_reporting_round
from proto.common.data.services.reports import get_or_create_monitoring_reports_for_grant_recipient
from proto.form_runner.expressions import build_autocomplete_context
from proto.manage.platform.forms.data_collection import (
    ChooseTemplateSectionsForm,
    NewConditionForm,
    NewQuestionTypeForm,
    NewSectionForm,
    NewValidationForm,
    QuestionForm,
    human_readable,
)
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
        data={
            "order": (
                max(asec.order for asec in reporting_round.data_collection_definition.sections)
                if reporting_round.data_collection_definition
                else 0
            )
            + 1
        }
    )

    if form.validate_on_submit():
        ensure_round_has_data_collection_definition(reporting_round)
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
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/sections/<section_id>/create-question/type",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def create_question_type(grant_code, round_ext_id, section_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    section = get_section_for_data_collection_definition(reporting_round.data_collection_definition, section_id)
    form = NewQuestionTypeForm(data={"type": session.get("new_question_type")})

    if form.validate_on_submit():
        session["new_question_type"] = form.data.get("type")
        return redirect(
            url_for(
                "proto_manage.platform.reporting_rounds.create_question_view",
                grant_code=grant_code,
                round_ext_id=round_ext_id,
                section_id=section_id,
            )
        )

    return render_template(
        "manage/platform/create_question_add_type.html",
        grant=grant,
        round=round,
        section=section,
        form=form,
        active_sub_navigation_tab="funding",
        back_link=url_for(
            "proto_manage.platform.reporting_rounds.view_reporting_round_data_collection",
            grant_code=grant_code,
            round_ext_id=round_ext_id,
        ),
    )


@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/sections/<section_id>/create-question",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def create_question_view(grant_code, round_ext_id, section_id, question_id=None):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    section = get_section_for_data_collection_definition(reporting_round.data_collection_definition, section_id)
    form = QuestionForm(
        data={
            "order": (max(q.order for q in section.questions) if section.questions else 0) + 1,
            "type": session.get("new_question_type"),
        }
    )

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
        "manage/platform/create_question_add_edit_detail.html",
        grant=grant,
        reporting_round=reporting_round,
        question_type_human_readable=human_readable.get(QuestionType(session.get("new_question_type"))),
        section=section,
        form=form,
        autocomplete_context=autocomplete_context,
        back_link=url_for(
            "proto_manage.platform.reporting_rounds.view_reporting_round_data_collection",
            grant_code=grant_code,
            round_ext_id=round_ext_id,
        ),
        active_sub_navigation_tab="monitoring",
    )


@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/sections/<section_id>/edit-question/<question_id>",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def edit_question_view(grant_code, round_ext_id, section_id, question_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    question = get_data_collection_definition_question(
        reporting_round.data_collection_definition, section_id, question_id
    )
    section = question.section
    form = QuestionForm(obj=question, data={"mandatory": "mandatory"}, submit_label=_l("Update question"))
    form.type.data = question.type.value  # hack

    if form.validate_on_submit():
        update_question(
            question=question,
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
        "manage/platform/create_question_add_edit_detail.html",
        grant=grant,
        reporting_round=reporting_round,
        question_type_human_readable=human_readable.get(question.type),
        section=section,
        question=question,
        form=form,
        autocomplete_context=autocomplete_context,
        back_link=url_for(
            "proto_manage.platform.reporting_rounds.view_reporting_round_data_collection",
            grant_code=grant_code,
            round_ext_id=round_ext_id,
        ),
        active_sub_navigation_tab="monitoring",
    )


@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/sections/<section_id>/question/<question_id>/create-condition",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def create_condition(grant_code, round_ext_id, section_id, question_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    section = get_section_for_data_collection_definition(reporting_round.data_collection_definition, section_id)

    # int ids shouldn't be in the url
    question = next(x for x in section.questions if x.id == int(question_id))

    form = NewConditionForm()

    if form.validate_on_submit():
        create_question_condition(
            question,
            **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}},
        )
        return redirect(
            url_for(
                "proto_manage.platform.reporting_rounds.edit_question_view",
                grant_code=grant_code,
                round_ext_id=round_ext_id,
                section_id=section_id,
                question_id=question_id,
            )
        )

    autocomplete_context = build_autocomplete_context(grant, reporting_round.data_collection_definition)

    # to not boil the ocean I'll assume you're coming from editing an existing question - we can make this work
    # with nice symetry between create + update but want something in for now
    back_link = url_for(
        "proto_manage.platform.reporting_rounds.edit_question_view",
        grant_code=grant_code,
        round_ext_id=round_ext_id,
        section_id=section_id,
        question_id=question_id,
    )

    return render_template(
        "manage/platform/create_question_add_condition.html",
        grant=grant,
        round=round,
        section=section,
        form=form,
        # horrible - make this consistent with the
        # question_type_human_readbale=human_readable
        question_type_human_readable=human_readable.get(question.type),
        active_sub_navigation_tab="funding",
        back_link=back_link,
        question=question,
        autocomplete_context=autocomplete_context,
    )


@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/sections/<section_id>/question/<question_id>/condition/<condition_id>",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def edit_condition(grant_code, round_ext_id, section_id, question_id, condition_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    section = get_section_for_data_collection_definition(reporting_round.data_collection_definition, section_id)

    # int ids shouldn't be in the url
    question = next(x for x in section.questions if x.id == int(question_id))

    condition = next(x for x in question.conditions if x.id == int(condition_id))

    form = NewConditionForm(obj=condition)

    if form.validate_on_submit():
        update_question_condition(
            condition,
            **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}},
        )
        return redirect(
            url_for(
                "proto_manage.platform.reporting_rounds.edit_question_view",
                grant_code=grant_code,
                round_ext_id=round_ext_id,
                section_id=section_id,
                question_id=question_id,
            )
        )

    autocomplete_context = build_autocomplete_context(grant, reporting_round.data_collection_definition)

    # to not boil the ocean I'll assume you're coming from editing an existing question - we can make this work
    # with nice symetry between create + update but want something in for now
    back_link = url_for(
        "proto_manage.platform.reporting_rounds.edit_question_view",
        grant_code=grant_code,
        round_ext_id=round_ext_id,
        section_id=section_id,
        question_id=question_id,
    )

    return render_template(
        "manage/platform/create_question_add_condition.html",
        grant=grant,
        reporting_round=reporting_round,
        section=section,
        form=form,
        # horrible - make this consistent with the
        # question_type_human_readbale=human_readable
        question_type_human_readable=human_readable.get(question.type),
        active_sub_navigation_tab="funding",
        back_link=back_link,
        question=question,
        condition=condition,
        is_edit=True,
        autocomplete_context=autocomplete_context,
    )


@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/sections/<section_id>/question/<question_id>/create-validation",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def create_validation(grant_code, round_ext_id, section_id, question_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    section = get_section_for_data_collection_definition(reporting_round.data_collection_definition, section_id)

    # int ids shouldn't be in the url
    question = next(x for x in section.questions if x.id == int(question_id))

    form = NewValidationForm()

    if form.validate_on_submit():
        create_question_validation(
            question,
            **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}},
        )
        return redirect(
            url_for(
                "proto_manage.platform.reporting_rounds.edit_question_view",
                grant_code=grant_code,
                round_ext_id=round_ext_id,
                section_id=section_id,
                question_id=question_id,
            )
        )

    autocomplete_context = build_autocomplete_context(grant, reporting_round.data_collection_definition, answer=True)

    # to not boil the ocean I'll assume you're coming from editing an existing question - we can make this work
    # with nice symetry between create + update but want something in for now
    back_link = url_for(
        "proto_manage.platform.reporting_rounds.edit_question_view",
        grant_code=grant_code,
        round_ext_id=round_ext_id,
        section_id=section_id,
        question_id=question_id,
    )

    return render_template(
        "manage/platform/create_question_add_validation.html",
        grant=grant,
        reporting_round=reporting_round,
        section=section,
        form=form,
        # horrible - make this consistent with the
        # question_type_human_readbale=human_readable
        question_type_human_readable=human_readable.get(question.type),
        active_sub_navigation_tab="funding",
        back_link=back_link,
        question=question,
        autocomplete_context=autocomplete_context,
    )


@reporting_rounds_blueprint.route(
    "/grants/<grant_code>/reporting-rounds/<round_ext_id>/sections/<section_id>/question/<question_id>/validation/<validation_id>",  # noqa
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def edit_validation(grant_code, round_ext_id, section_id, question_id, validation_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    section = get_section_for_data_collection_definition(reporting_round.data_collection_definition, section_id)

    # int ids shouldn't be in the url
    question = next(x for x in section.questions if x.id == int(question_id))

    validation = next(x for x in question.validations if x.id == int(validation_id))

    form = NewValidationForm(obj=validation)

    if form.validate_on_submit():
        update_question_validation(
            validation,
            **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}},
        )
        return redirect(
            url_for(
                "proto_manage.platform.reporting_rounds.edit_question_view",
                grant_code=grant_code,
                round_ext_id=round_ext_id,
                section_id=section_id,
                question_id=question_id,
            )
        )

    autocomplete_context = build_autocomplete_context(grant, reporting_round.data_collection_definition, answer=True)

    # to not boil the ocean I'll assume you're coming from editing an existing question - we can make this work
    # with nice symetry between create + update but want something in for now
    back_link = url_for(
        "proto_manage.platform.reporting_rounds.edit_question_view",
        grant_code=grant_code,
        round_ext_id=round_ext_id,
        section_id=section_id,
        question_id=question_id,
    )

    return render_template(
        "manage/platform/create_question_add_validation.html",
        grant=grant,
        reporting_round=reporting_round,
        section=section,
        form=form,
        # horrible - make this consistent with the
        # question_type_human_readbale=human_readable
        question_type_human_readable=human_readable.get(question.type),
        active_sub_navigation_tab="funding",
        back_link=back_link,
        question=question,
        validation=validation,
        is_edit=True,
        autocomplete_context=autocomplete_context,
    )


@reporting_rounds_blueprint.post("/grants/<grant_code>/reporting-rounds/<round_ext_id>/preview-report")
@is_authenticated(as_platform_admin=True)
def preview_report(grant_code, round_ext_id):
    grant, reporting_round = get_grant_and_reporting_round(grant_code, round_ext_id)
    form = PreviewReportForm(submit_label=None)
    if form.validate_on_submit():
        get_or_create_monitoring_reports_for_grant_recipient(
            get_grant_recipient_for_organisation(g.account.organisation_id, grant.short_name)
        )
        return redirect(
            url_for("proto_report.tasklist", short_name=grant.short_name, reporting_round_id=reporting_round.id)
        )

    raise Exception(f"Failed to start report: {form.data}")
