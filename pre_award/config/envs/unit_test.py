"""Flask Local Development Environment Configuration."""

import base64
import logging
from distutils.util import strtobool
from os import getenv

from fsd_utils import CommonConfig, configclass

from pre_award.config.envs.default import DefaultConfig
from pre_award.config.envs.default import DefaultConfig as Config


@configclass
class UnitTestConfig(Config):
    #  Application Config
    SECRET_KEY = "test"  # pragma: allowlist secret

    # APIs
    APPLICATION_STORE_API_HOST = CommonConfig.TEST_APPLICATION_STORE_API_HOST
    ACCOUNT_STORE_API_HOST = CommonConfig.TEST_ACCOUNT_STORE_API_HOST
    FUND_STORE_API_HOST = Config.TEST_FUND_STORE_API_HOST

    SQLALCHEMY_ECHO = False

    # Security
    FORCE_HTTPS = False

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    # Database
    WARN_IF_QUERIES_OVER_MS = 5

    # ---------------
    # AWS Config
    # ---------------
    AWS_SECRET_ACCESS_KEY = AWS_SQS_SECRET_ACCESS_KEY = "test_secret_key"  # pragma: allowlist secret
    AWS_ACCESS_KEY_ID = AWS_SQS_ACCESS_KEY_ID = "test_access_key"  # pragma: allowlist secret
    USE_LOCAL_DATA = True
    AWS_SQS_REGION = AWS_REGION = "eu-west-2"

    # ---------------
    # S3 Config
    # ---------------

    # ----------------------
    # FRONTENDS CONFIG
    # ----------------------
    DefaultConfig.TALISMAN_SETTINGS["force_https"] = False
    USE_LOCAL_DATA = "True"
    SESSION_COOKIE_SECURE = False
    FUND_ID_COF = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
    COOKIE_DOMAIN = ".levellingup.gov.localhost"

    # RSA 256 KEYS
    RSA256_PUBLIC_KEY_BASE64 = getenv("RSA256_PUBLIC_KEY_BASE64")
    if RSA256_PUBLIC_KEY_BASE64:
        RSA256_PUBLIC_KEY = base64.b64decode(RSA256_PUBLIC_KEY_BASE64).decode()
    if not hasattr(DefaultConfig, "RSA256_PUBLIC_KEY"):
        _test_public_key_path = DefaultConfig.FLASK_ROOT + "/tests/pre_award/keys/rsa256/public.pem"
        with open(_test_public_key_path, mode="rb") as public_key_file:
            RSA256_PUBLIC_KEY = public_key_file.read()

    RSA256_PRIVATE_KEY_BASE64 = getenv("RSA256_PRIVATE_KEY_BASE64")
    if RSA256_PRIVATE_KEY_BASE64:
        RSA256_PRIVATE_KEY = base64.b64decode(RSA256_PRIVATE_KEY_BASE64).decode()
    if not hasattr(DefaultConfig, "RSA256_PRIVATE_KEY"):
        _test_private_key_path = DefaultConfig.FLASK_ROOT + "/tests/pre_award/keys/rsa256/private.pem"
        with open(_test_private_key_path, mode="rb") as private_key_file:
            RSA256_PRIVATE_KEY = private_key_file.read()

    WTF_CSRF_ENABLED = False

    # Redis Configuration for Feature Flags
    TOGGLES_URL = "redis://localhost:6379/0"

    FSD_USER_TOKEN_COOKIE_NAME = "fsd_user_token"
    FEATURE_CONFIG = {
        "TAGGING": True,
        "ASSESSMENT_ASSIGNMENT": True,
        "UNCOMPETED_WORKFLOW": True,
        **CommonConfig.dev_feature_configuration,
    }

    SHOW_ALL_ROUNDS = True

    # Azure Active Directory Config
    AZURE_AD_CLIENT_ID = "abc"
    AZURE_AD_CLIENT_SECRET = "123"
    AZURE_AD_TENANT_ID = "organizations"
    AZURE_AD_AUTHORITY = (
        # consumers|organizations|<tenant_id>
        # - signifies the Azure AD tenant endpoint
        "https://login.microsoftonline.com/" + AZURE_AD_TENANT_ID
    )

    SESSION_TYPE = (
        # Specifies how the token cache should be stored
        # in server-side session
        # "filesystem"
        "redis"
    )
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    ALLOW_ASSESSMENT_LOGIN_VIA_MAGIC_LINK = strtobool(getenv("ALLOW_ASSESSMENT_LOGIN_VIA_MAGIC_LINK", "False"))
    WTF_CSRF_ENABLED = False

    # ---------------
    # S3 Config
    # ---------------

    GOV_NOTIFY_API_KEY = "test-00000000-0000-0000-0000-000000000000-00000000-0000-0000-0000-000000000000"
