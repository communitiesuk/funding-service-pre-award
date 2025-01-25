from urllib.parse import urljoin

from flask import current_app, redirect, render_template, session, url_for
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovSubmitInput, GovTextInput
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

from common.blueprints import Blueprint
from config import Config
from proto.common.auth import maybe_authenticated
from proto.common.data.services.magic_links import (
    claim_magic_link,
    create_magic_link,
    get_magic_link,
    get_magic_link_by_id,
)
from services.notify import get_notification_service

web_blueprint = Blueprint("web", __name__)


class MagicLinkForm(FlaskForm):
    email = StringField(
        _l("Email address"),
        widget=GovTextInput(),
        validators=[
            DataRequired(_l("Enter an email address")),
            Email(_l("Enter an email address in the correct format, like name@example.com")),
        ],
        description=_l(
            "We'll email you a link to start a new application, or continue any applications you have in progress."
        ),
    )

    submit = SubmitField(_l("Continue"), widget=GovSubmitInput())


@web_blueprint.get("/cookies")
def cookies_handler():
    return render_template("apply/web/cookies.jinja.html")


@web_blueprint.get("/accessibility")
def accessibility_statement_handler():
    return render_template("apply/web/accessibility.jinja.html")


@web_blueprint.route("/auth/magic_links", methods=["GET", "POST"])
@maybe_authenticated
def magic_links_enter_email_handler():
    form = MagicLinkForm()
    if form.validate_on_submit():
        path = session.get("magic_links_forward_path", url_for("proto_apply.grant_blueprint.all_open_grants_handler"))
        magic_link = create_magic_link(email=form.data.get("email"), path=path)

        if current_app.config["BYPASS_NOTIFY_SORRY_STEVEN"]:
            return redirect(url_for("proto_apply.web.magic_links_return_handler", token=magic_link.token))

        get_notification_service().proto_send_magic_link(magic_link=magic_link)
        return redirect(url_for("proto_apply.web.magic_links_confirm_email_handler", external_id=magic_link.id))

    return render_template(
        "apply/auth/magic_links/enter_email.jinja.html",
        magic_links_back_path=session.get("magic_links_back_path"),
        form=form,
    )


@web_blueprint.get("/auth/magic_links/<external_id>")
def magic_links_confirm_email_handler(external_id):
    magic_link = get_magic_link_by_id(external_id)
    return render_template(
        "apply/auth/magic_links/confirm_email.jinja.html",
        magic_link=magic_link,
        original_url=urljoin(Config.APPLICANT_FRONTEND_HOST, magic_link.path),
    )


@web_blueprint.get("/auth/return/magic_links/<token>")
def magic_links_return_handler(token):
    magic_link = get_magic_link(token=token)
    account = claim_magic_link(magic_link=magic_link)

    origin_path = session.pop("magic_links_back_path", None)
    session.pop("magic_links_forward_path", None)

    session["is_authenticated"] = True
    session["magic_links_account_id"] = account.id
    session["magic_links_origin_path"] = origin_path

    return redirect(urljoin(Config.APPLICANT_FRONTEND_HOST, magic_link.path))


@web_blueprint.get("/auth/sign_out")
def magic_links_sign_out_handler():
    origin_path = session.pop("magic_links_origin_path", None)
    session.clear()
    if origin_path:
        return redirect(urljoin(Config.APPLICANT_FRONTEND_HOST, origin_path))
    else:
        # there is no real "home" on the apply tool as its linked to by other tools - this would
        # need a specific interstitial page telling you to go back to where you found the link
        return redirect("/")
