from functools import wraps
from urllib.parse import urlparse

from flask import redirect, request, session, url_for

# from proto.common.auth.magic_links import MagicLinksAuthenticator


def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # this concept only works if the only thing the method can do is raise an exception - interrupting the flow
        # in order to have it as part of the middleware it would have to return the value passed on or handle it here
        # MagicLinksAuthenticator().authenticate()
        if not session.get("is_authenticated"):
            # I'm not a big fan of this - either the short code lives in the URL or in the session but it should be more formally set and parsed
            # if there isn't a short code I think for now this should just break - valid question about how it gets it when trying to access something like
            # the application task list page (load the application and set the short code for that?)
            # OK it shouldn't work based on passing in specific values - it should record the URL you're trying to access and take you to that if you get authenticated
            # don't try and be clever here

            # this route was accessed, requires authentication and should sent the user on to where they were trying to
            session["magic_links_forward_path"] = request.path

            # this would be cleared by magic links going through but I'm not sure about it - consider reconsider
            if urlparse(request.referrer).path.startswith("/grant"):
                session["magic_links_back_path"] = urlparse(request.referrer).path
            # the one edge case then is what if you load up the magic links page _without_ the URL you want to forward the user to, should it show a uniform error, boot your fund page back up
            return redirect(url_for("proto_apply_blueprint.web_blueprint.magic_links_enter_email_handler"))
        else:
            return func(*args, **kwargs)

    return wrapper
