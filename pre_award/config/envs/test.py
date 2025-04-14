"""Flask Test Environment Configuration."""

import base64
from os import environ

from fsd_utils import CommonConfig, configclass

from pre_award.config.envs.aws import AwsConfig


@configclass
class TestConfig(AwsConfig):
    RSA256_PUBLIC_KEY = base64.b64decode(environ.get("RSA256_PUBLIC_KEY_BASE64")).decode()

    # LRU cache settings
    LRU_CACHE_TIME = 300  # in seconds

    FEATURE_CONFIG = {
        "TAGGING": True,
        "ASSESSMENT_ASSIGNMENT": True,
        "UNCOMPETED_WORKFLOW": True,
        **CommonConfig.dev_feature_configuration,
    }
