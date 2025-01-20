from urllib.parse import urljoin

from flask import redirect, render_template, request, session, url_for

from common.blueprints import Blueprint
from config import Config
from proto.common.data.services.magic_links import create_magic_link, get_magic_link, get_magic_link_by_id, set_used
from services.notify import get_notification_service

web_blueprint = Blueprint("web_blueprint", __name__)


@web_blueprint.get("/cookies")
def cookies_handler():
    return render_template("web/cookies.jinja.html")


@web_blueprint.get("/accessibility")
def accessibility_statement_handler():
    return render_template("web/accessibility.jinja.html")


# happy to move this to an auth_routes if people think thats cleaner
# for now I'm putting the grant your trying to access in the session, this could also go in the URL
@web_blueprint.get("/auth/magic_links")
def magic_links_enter_email_handler():
    # should the magic link work without a specific short code, it requires a short code should that go in the URL
    # rather than in the sessiona

    # needs to decide what to do if it cant access this
    # either I put this in on the page here or I just load it in the post controller
    # session.get("magic_links_forward_path")
    return render_template(
        "auth/magic_links/enter_email.jinja.html", magic_links_back_path=session.get("magic_links_back_path")
    )


@web_blueprint.get("/auth/magic_links/<external_id>")
def magic_links_confirm_email_handler(external_id):
    magic_link = get_magic_link_by_id(external_id)
    return render_template(
        "auth/magic_links/confirm_email.jinja.html",
        magic_link=magic_link,
        original_url=urljoin(Config.APPLICANT_FRONTEND_HOST, magic_link.path),
    )


# am I OK with this POST rendering the confirmation page or do I want it to redirect to a page
# that can be refreshed without actions that will render the page (based on the token its expecting?)
@web_blueprint.post("/auth/magic_links")
def magic_links_submit_email_handler():
    # replace with parsing from wtfforms
    email = request.form["email"]
    # I'm only going to build the happy path until comibining with the base branch and getting form libs up to date
    path = session.get("magic_links_forward_path")

    # at the moment not thinking about transactional gaurantees, will send the email in a follow up command
    magic_link = create_magic_link(email=email, path=path)
    get_notification_service().proto_send_magic_link(magic_link=magic_link)
    return redirect(
        url_for("proto_apply_blueprint.web_blueprint.magic_links_confirm_email_handler", external_id=magic_link.id)
    )
    # write a line in the magic links table in the postgres database
    # (forward path, email, something else)
    # send an email using that line from the table


# thinking ahead a bit - when the page is loaded by things crawling the link
# current method works by only fulfilling the link when a "Continue" button is clicked - crawlers wont click the button
# this method seems sensible but it would be nice if a bit of javascript could run, possibly even before the page is loaded which would foward you on
# assuming crawlers aren't running js - that would fall apart if any did
# it should also consider HEAD vs. GET requests which i believe most crawlers are supposed to be configured to make
@web_blueprint.get("/auth/return/magic_links/<token>")
def magic_links_return_handler(token):
    # currently this will break if a link is followed for a second time - I think it should be fine to continue if the session is already authenticated
    # can consider that from a security POV
    magic_link = get_magic_link(token=token)

    # update magic link to say its been used - I can probably include upserting an account for that email and marking the link as used together
    # in a transaction to make claiming it feel a bit more robust
    set_used(magic_link=magic_link)

    session.pop("magic_links_back_path")
    session.pop("magic_links_forward_path")

    # assuming this is cleared after a configured amount of time - would need to go in and fact check this
    session["is_authenticated"] = True
    return redirect(urljoin(Config.APPLICANT_FRONTEND_HOST, magic_link.path))
    # clear anything to do with magic links from the session

    # check the magic links line in the table for this token
    # upsert an account for this email
    # redirect to forward path
