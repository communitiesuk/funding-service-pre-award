import datetime
from os import getenv
from urllib.parse import urlencode, urljoin

import psycopg2
from flask import Flask, current_app, g, make_response, render_template, request, url_for
from flask.json.provider import DefaultJSONProvider
from flask_assets import Environment
from flask_babel import Babel, gettext, pgettext
from flask_compress import Compress
from flipper import FeatureFlagClient, MemoryFeatureFlagStore

from common.utils.filters import datetime_format_respect_lang, to_bst

try:
    from flask_debugtoolbar import DebugToolbarExtension

    toolbar = DebugToolbarExtension()
except ImportError:
    toolbar = None
from flask_redis import FlaskRedis
from flask_session import Session
from flask_talisman import Talisman
from flask_wtf import CSRFProtect
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import DbChecker, FlaskRunningChecker, RedisChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging
from fsd_utils.toggles.toggles import create_toggles_client, initialise_toggles_redis_store, load_toggles
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader
from sqlalchemy_utils import Ltree

import static_assets
from pre_award.account_store.core.account import account_core_bp
from pre_award.application_store.api.routes.application.routes import application_store_bp
from pre_award.application_store.db.exceptions.application import ApplicationError
from pre_award.apply.filters import (
    custom_format_datetime,
    date_format_short_month,
    datetime_format,
    datetime_format_full_month,
    datetime_format_short_month,
    kebab_case_to_human,
    snake_case_to_human,
    status_translation,
    string_to_datetime,
)
from pre_award.apply.helpers import find_fund_and_round_in_request, find_fund_in_request, find_round_in_request
from pre_award.assess.shared.filters import (
    add_to_dict,
    all_caps_to_human,
    assess_datetime_format,
    ast_literal_eval,
    datetime_format_24hr,
    format_address,
    format_project_ref,
    remove_dashes_underscores_capitalize,
    remove_dashes_underscores_capitalize_keep_uppercase,
    slash_separated_day_month_year,
    utc_to_bst,
)
from pre_award.assessment_store.api.routes import assessment_store_bp
from pre_award.common.locale_selector.get_lang import get_lang
from pre_award.common.locale_selector.set_lang import LanguageSelector
from pre_award.config import Config
from pre_award.form_store.api.routes import form_store_bp
from pre_award.fund_store.api.routes import fund_store_bp
from services.notify import NotificationService


# TODO: Remove this when we have stripped out the HTTP/JSON interface between "pre-award-stores" and
#       "pre-award-frontend" We need this in the interim because the way that connexion serializes datetimes is
#       different from how flask serializes datetimes by default, and pre-award-frontend (specifically around survey
#       feedback) is expecting the connexion format with "Z" suffixes and using `isoformat` rather than RFC 822.
def _connexion_compatible_datetime_serializer(o):
    if isinstance(o, datetime.datetime):
        if o.tzinfo:
            # eg: '2015-09-25T23:14:42.588601+00:00'
            return o.isoformat("T")
        else:
            # No timezone present - assume UTC.
            # eg: '2015-09-25T23:14:42.588601Z'
            return o.isoformat("T") + "Z"

    if isinstance(o, datetime.date):
        return o.isoformat()

    from flask.json.provider import _default

    return _default(o)


# TODO: See above
class ConnexionCompatibleJSONProvider(DefaultJSONProvider):
    default = staticmethod(_connexion_compatible_datetime_serializer)


# TODO: See above
class ConnexionCompatibleJSONFlask(Flask):
    json_provider_class = ConnexionCompatibleJSONProvider


redis_mlinks = FlaskRedis(config_prefix="REDIS_MLINKS")


