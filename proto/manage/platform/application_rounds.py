from flask import g, redirect, render_template, session, url_for

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.models.question_bank import TemplateType
from proto.common.data.services.applications import create_application
from proto.common.data.services.grants import get_grant_and_round
from proto.common.data.services.question_bank import (
    add_template_sections_to_data_collection_definition,
    create_question,
    create_question_condition,
    create_question_validation,
    create_section,
    ensure_round_has_data_collection_definition,
    get_section_for_data_collection_definition,
    get_template_sections_and_questions,
    update_question,
    update_question_condition,
    update_question_validation,
)
from proto.common.data.services.round import update_round
from proto.form_runner.expressions import build_autocomplete_context
from proto.manage.platform.forms.application_round import (
    MakeRoundLiveForm,
    PreviewApplicationForm,
)
from proto.manage.platform.forms.data_collection import (
    ChooseTemplateSectionsForm,
    NewConditionForm,
    NewQuestionTypeForm,
    NewSectionForm,
    NewValidationForm,
    QuestionForm,
    human_readable,
)

rounds_blueprint = Blueprint("rounds", __name__)


@rounds_blueprint.context_processor
def _rounds_service_nav():
    return dict(active_navigation_tab="grants")


@rounds_blueprint.get("/grants/<grant_code>/rounds/<round_code>")
@is_authenticated(as_platform_admin=True)
def view_round_overview(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    return render_template(
        "manage/platform/application_round/view_round_overview.html",
        grant=grant,
        round=round,
        back_link=url_for("proto_manage.platform.grants.view_grant_rounds", grant_code=grant_code),
        active_sub_navigation_tab="funding",
    )


@rounds_blueprint.get("/grants/<grant_code>/rounds/<round_code>/data-collection")
@is_authenticated(as_platform_admin=True)
def view_round_data_collection(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    form = PreviewApplicationForm(
        submit_label="Preview application", data={"round_id": round.id, "organisation_id": g.account.organisation_id}
    )
    # have a nicer managed method of setting this up and consistently clearing them out
    session.pop("new_question_type", None)
    return render_template(
        "manage/platform/application_round/view_round_data_collection.html",
        grant=grant,
        round=round,
        form=form,
        back_link=url_for("proto_manage.platform.grants.view_grant_rounds", grant_code=grant_code),
        active_sub_navigation_tab="funding",
    )


@rounds_blueprint.route("/grants/<grant_code>/rounds/<round_code>/configuration", methods=["GET", "POST"])
@is_authenticated(as_platform_admin=True)
def view_round_configuration(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    form = MakeRoundLiveForm()
    if form.validate_on_submit():
        update_round(round, draft=False)
        return redirect(
            url_for("proto_manage.platform.rounds.view_round_overview", grant_code=grant_code, round_code=round_code)
        )
    return render_template(
        "manage/platform/application_round/view_round_configuration.html",
        grant=grant,
        round=round,
        form=form,
        back_link=url_for("proto_manage.platform.grants.view_grant_rounds", grant_code=grant_code),
        active_sub_navigation_tab="funding",
    )


@rounds_blueprint.route("/grants/<grant_code>/rounds/<round_code>/choose-from-question-bank", methods=["GET", "POST"])
@is_authenticated(as_platform_admin=True)
def choose_from_question_bank(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    template_sections = get_template_sections_and_questions(template_type=TemplateType.APPLICATION)
    form = ChooseTemplateSectionsForm(template_sections)

    if form.validate_on_submit():
        add_template_sections_to_data_collection_definition(round, form.sections.data)
        return redirect(
            url_for(
                "proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code
            )
        )

    return render_template(
        "manage/platform/choose_from_question_bank.html",
        grant=grant,
        round=round,
        form=form,
        back_link=url_for(
            "proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code
        ),
        active_sub_navigation_tab="funding",
    )


@rounds_blueprint.route("/grants/<grant_code>/rounds/<round_code>/create-section", methods=["GET", "POST"])
@is_authenticated(as_platform_admin=True)
def create_section_view(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    form = NewSectionForm(
        data={
            "order": (
                max(asec.order for asec in round.data_collection_definition.sections)
                if round.data_collection_definition
                else 0
            )
            + 1
        }
    )

    if form.validate_on_submit():
        ensure_round_has_data_collection_definition(round)
        create_section(
            definition_id=round.data_collection_definition.id,
            **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}},
        )
        return redirect(
            url_for(
                "proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code
            )
        )

    return render_template(
        "manage/platform/create_section.html",
        grant=grant,
        round=round,
        form=form,
        back_link=url_for(
            "proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code
        ),
        active_sub_navigation_tab="funding",
    )


@rounds_blueprint.route(
    "/grants/<grant_code>/rounds/<round_code>/sections/<section_id>/create-question/type", methods=["GET", "POST"]
)
@is_authenticated(as_platform_admin=True)
def create_question_type(grant_code, round_code, section_id):
    grant, round = get_grant_and_round(grant_code, round_code)
    section = get_section_for_data_collection_definition(round.data_collection_definition, section_id)
    form = NewQuestionTypeForm(data={"type": session.get("new_question_type")})

    if form.validate_on_submit():
        session["new_question_type"] = form.data.get("type")
        return redirect(
            url_for(
                "proto_manage.platform.rounds.create_question_view",
                grant_code=grant_code,
                round_code=round_code,
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
            "proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code
        ),
    )


# a lot of duplication - the same handler could likely be used for create/ view
@rounds_blueprint.route(
    "/grants/<grant_code>/rounds/<round_code>/sections/<section_id>/question/<question_id>", methods=["GET", "POST"]
)
@is_authenticated(as_platform_admin=True)
def edit_question(grant_code, round_code, section_id, question_id):
    grant, round = get_grant_and_round(grant_code, round_code)
    section = get_section_for_data_collection_definition(round.data_collection_definition, section_id)

    # int ids shouldn't be in the url
    question = next(x for x in section.questions if x.id == int(question_id))

    form = QuestionForm(obj=question, data={"mandatory": "mandatory"})

    if form.validate_on_submit():
        update_question(
            question,
            **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token", "mandatory", "type"}},
        )
        return redirect(
            url_for(
                "proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code
            )
        )

    autocomplete_context = build_autocomplete_context(grant, round.data_collection_definition)
    back_link = url_for(
        "proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code
    )

    return render_template(
        "manage/platform/create_question_add_edit_detail.html",
        grant=grant,
        round=round,
        section=section,
        form=form,
        # horrible - make this consistent with the
        # question_type_human_readbale=human_readable
        question_type_human_readable=human_readable.get(question.type),
        active_sub_navigation_tab="funding",
        back_link=back_link,
        is_edit=True,
        question=question,
        autocomplete_context=autocomplete_context,
    )


@rounds_blueprint.route(
    "/grants/<grant_code>/rounds/<round_code>/sections/<section_id>/question/<question_id>/create-condition",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def create_condition(grant_code, round_code, section_id, question_id):
    grant, round = get_grant_and_round(grant_code, round_code)
    section = get_section_for_data_collection_definition(round.data_collection_definition, section_id)

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
                "proto_manage.platform.rounds.edit_question",
                grant_code=grant_code,
                round_code=round_code,
                section_id=section_id,
                question_id=question_id,
            )
        )

    autocomplete_context = build_autocomplete_context(grant, round.data_collection_definition, answer=True)

    # to not boil the ocean I'll assume you're coming from editing an existing question - we can make this work
    # with nice symetry between create + update but want something in for now
    back_link = url_for(
        "proto_manage.platform.rounds.edit_question",
        grant_code=grant_code,
        round_code=round_code,
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


@rounds_blueprint.route(
    "/grants/<grant_code>/rounds/<round_code>/sections/<section_id>/question/<question_id>/condition/<condition_id>",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def edit_condition(grant_code, round_code, section_id, question_id, condition_id):
    grant, round = get_grant_and_round(grant_code, round_code)
    section = get_section_for_data_collection_definition(round.data_collection_definition, section_id)

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
                "proto_manage.platform.rounds.edit_question",
                grant_code=grant_code,
                round_code=round_code,
                section_id=section_id,
                question_id=question_id,
            )
        )

    autocomplete_context = build_autocomplete_context(grant, round.data_collection_definition, answer=True)

    # to not boil the ocean I'll assume you're coming from editing an existing question - we can make this work
    # with nice symetry between create + update but want something in for now
    back_link = url_for(
        "proto_manage.platform.rounds.edit_question",
        grant_code=grant_code,
        round_code=round_code,
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
        condition=condition,
        is_edit=True,
        autocomplete_context=autocomplete_context,
    )


@rounds_blueprint.route(
    "/grants/<grant_code>/rounds/<round_code>/sections/<section_id>/question/<question_id>/create-validation",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def create_validation(grant_code, round_code, section_id, question_id):
    grant, round = get_grant_and_round(grant_code, round_code)
    section = get_section_for_data_collection_definition(round.data_collection_definition, section_id)

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
                "proto_manage.platform.rounds.edit_question",
                grant_code=grant_code,
                round_code=round_code,
                section_id=section_id,
                question_id=question_id,
            )
        )

    autocomplete_context = build_autocomplete_context(grant, round.data_collection_definition, answer=True)

    # to not boil the ocean I'll assume you're coming from editing an existing question - we can make this work
    # with nice symetry between create + update but want something in for now
    back_link = url_for(
        "proto_manage.platform.rounds.edit_question",
        grant_code=grant_code,
        round_code=round_code,
        section_id=section_id,
        question_id=question_id,
    )

    return render_template(
        "manage/platform/create_question_add_validation.html",
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


@rounds_blueprint.route(
    "/grants/<grant_code>/rounds/<round_code>/sections/<section_id>/question/<question_id>/validation/<validation_id>",
    methods=["GET", "POST"],
)
@is_authenticated(as_platform_admin=True)
def edit_validation(grant_code, round_code, section_id, question_id, validation_id):
    grant, round = get_grant_and_round(grant_code, round_code)
    section = get_section_for_data_collection_definition(round.data_collection_definition, section_id)

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
                "proto_manage.platform.rounds.edit_question",
                grant_code=grant_code,
                round_code=round_code,
                section_id=section_id,
                question_id=question_id,
            )
        )

    autocomplete_context = build_autocomplete_context(grant, round.data_collection_definition, answer=True)

    # to not boil the ocean I'll assume you're coming from editing an existing question - we can make this work
    # with nice symetry between create + update but want something in for now
    back_link = url_for(
        "proto_manage.platform.rounds.edit_question",
        grant_code=grant_code,
        round_code=round_code,
        section_id=section_id,
        question_id=question_id,
    )

    return render_template(
        "manage/platform/create_question_add_validation.html",
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
        validation=validation,
        is_edit=True,
        autocomplete_context=autocomplete_context,
    )


