from flask import render_template, request, session

from common.blueprints import Blueprint

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


# am I OK with this POST rendering the confirmation page or do I want it to redirect to a page
# that can be refreshed without actions that will render the page (based on the token its expecting?)
@web_blueprint.post("/auth/magic_links")
def magic_links_submit_email_handler():
    # replace with parsing from wtfforms
    email = request.form["email"]
    # I'm only going to build the happy path until comibining with the base branch and getting form libs up to date
    path = session.get("magic_links_forward_path")

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
    # redirect or break

    # check the magic links line in the table for this token
    # upsert an account for this email
    # redirect to forward path
    return True
