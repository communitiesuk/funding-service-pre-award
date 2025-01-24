import datetime

from flask import g, redirect, render_template, url_for

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.exceptions import DataValidationError, attach_validation_error_to_form
from proto.common.data.services.applications import create_application
from proto.common.data.services.grants import get_grant, get_grant_and_round
from proto.common.data.services.question_bank import (
    add_template_sections_to_data_collection_definition,
    create_question,
    create_section,
    get_application_template_sections_and_questions,
    get_section_for_data_collection_definition,
)
from proto.common.data.services.round import create_round, update_round
from proto.manage.platform import (
    ChooseTemplateSectionsForm,
    CreateRoundForm,
    MakeRoundLiveForm,
    NewQuestionForm,
    NewSectionForm,
    PreviewApplicationForm,
)

rounds_blueprint = Blueprint("rounds", __name__)


@rounds_blueprint.context_processor
def _rounds_service_nav():
    return dict(active_navigation_tab="rounds")


@rounds_blueprint.route("/grants/<grant_code>/create-round", methods=["GET", "POST"])
@is_authenticated
def create_round_view(grant_code):
    grant = get_grant(grant_code)
    form = CreateRoundForm()
    if form.validate_on_submit():
        try:
            round = create_round(
                fund_id=grant.id,
                **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}},
                proto_start_date=datetime.date(2025, 1, 1),
                proto_end_date=datetime.date(2025, 1, 31),
            )
        except DataValidationError as e:
            attach_validation_error_to_form(form, e)
        else:
            return redirect(
                url_for(
                    "proto_manage.platform.rounds.view_round_overview",
                    grant_code=grant_code,
                    round_code=round.short_name,
                )
            )

    return render_template(
        "manage/platform/create_round.html",
        form=form,
        back_link=url_for("proto_manage.platform.grants.view_grant_rounds", grant_code=grant_code),
    )


@rounds_blueprint.get("/grants/<grant_code>/rounds/<round_code>")
@is_authenticated
def view_round_overview(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    return render_template(
        "manage/platform/view_round_overview.html",
        grant=grant,
        round=round,
        back_link=url_for("proto_manage.platform.grants.view_grant_rounds", grant_code=grant_code),
    )


@rounds_blueprint.get("/grants/<grant_code>/rounds/<round_code>/data-collection")
@is_authenticated
def view_round_data_collection(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    form = PreviewApplicationForm(
        submit_label="Preview application", data={"round_id": round.id, "account_id": g.account.id}
    )
    return render_template(
        "manage/platform/view_round_data_collection.html",
        grant=grant,
        round=round,
        form=form,
        back_link=url_for("proto_manage.platform.grants.view_grant_rounds", grant_code=grant_code),
    )


@rounds_blueprint.route("/grants/<grant_code>/rounds/<round_code>/configuration", methods=["GET", "POST"])
@is_authenticated
def view_round_configuration(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    form = MakeRoundLiveForm()
    if form.validate_on_submit():
        update_round(round, draft=False)
        return redirect(
            url_for("proto_manage.platform.rounds.view_round_overview", grant_code=grant_code, round_code=round_code)
        )
    return render_template(
        "manage/platform/view_round_configuration.html",
        grant=grant,
        round=round,
        form=form,
        back_link=url_for("proto_manage.platform.grants.view_grant_rounds", grant_code=grant_code),
    )


@rounds_blueprint.route("/grants/<grant_code>/rounds/<round_code>/choose-from-question-bank", methods=["GET", "POST"])
@is_authenticated
def choose_from_question_bank(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    template_sections = get_application_template_sections_and_questions()
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
    )


@rounds_blueprint.route("/grants/<grant_code>/rounds/<round_code>/create-section", methods=["GET", "POST"])
@is_authenticated
def create_section_view(grant_code, round_code):
    grant, round = get_grant_and_round(grant_code, round_code)
    form = NewSectionForm(data={"order": max(asec.order for asec in round.data_collection_definition.sections) + 1})

    if form.validate_on_submit():
        create_section(round_id=round.id, **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}})
        return redirect(
            url_for(
                "proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code
            )
        )

    return render_template("manage/platform/create_section.html", grant=grant, round=round, form=form)


@rounds_blueprint.route(
    "/grants/<grant_code>/rounds/<round_code>/sections/<section_id>/create-question", methods=["GET", "POST"]
)
@is_authenticated
def create_question_view(grant_code, round_code, section_id):
    grant, round = get_grant_and_round(grant_code, round_code)
    section = get_section_for_data_collection_definition(round.data_collection_definition, section_id)
    form = NewQuestionForm(data={"order": (max(q.order for q in section.questions) if section.questions else 0) + 1})

    if form.validate_on_submit():
        create_question(
            section_id=section.id, **{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}}
        )
        return redirect(
            url_for(
                "proto_manage.platform.rounds.view_round_data_collection", grant_code=grant_code, round_code=round_code
            )
        )
    return render_template("manage/platform/create_question.html", grant=grant, round=round, section=section, form=form)


@rounds_blueprint.post("/grants/<grant_code>/rounds/<round_code>/preview-application")
@is_authenticated
def preview_application(grant_code, round_code):
    form = PreviewApplicationForm(submit_label=None)
    if form.validate_on_submit():
        application = create_application(preview=True, round_id=form.round_id.data, account_id=form.account_id.data)
        return redirect(url_for("proto_apply.application.application_tasklist", application_id=application.id))

    raise Exception(f"Failed to start application: {form.data}")
