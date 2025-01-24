from functools import wraps
from urllib.parse import urlparse

from flask import abort, current_app, g, redirect, request, session, url_for

from proto.common.data.services.accounts import get_account


def is_authenticated(func=None, /, as_platform_admin=False):
    def is_authenticated_decorator(innerfunc):
        @wraps(innerfunc)
        def wrapper(*args, **kwargs):
            if session.get("is_authenticated"):
                try:
                    g.account = get_account(session["magic_links_account_id"])
                except:  # noqa
                    session.clear()

            if not session.get("is_authenticated"):
                session["magic_links_forward_path"] = request.path

                if request.host == current_app.config["FUNDING_HOST"]:
                    session["magic_links_back_path"] = urlparse(request.referrer).path
                else:
                    session["magic_links_back_path"] = url_for(
                        "proto_apply.grant_blueprint.all_open_grants_handler", _external=False
                    )

                return redirect(url_for("proto_apply.web.magic_links_enter_email_handler"))

            if as_platform_admin and not g.account.is_platform_admin:
                abort(403)

            return innerfunc(*args, **kwargs)

        return wrapper

    if func:
        return is_authenticated_decorator(func)

    return is_authenticated_decorator


def maybe_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("is_authenticated"):
            try:
                g.account = get_account(session["magic_links_account_id"])
            except:  # noqa
                pass

        return func(*args, **kwargs)

    return wrapper