@rounds_blueprint.route(
    "/grants/<grant_code>/rounds/<round_code>/sections/<section_id>/create-question", methods=["GET", "POST"]
)
@is_authenticated(as_platform_admin=True)
def create_question_view(grant_code, round_code, section_id):
    grant, round = get_grant_and_round(grant_code, round_code)
    section = get_section_for_data_collection_definition(round.data_collection_definition, section_id)

    # should do things if the session isn't appropriately set up for this
    # stage in the journey but - proto<< HEAD
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
                "proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code
            )
        )

    autocomplete_context = build_autocomplete_context(grant, round.data_collection_definition)
    back_link = (
        url_for("proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code)
        if not session.get("new_question_type")
        else url_for(
            "proto_manage.platform.rounds.create_question_type",
            grant_code=grant_code,
            round_code=round_code,
            section_id=section_id,
        )
    )

    return render_template(
        "manage/platform/create_question_add_edit_detail.html",
        grant=grant,
        round=round,
        section=section,
        form=form,
        # horrible - make this consistent with the
        # question_type_human_readbale=human_readable
        question_type_human_readable=human_readable.get(session.get("new_question_type")),
        active_sub_navigation_tab="funding",
        autocomplete_context=autocomplete_context,
        back_link=back_link,
    )


@rounds_blueprint.post("/grants/<grant_code>/rounds/<round_code>/preview-application")
@is_authenticated(as_platform_admin=True)
def preview_application(grant_code, round_code):
    form = PreviewApplicationForm(submit_label=None)
    if form.validate_on_submit():
        application = create_application(
            preview=True, round_id=form.round_id.data, organisation_id=form.organisation_id.data
        )
        return redirect(
            url_for("proto_apply.application.application_tasklist", application_external_id=application.external_id)
        )

    raise Exception(f"Failed to start application: {form.data}")
