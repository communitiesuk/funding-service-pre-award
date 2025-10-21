"""Flask Local Development Environment Configuration."""

import base64
import logging
from distutils.util import strtobool
from os import getenv

from fsd_utils import CommonConfig, configclass

from pre_award.config.envs.default import DefaultConfig
from pre_award.config.envs.default import DefaultConfig as Config


@configclass
class DevelopmentConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    FLASK_ENV = "development"

    DEBUG_TB_ENABLED = True
    DEBUG_TB_ROUTES_HOST = "*"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    TALISMAN_SETTINGS = Config.TALISMAN_SETTINGS

    # Flask-DebugToolbar scripts
    TALISMAN_SETTINGS["content_security_policy"]["script-src"].extend(
        ["'sha256-zWl5GfUhAzM8qz2mveQVnvu/VPnCS6QL7Niu6uLmoWU='"]
    )

    # Flask-DebugToolbar styles
    TALISMAN_SETTINGS["content_security_policy"]["style-src"].extend(
        [
            "'sha256-biLFinpqYMtWHmXfkA1BPeCY0/fNt46SAZ+BBk5YUog='",
            "'sha256-0EZqoz+oBhx7gF4nvY2bSqoGyy4zLjNF+SDQXGp/ZrY='",
            "'sha256-1NkfmhNaD94k7thbpTCKG0dKnMcxprj9kdSKzKR6K/k='",
            "'sha256-9KTa3VNMmypk8vbtqjwun0pXQtx5+yn5QoD/WlzV4qM='",
            "'sha256-fQY5fP3hSW2gDBpf5aHxpgfqCUocwOYh6zrfhhLsenY='",
            "'sha256-fHdQRrIUf6pjwHfX7CTFKabEZ1qmGXrWk9TRExXo9ZY='",
            "'sha256-Hw2dKmajmSN3MPIUjiOlZtZGa+LcQKY3gdW95UOmTAk='",
            "'sha256-7eLPjKEGogf4iYql5CFUp5LBUXCOKJkJ52Lrgz5DOg0='",
        ]
    )

    # Logging
    FSD_LOG_LEVEL = logging.INFO
    # ---------------
    # AWS Config
    # ---------------
    AWS_BUCKET_NAME = getenv("AWS_BUCKET_NAME")
    AWS_SECRET_ACCESS_KEY = AWS_SQS_SECRET_ACCESS_KEY = "test_secret_key"  # pragma: allowlist secret
    AWS_ACCESS_KEY_ID = AWS_SQS_ACCESS_KEY_ID = "test_access_key"  # pragma: allowlist secret
    AWS_SQS_REGION = AWS_REGION = "eu-west-2"

    # ---------------
    # S3 Config
    # ---------------

    USE_LOCAL_DATA = strtobool(getenv("USE_LOCAL_DATA", "True"))
    SESSION_COOKIE_SECURE = False
    AUTO_REDIRECT_LOGIN = True
    DISABLE_NOTIFICATION_SERVICE = False  # Toggle on if you have no notify api key.

    SESSION_COOKIE_DOMAIN = getenv("SESSION_COOKIE_DOMAIN")

    # RSA 256 KEYS
    if not hasattr(DefaultConfig, "RSA256_PUBLIC_KEY"):
        _test_public_key_path = DefaultConfig.FLASK_ROOT + "/tests/pre_award/keys/rsa256/public.pem"
        with open(_test_public_key_path, mode="rb") as public_key_file:
            RSA256_PUBLIC_KEY = public_key_file.read()
    if not hasattr(DefaultConfig, "RSA256_PRIVATE_KEY"):
        _test_private_key_path = DefaultConfig.FLASK_ROOT + "/tests/pre_award/keys/rsa256/private.pem"
        with open(_test_private_key_path, mode="rb") as private_key_file:
            RSA256_PRIVATE_KEY = private_key_file.read()

    LRU_CACHE_TIME = 1  # in seconds
    FSD_USER_TOKEN_COOKIE_NAME = "fsd_user_token"
    AUTHENTICATOR_HOST = getenv("AUTHENTICATOR_HOST", "https://authenticator")
    SSO_LOGIN_URL = AUTHENTICATOR_HOST + "/sso/login"
    SSO_LOGOUT_URL = AUTHENTICATOR_HOST + "/sso/logout"

    DEBUG_USER_ON = True  # Set to True to use DEBUG user

    DEBUG_USER_ROLE = "LEAD_ASSESSOR"
    DEBUG_USER = {
        "full_name": "Development User",
        "email": "dev@example.com",
        "roles": [
            "GBRF_ASSESSOR",
            "GBRF_LEAD_ASSESSOR",
            "GBRF_COMMENTER",
            "LPDF_ASSESSOR",
            "LPDF_LEAD_ASSESSOR",
            "LPDF_COMMENTER",
            "COF_LEAD_ASSESSOR",
            "COF_ASSESSOR",
            "COF_COMMENTER",
            "COF_ENGLAND",
            "COF_SCOTLAND",
            "COF_WALES",
            "COF_NORTHERNIRELAND",
            "NSTF_LEAD_ASSESSOR",
            "NSTF_ASSESSOR",
            "NSTF_COMMENTER",
            "CYP_LEAD_ASSESSOR",
            "CYP_ASSESSOR",
            "CYP_COMMENTER",
            "DPIF_LEAD_ASSESSOR",
            "DPIF_ASSESSOR",
            "DPIF_COMMENTER",
            "COF-EOI_LEAD_ASSESSOR",
            "COF-EOI_ASSESSOR",
            "COF-EOI_COMMENTER",
            "HSRA_LEAD_ASSESSOR",
            "HSRA_ASSESSOR",
            "HSRA_COMMENTER",
            "CTDF_LEAD_ASSESSOR",
            "CTDF_ASSESSOR",
            "CF1_LEAD_ASSESSOR",
            "CF1_ASSESSOR",
            "UF1_LEAD_ASSESSOR",
            "UF1_ASSESSOR",
            "FFW_LEAD_ASSESSOR",
            "FFW_ASSESSOR",
            "CFA_LEAD_ASSESSOR",
            "CFA_ASSESSOR",
            "CFA_COMMENTER",
            "CHAM_LEAD_ASSESSOR",
            "CHAM_ASSESSOR",
            "CHAM_COMMENTER",
            "PFN_LEAD_ASSESSOR",
            "PFN_ASSESSOR",
            "PFN_COMMENTER",
            "FSD_ADMIN",
            "LAHF_LEAD_ASSESSOR",
            "LAHF_ASSESSOR",
            "LAHF_COMMENTER",
            "SHIF_LEAD_ASSESSOR",
            "SHIF_ASSESSOR",
            "SHIF_COMMENTER",
        ],
        "highest_role_map": {
            "FFW": DEBUG_USER_ROLE,
            "GBRF": DEBUG_USER_ROLE,
            "LPDF": DEBUG_USER_ROLE,
            "CTDF": DEBUG_USER_ROLE,
            "CF1": DEBUG_USER_ROLE,
            "UF1": DEBUG_USER_ROLE,
            "COF": DEBUG_USER_ROLE,
            "NSTF": DEBUG_USER_ROLE,
            "CYP": DEBUG_USER_ROLE,
            "DPIF": DEBUG_USER_ROLE,
            "COF-EOI": DEBUG_USER_ROLE,
            "HSRA": DEBUG_USER_ROLE,
            "CFA": DEBUG_USER_ROLE,
            "CHAM": DEBUG_USER_ROLE,
            "PFN": DEBUG_USER_ROLE,
            "LAHF": DEBUG_USER_ROLE,
            "SHIF": DEBUG_USER_ROLE,
        },
    }
    DEBUG_USER_ACCOUNT_ID = "00000000-0000-0000-0000-000000000000"

    RSA256_PUBLIC_KEY_BASE64 = getenv("RSA256_PUBLIC_KEY_BASE64")
    if RSA256_PUBLIC_KEY_BASE64:
        RSA256_PUBLIC_KEY = base64.b64decode(RSA256_PUBLIC_KEY_BASE64).decode()

    ASSETS_AUTO_BUILD = True

    FEATURE_CONFIG = {
        "TAGGING": True,
        "ASSESSMENT_ASSIGNMENT": True,
        "UNCOMPETED_WORKFLOW": True,
        **CommonConfig.dev_feature_configuration,
    }
