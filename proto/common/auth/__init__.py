from functools import wraps
from urllib.parse import urlparse

from flask import g, redirect, request, session, url_for

from proto.common.data.services.accounts import get_account


def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("is_authenticated"):
            try:
                g.account = get_account(session["magic_links_account_id"])
            except:  # noqa
                g.account = None
                session.clear()

        if not session.get("is_authenticated"):
            session["magic_links_forward_path"] = request.path
            session["magic_links_back_path"] = urlparse(request.referrer).path
            return redirect(url_for("proto_apply.web.magic_links_enter_email_handler"))
        else:
            return func(*args, **kwargs)

    return wrapper


def maybe_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("is_authenticated"):
            try:
                g.account = get_account(session["magic_links_account_id"])
            except:  # noqa
                g.account = None

        return func(*args, **kwargs)

    return wrapper
