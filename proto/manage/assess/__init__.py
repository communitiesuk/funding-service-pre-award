from flask import flash, g, redirect, render_template, request, session, url_for
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovSubmitInput, GovTextArea
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.services.applications import add_comment, get_application, search_applications
from proto.common.data.services.grants import get_active_round, get_all_grants_with_rounds, get_grant

assess_blueprint = Blueprint("assess", __name__)


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


@assess_blueprint.get("/grants/<short_code>/applications/<application_id>")
@is_authenticated(as_platform_admin=True)
def assess_application_detail_hander(short_code, application_id):
    grant = get_grant(short_code)
    application = get_application(application_id)
    return render_template("manage/assess/assess_application_detail.jinja.html", grant=grant, application=application)


@assess_blueprint.get("/grants/<short_code>/applications/<application_id>/all_answers")
@is_authenticated(as_platform_admin=True)
def assess_application_all_answers_handler(short_code, application_id):
    grant = get_grant(short_code)
    application = get_application(application_id)
    return render_template(
        "manage/assess/assess_application_view_all_answers.html", grant=grant, application=application
    )


class CommentForm(FlaskForm):
    comment = StringField(
        _l("Comment on this section"),
        widget=GovTextArea(),
        validators=[DataRequired(_l("Enter a comment"))],
        description=_l(
            "Use comments to record assessment progress for yourself and other assessors. "
            "Comments on competed grants will not be shared with applicants."
        ),
    )
    action = HiddenField("action")

    submit = SubmitField(_l("Add comment"), widget=GovSubmitInput())


@assess_blueprint.route(
    "/grants/<short_code>/applications/<application_id>/section/<section_id>", methods=["GET", "POST"]
)
@is_authenticated(as_platform_admin=True)
def assess_application_section_hander(short_code, application_id, section_id):
    # use enums why not
    form = CommentForm(request.values, action="COMMENT")
    grant = get_grant(short_code)
    application = get_application(application_id)
    section_data = next((x for x in application.data_collection_instance.section_data if str(x.id) == section_id), None)

    if form.validate_on_submit():
        action = form.data.get("action")
        comment = form.data.get("comment")

        if action == "COMMENT":
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

    return render_template(
        "manage/assess/assess_application_section_detail.html",
        grant=grant,
        application=application,
        section_data=section_data,
        form=form,
    )