def create_app() -> Flask:  # noqa: C901
    init_sentry()

    # TODO: See above
    flask_app = ConnexionCompatibleJSONFlask(
        __name__,
        static_url_path="/assets",
        static_folder="static",
        host_matching=True,
        static_host="<host_from_current_request>",
    )

    flask_app.config.from_object("pre_award.config.Config")

    toggle_client = None
    if getenv("FLASK_ENV") != "unit_test":
        initialise_toggles_redis_store(flask_app)
        toggle_client = create_toggles_client()
        load_toggles(Config.FEATURE_CONFIG, toggle_client)
    else:
        toggle_client = FeatureFlagClient(MemoryFeatureFlagStore())
        load_toggles(Config.FEATURE_CONFIG, toggle_client)

    Babel(flask_app, locale_selector=get_lang)
    LanguageSelector(flask_app)

    # Bundle and compile assets
    assets = Environment()
    assets.init_app(flask_app)
    static_assets.init_assets(flask_app, auto_build=Config.ASSETS_AUTO_BUILD)

    flask_app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("pre_award.apply"),
            PackageLoader("pre_award.assess"),
            # move everything into one templates folder for assess rather than nesting in blueprints
            PackageLoader("pre_award.assess.shared"),
            PackageLoader("pre_award.assess.assessments"),
            PackageLoader("pre_award.assess.flagging"),
            PackageLoader("pre_award.assess.tagging"),
            PackageLoader("pre_award.assess.scoring"),
            PackageLoader("pre_award.authenticator.frontend"),
            PackageLoader("common"),
            PackageLoader("apply"),
            PrefixLoader({"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}),
        ]
    )

    NotificationService().init_app(flask_app)

    flask_app.jinja_env.trim_blocks = True
    flask_app.jinja_env.lstrip_blocks = True
    flask_app.jinja_env.add_extension("jinja2.ext.i18n")
    flask_app.jinja_env.add_extension("jinja2.ext.do")
    flask_app.jinja_env.globals["get_lang"] = get_lang
    flask_app.jinja_env.globals["pgettext"] = pgettext

    flask_app.jinja_env.filters["datetime_format_short_month"] = datetime_format_short_month
    flask_app.jinja_env.filters["datetime_format_full_month"] = datetime_format_full_month
    flask_app.jinja_env.filters["string_to_datetime"] = string_to_datetime
    flask_app.jinja_env.filters["custom_format_datetime"] = custom_format_datetime
    flask_app.jinja_env.filters["date_format_short_month"] = date_format_short_month
    flask_app.jinja_env.filters["datetime_format"] = datetime_format
    flask_app.jinja_env.filters["snake_case_to_human"] = snake_case_to_human
    flask_app.jinja_env.filters["kebab_case_to_human"] = kebab_case_to_human
    flask_app.jinja_env.filters["status_translation"] = status_translation

    # Assess filters
    flask_app.jinja_env.filters["ast_literal_eval"] = ast_literal_eval
    flask_app.jinja_env.filters["assess_datetime_format"] = assess_datetime_format
    flask_app.jinja_env.filters["utc_to_bst"] = utc_to_bst
    flask_app.jinja_env.filters["add_to_dict"] = add_to_dict
    flask_app.jinja_env.filters["slash_separated_day_month_year"] = slash_separated_day_month_year
    flask_app.jinja_env.filters["all_caps_to_human"] = all_caps_to_human
    flask_app.jinja_env.filters["datetime_format_24hr"] = datetime_format_24hr
    flask_app.jinja_env.filters["format_project_ref"] = format_project_ref
    flask_app.jinja_env.filters["remove_dashes_underscores_capitalize"] = remove_dashes_underscores_capitalize
    flask_app.jinja_env.filters["remove_dashes_underscores_capitalize_keep_uppercase"] = (
        remove_dashes_underscores_capitalize_keep_uppercase
    )
    flask_app.jinja_env.filters["format_address"] = format_address

    # new monolith filters
    flask_app.jinja_env.filters["datetime_format_respect_lang"] = datetime_format_respect_lang
    flask_app.jinja_env.filters["to_bst"] = to_bst

    # This section is needed for url_for("foo", _external=True) to
    # automatically generate http scheme when this sample is
    # running on localhost, and to generate https scheme when it is
    # deployed behind reversed proxy.
    # See also #proxy_setups section at
    # flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone
    from werkzeug.middleware.proxy_fix import ProxyFix

    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_proto=1, x_host=1)

    csrf = CSRFProtect()
    csrf.init_app(flask_app)

    Compress(flask_app)

    if toolbar and flask_app.config["FLASK_ENV"] == "development":
        toolbar.init_app(flask_app)

    # These are required to associated errorhandlers and before/after request decorators with their blueprints
    import pre_award.apply.default.error_routes  # noqa
    import pre_award.assess.blueprint_middleware  # noqa
    from apply.routes import apply_bp
    from pre_award.apply.default.account_routes import account_bp
    from pre_award.apply.default.application_routes import application_bp
    from pre_award.apply.default.content_routes import content_bp
    from pre_award.apply.default.eligibility_routes import eligibility_bp
    from pre_award.apply.default.routes import default_bp
    from pre_award.assess.assessments.routes import assessment_bp
    from pre_award.assess.flagging.routes import flagging_bp
    from pre_award.assess.scoring.routes import scoring_bp
    from pre_award.assess.shared.routes import shared_bp
    from pre_award.assess.tagging.routes import tagging_bp
    from pre_award.authenticator.api.magic_links.routes import api_magic_link_bp
    from pre_award.authenticator.api.session.auth_session import api_sessions_bp
    from pre_award.authenticator.api.sso.routes import api_sso_bp
    from pre_award.authenticator.frontend.default.routes import default_bp as authenticator_default_bp
    from pre_award.authenticator.frontend.magic_links.routes import magic_links_bp
    from pre_award.authenticator.frontend.sso.routes import sso_bp
    from pre_award.authenticator.frontend.user.routes import user_bp
    from pre_award.common.error_routes import internal_server_error, not_found
    from pre_award.utils.routes import utils_bp

    flask_app.register_error_handler(404, not_found)
    flask_app.register_error_handler(500, internal_server_error)
    flask_app.register_error_handler(ApplicationError, internal_server_error)

    flask_app.register_blueprint(default_bp, host=flask_app.config["APPLY_HOST"])
    flask_app.register_blueprint(application_bp, host=flask_app.config["APPLY_HOST"])
    flask_app.register_blueprint(content_bp, host=flask_app.config["APPLY_HOST"])
    flask_app.register_blueprint(eligibility_bp, host=flask_app.config["APPLY_HOST"])
    flask_app.register_blueprint(account_bp, host=flask_app.config["APPLY_HOST"])

    flask_app.register_blueprint(shared_bp, host=flask_app.config["ASSESS_HOST"])
    flask_app.register_blueprint(tagging_bp, host=flask_app.config["ASSESS_HOST"])
    flask_app.register_blueprint(flagging_bp, host=flask_app.config["ASSESS_HOST"])
    flask_app.register_blueprint(scoring_bp, host=flask_app.config["ASSESS_HOST"])
    flask_app.register_blueprint(assessment_bp, host=flask_app.config["ASSESS_HOST"])

    flask_app.register_blueprint(authenticator_default_bp, host=flask_app.config["AUTH_HOST"])
    flask_app.register_blueprint(magic_links_bp, host=flask_app.config["AUTH_HOST"])
    flask_app.register_blueprint(sso_bp, host=flask_app.config["AUTH_HOST"])
    flask_app.register_blueprint(user_bp, host=flask_app.config["AUTH_HOST"])
    flask_app.register_blueprint(api_magic_link_bp, host=flask_app.config["AUTH_HOST"])
    flask_app.register_blueprint(api_sso_bp, host=flask_app.config["AUTH_HOST"])
    flask_app.register_blueprint(api_sessions_bp, host=flask_app.config["AUTH_HOST"])

    flask_app.register_blueprint(apply_bp, host=flask_app.config["APPLY_HOST"])

    # FIXME: we should be enforcing CSRF on requests to sign out via authenticator, but because this is a cross-domain
    #        request, flask_wtf rejects the request because it's not the same origin. See `project` method in
    #        `flask_wtf.csrf`. Note: this preserves existing behaviour, because Authenticator was not enforcing CSRF
    #        at all (it never initialised CSRFProtect).
    csrf.exempt(api_sessions_bp)
    csrf.exempt(api_sso_bp)

    flask_app.register_blueprint(account_core_bp, url_prefix="/account", host=Config.API_HOST)
    flask_app.register_blueprint(fund_store_bp, url_prefix="/fund", host=Config.API_HOST)
    flask_app.register_blueprint(application_store_bp, url_prefix="/application", host=Config.API_HOST)
    flask_app.register_blueprint(assessment_store_bp, url_prefix="/assessment", host=Config.API_HOST)
    flask_app.register_blueprint(form_store_bp, url_prefix="/forms", host=Config.API_HOST)
    flask_app.register_blueprint(utils_bp, url_prefix="/utils", host=Config.APPLY_HOST)
    csrf.exempt(account_core_bp)
    csrf.exempt(fund_store_bp)
    csrf.exempt(application_store_bp)
    csrf.exempt(assessment_store_bp)
    csrf.exempt(form_store_bp)
    csrf.exempt(utils_bp)  # NOSONAR: S4502 - API blueprint, consistent with other exemptions
    for bp, _ in assessment_store_bp._blueprints:
        csrf.exempt(bp)

    # Initialise Sessions
    session = Session()
    session.init_app(flask_app)

    # Initialise Redis Magic Links Store
    redis_mlinks.init_app(flask_app)

    # Configure application security with Talisman
    Talisman(flask_app, **Config.TALISMAN_SETTINGS)

    from pre_award.db import db, migrate

    # Bind SQLAlchemy ORM to Flask app
    db.init_app(flask_app)

    # Bind Flask-Migrate db utilities to Flask app
    migrate.init_app(flask_app, db, directory="pre_award/db/migrations", render_as_batch=True)

    # Enable mapping of ltree datatype for sections
    psycopg2.extensions.register_adapter(Ltree, lambda ltree: psycopg2.extensions.QuotedString(str(ltree)))

    # Initialise logging
    logging.init_app(flask_app)

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())
    health.add_check(DbChecker(db))
    health.add_check(RedisChecker(redis_mlinks))

    @flask_app.url_defaults
    def inject_host_from_current_request(endpoint, values):
        if flask_app.url_map.is_endpoint_expecting(endpoint, "host_from_current_request"):
            values["host_from_current_request"] = request.host

    @flask_app.url_value_preprocessor
    def pop_host_from_current_request(endpoint, values):
        if values is not None:
            values.pop("host_from_current_request", None)

    @flask_app.context_processor
    def inject_global_constants():
        if request.host == current_app.config["APPLY_HOST"]:
            return dict(
                stage="beta",
                service_meta_author="Department for Levelling up Housing and Communities",
                toggle_dict={feature.name: feature.is_enabled() for feature in toggle_client.list()}
                if toggle_client
                else {},
                support_desk_apply=Config.SUPPORT_DESK_APPLY,
            )
        elif request.host == current_app.config["ASSESS_HOST"]:
            return dict(
                stage="beta",
                service_title="Assessment Hub – GOV.UK",
                service_meta_description="Assessment Hub",
                service_meta_keywords="Assessment Hub",
                service_meta_author="DLUHC",
                sso_logout_url=flask_app.config.get("SSO_LOGOUT_URL"),
                g=g,
                toggle_dict=(
                    {feature.name: feature.is_enabled() for feature in toggle_client.list()} if toggle_client else {}
                ),
                support_desk_assess=Config.SUPPORT_DESK_ASSESS,
            )
        elif request.host == current_app.config["AUTH_HOST"]:
            query_params = urlencode({"fund": request.args.get("fund", ""), "round": request.args.get("round", "")})
            return dict(
                stage="beta",
                service_meta_author="Ministry of Housing, Communities and Local Government",
                accessibility_statement_url=urljoin(Config.APPLICANT_FRONTEND_HOST, "/accessibility_statement"),  # noqa
                cookie_policy_url=urljoin(Config.APPLICANT_FRONTEND_HOST, "/cookie_policy"),
                contact_us_url=urljoin(Config.APPLICANT_FRONTEND_HOST, f"/contact_us?{query_params}"),
                privacy_url=urljoin(Config.APPLICANT_FRONTEND_HOST, f"/privacy?{query_params}"),
                feedback_url=urljoin(Config.APPLICANT_FRONTEND_HOST, f"/feedback?{query_params}"),
            )

        return {}

    def get_fund_and_round_in_request():
        fd, rnd = None, None
        if request.view_args or request.args or request.form:
            try:
                fd = find_fund_in_request()
                rnd = find_round_in_request()
            except Exception as e:  # noqa
                current_app.logger.warning(
                    (
                        "Exception: %(e)s, occured when trying to reach url: %(url)s, "
                        "with view_args: %(view_args)s, and args: %(args)s"
                    ),
                    dict(e=e, url=request.url, view_args=request.view_args, args=request.args),
                )
        return fd, rnd

    def _get_service_title():
        fund, rnd = get_fund_and_round_in_request()
        # TODO Assuming that this is the only round that is not going to need the hardcoded text
        # "Apply for ...". otherwise we need to find a better way to handle this

        # 1) If we got a fund AND it’s that special round (PFN-RP), show just the fund title
        if fund and rnd and rnd.id == "9217792e-d8c2-45c8-8170-eed4a8946184":
            return fund.title

        # 2) If we got a fund (any other round or no round at all), show “Apply for …”
        if fund:
            return f"{gettext('Apply for')} {fund.title}"
        elif (
            request.args
            and (return_app := request.args.get("return_app"))
            and request.host == current_app.config["AUTH_HOST"]
        ):
            return Config.SAFE_RETURN_APPS[return_app].service_title

        return gettext("Access Funding")

    def _privacy_for_round(round_obj):
        """Return the privacy_notice URL string for a round object, or None."""
        if not round_obj:
            return None
        privacy_val = getattr(round_obj, "privacy_notice", None)
        if isinstance(privacy_val, str) and privacy_val.strip():
            return privacy_val.strip()
        return None

    @flask_app.context_processor
    def utility_processor():
        return {"get_service_title": _get_service_title}

    @flask_app.context_processor
    def get_page_title():
        def _get_page_title():
            # Use the get_service_title function already in the context
            get_service_title = flask_app.jinja_env.globals.get("get_service_title")
            # If not found in globals, fallback to calling the utility directly
            if not get_service_title:
                get_service_title = _get_service_title
            base_title = get_service_title()
            return f"{base_title} - GOV.UK"

        return {"get_page_title": _get_page_title}

    @flask_app.context_processor
    def inject_content_urls():
        privacy_url = ""
        try:
            fund, round = find_fund_and_round_in_request()
            if fund and round:
                privacy_url = _privacy_for_round(round) or ""
                return dict(
                    accessibility_statement_url=url_for(
                        "content_routes.accessibility_statement",
                        fund=fund.short_name,
                        round=round.short_name,
                    ),
                    contact_us_url=url_for(
                        "apply_routes.contact_us",
                        fund_short_name=fund.short_name,
                        round=round.short_name,
                    ),
                    privacy_url=privacy_url,
                    feedback_url=url_for(
                        "content_routes.feedback",
                        fund=fund.short_name,
                        round=round.short_name,
                    ),
                )
        except Exception as e:  # noqa
            current_app.logger.warning(
                (
                    "Exception: %(e)s, occured when trying to reach url: %(url)s, "
                    "with view_args: %(view_args)s, and args: %(args)s"
                ),
                dict(e=e, url=request.url, view_args=request.view_args, args=request.args),
            )
        return dict(
            accessibility_statement_url=url_for("content_routes.accessibility_statement"),
            contact_us_url=url_for("apply_routes.contact_us"),
            privacy_url=privacy_url,
            feedback_url=url_for("content_routes.feedback"),
        )

    @flask_app.context_processor
    def is_uncompeted_flow():
        def _is_uncompeted_flow(fund=None):
            fund = fund if fund else find_fund_in_request()
            toggle_dict = (
                {feature.name: feature.is_enabled() for feature in toggle_client.list()} if toggle_client else {}
            )
            return (
                toggle_dict.get("UNCOMPETED_WORKFLOW")
                and fund.funding_type == "UNCOMPETED"
                and fund.short_name != "DPIF"
            )

        return dict(is_uncompeted_flow=_is_uncompeted_flow)

    @flask_app.context_processor
    def is_pfn_fund_round():
        fd, rnd = get_fund_and_round_in_request()
        is_pfn = getattr(fd, "short_name", None) == "PFN" and getattr(rnd, "short_name", None) == "RP"
        return {"is_pfn_fund_round": is_pfn}

    @flask_app.after_request
    def after_request(response):
        if request.host == current_app.config["API_HOST"]:
            return response

        if request.path.endswith("js") or request.path.endswith("css"):
            response.headers["Cache-Control"] = "public, max-age=3600"

        elif "Cache-Control" not in response.headers:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

        return response

    @flask_app.before_request
    def filter_all_requests():
        source_app_host_match = {
            current_app.config["APPLY_HOST"]: "apply_frontend",
            current_app.config["ASSESS_HOST"]: "assess_frontend",
            current_app.config["AUTH_HOST"]: "authenticator_frontend",
            current_app.config["API_HOST"]: request.blueprint,
        }
        request.get_extra_log_context = lambda: {"source": source_app_host_match.get(request.host)}
        if request.host == current_app.config["API_HOST"]:
            return

        if flask_app.config.get("MAINTENANCE_MODE") and not (
            request.path.endswith("js") or request.path.endswith("css") or request.path.endswith("/healthcheck")
        ):
            current_app.logger.warning(
                "Application is in the Maintenance mode reach url: %(url)s", dict(url=request.url)
            )

            if request.host == current_app.config["ASSESS_HOST"]:
                maintenance_template = "assess/maintenance.html"
            else:
                maintenance_template = "apply/maintenance.html"

            return (
                render_template(
                    maintenance_template,
                    maintenance_end_time=flask_app.config.get("MAINTENANCE_END_TIME"),
                ),
                503,
            )

        if request.path == "/favicon.ico":
            return make_response("404"), 404

    return flask_app
