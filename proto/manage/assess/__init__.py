from flask import flash, g, redirect, render_template, request, session, url_for
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextArea
from wtforms import HiddenField, RadioField, StringField, SubmitField
from wtforms.validators import DataRequired

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.services.applications import (
    add_comment,
    get_application,
    get_comments,
    score_application,
    search_applications,
)
from proto.common.data.services.grants import get_active_round, get_all_grants_with_rounds, get_grant

assess_blueprint = Blueprint("assess", __name__)


class CommentForm(FlaskForm):
    comment = StringField(
        _l("Comment"),
        widget=GovTextArea(),
        validators=[DataRequired(_l("Enter a comment"))],
        description=_l(
            "Use comments to record assessment progress for yourself and other assessors. "
            "Comments on competed grants will not be shared with applicants."
        ),
    )
    action = HiddenField("action")

    submit = SubmitField(_l("Add comment"), widget=GovSubmitInput())


class ScoreForm(FlaskForm):
    score = RadioField(
        _l("Your score"),
        choices=[
            (5, _l("5 Strong")),
            (4, _l("4 Good")),
            (3, _l("3 Satisfactory")),
            (2, _l("2 Partial")),
            (1, _l("1 Poor")),
        ],
        widget=GovRadioInput(),
        validators=[DataRequired(_l("Select a score"))],
    )
    reason = StringField(
        _l("Add a reason for this score"), widget=GovTextArea(), validators=[DataRequired(_l("Enter a reason"))]
    )
    action = HiddenField("action")

    submit = SubmitField(_l("Add score"), widget=GovSubmitInput())


@assess_blueprint.context_processor
def _grants_service_nav():
    return dict(active_navigation_tab="applications")


@assess_blueprint.get("/route/grants/applications")
@is_authenticated(as_platform_admin=True)
def route_grant_applications():
    if session.get("last_selected_grant_short_code"):
        return redirect(
            url_for(
                "proto_manage.assess.list_grant_applications_handler",
                short_code=session.get("last_selected_grant_short_code"),
            )
        )
    else:
        grants = get_all_grants_with_rounds()
        selected_grant = grants[0]
        if selected_grant:
            return redirect(
                url_for("proto_manage.assess.list_grant_applications_handler", short_code=selected_grant.short_name)
            )
        else:
            return redirect(url_for("proto_manage.platform.grants.index"))


@assess_blueprint.get("/grants/<short_code>/applications")
@is_authenticated(as_platform_admin=True)
def list_grant_applications_handler(short_code):
    active_round, grant = get_active_round(short_code)

    if not active_round:
        grant = get_grant(short_code=short_code)
    applications = search_applications(short_code)
    return render_template("manage/assess/grant_list_applications.jinja.html", applications=applications, grant=grant)


@assess_blueprint.route("/grants/<short_code>/applications/<application_id>", methods=["GET", "POST"])
@is_authenticated(as_platform_admin=True)
def assess_application_detail_hander(short_code, application_id):
    form = CommentForm(request.values, action="COMMENT")
    grant = get_grant(short_code)
    application = get_application(application_id)

    if form.validate_on_submit():
        action = form.data.get("action")
        comment = form.data.get("comment")

        if action == "COMMENT":
            add_comment(account=g.account, application=application, comment=comment)
            flash("COMMENT_ADDED")
            return redirect(
                url_for(
                    "proto_manage.assess.assess_application_detail_hander",
                    short_code=short_code,
                    application_id=application_id,
                )
            )

    comments = get_comments(application.id)
    return render_template(
        "manage/assess/assess_application_detail.jinja.html",
        grant=grant,
        application=application,
        comments=comments,
        form=form,
    )


@assess_blueprint.get("/grants/<short_code>/applications/<application_id>/all_answers")
@is_authenticated(as_platform_admin=True)
def assess_application_all_answers_handler(short_code, application_id):
    grant = get_grant(short_code)
    application = get_application(application_id)
    return render_template(
        "manage/assess/assess_application_view_all_answers.html", grant=grant, application=application
    )


@assess_blueprint.route(
    "/grants/<short_code>/applications/<application_id>/section/<section_id>", methods=["GET", "POST"]
)
@is_authenticated(as_platform_admin=True)
def assess_application_section_hander(short_code, application_id, section_id):
    # use enums pls
    form = CommentForm(request.values, action="COMMENT")
    score_form = ScoreForm(request.values, action="SCORE")
    grant = get_grant(short_code)
    application = get_application(application_id)
    section_data = next((x for x in application.data_collection_instance.section_data if str(x.id) == section_id), None)

    # this is really hacky - I'm sure wtf forms has a nice way of doing multiple forms per page, go look that up
    if request.form.get("action") == "COMMENT":
        if form.validate_on_submit():
            comment = form.data.get("comment")

            add_comment(account=g.account, application=application, comment=comment, section=section_data)
            flash("COMMENT_ADDED")
            return redirect(
                url_for(
                    "proto_manage.assess.assess_application_section_hander",
                    short_code=short_code,
                    application_id=application_id,
                    section_id=section_id,
                )
            )
    elif request.form.get("action") == "SCORE":
        if score_form.validate_on_submit():
            score = score_form.data.get("score")
            reason = score_form.data.get("reason")

            score_application(
                account=g.account, application=application, reason=reason, score=score, section=section_data
            )
            flash("SCORE_ADDED")
            return redirect(
                url_for(
                    "proto_manage.assess.assess_application_section_hander",
                    short_code=short_code,
                    application_id=application_id,
                    section_id=section_id,
                )
            )
    comments = get_comments(application.id, section_id=section_id)
    actions = comments + section_data.scores

    return render_template(
        "manage/assess/assess_application_section_detail.html",
        grant=grant,
        application=application,
        section_data=section_data,
        form=form,
        score_form=score_form,
        actions=actions,
    )
