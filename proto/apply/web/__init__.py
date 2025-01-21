from urllib.parse import urljoin

from flask import redirect, render_template, request, session, url_for

from common.blueprints import Blueprint
from config import Config
from proto.common.data.services.magic_links import (
    claim_magic_link,
    create_magic_link,
    get_magic_link,
    get_magic_link_by_id,
)
from services.notify import get_notification_service

web_blueprint = Blueprint("web", __name__)


@web_blueprint.get("/cookies")
def cookies_handler():
    return render_template("apply/web/cookies.jinja.html")


@web_blueprint.get("/accessibility")
def accessibility_statement_handler():
    return render_template("apply/web/accessibility.jinja.html")


@web_blueprint.get("/auth/magic_links")
def magic_links_enter_email_handler():
    return render_template(
        "apply/auth/magic_links/enter_email.jinja.html", magic_links_back_path=session.get("magic_links_back_path")
    )


@web_blueprint.get("/auth/magic_links/<external_id>")
def magic_links_confirm_email_handler(external_id):
    magic_link = get_magic_link_by_id(external_id)
    return render_template(
        "apply/auth/magic_links/confirm_email.jinja.html",
        magic_link=magic_link,
        original_url=urljoin(Config.APPLICANT_FRONTEND_HOST, magic_link.path),
    )


@web_blueprint.post("/auth/magic_links")
def magic_links_submit_email_handler():
    # replace with parsing from wtfforms
    email = request.form["email"]
    path = session.get("magic_links_forward_path")

    magic_link = create_magic_link(email=email, path=path)
    get_notification_service().proto_send_magic_link(magic_link=magic_link)
    return redirect(url_for("proto_apply.web.magic_links_confirm_email_handler", external_id=magic_link.id))


@web_blueprint.get("/auth/return/magic_links/<token>")
def magic_links_return_handler(token):
    magic_link = get_magic_link(token=token)
    account = claim_magic_link(magic_link=magic_link)

    origin_path = session.pop("magic_links_back_path", None)
    session.pop("magic_links_forward_path", None)

    session["is_authenticated"] = True
    session["magic_links_account_id"] = account.id
    session["magic_links_account_email"] = account.email
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
