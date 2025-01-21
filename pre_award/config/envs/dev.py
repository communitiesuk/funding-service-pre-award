"""Flask Dev Pipeline Environment Configuration."""

import logging
from os import getenv

from fsd_utils import CommonConfig, configclass

from pre_award.config.envs.aws import AwsConfig


@configclass
class DevConfig(AwsConfig):
    # Logging
    FSD_LOG_LEVEL = logging.INFO

    SESSION_COOKIE_DOMAIN = getenv("SESSION_COOKIE_DOMAIN")

    # assess dev config
    REDIS_INSTANCE_NAME = "funding-service-magic-links-dev"

    FEATURE_CONFIG = {
        "TAGGING": True,
        "ASSESSMENT_ASSIGNMENT": True,
        "UNCOMPETED_WORKFLOW": True,
        **CommonConfig.dev_feature_configuration,
    }
