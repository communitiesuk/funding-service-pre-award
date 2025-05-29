# flake8: noqa
from os import environ

FLASK_ENV = environ.get("FLASK_ENV")

match FLASK_ENV:
    case "development":
        from pre_award.config.envs.development import DevelopmentConfig as Config
    case "dev":
        from pre_award.config.envs.dev import DevConfig as Config
    case "test":
        from pre_award.config.envs.test import TestConfig as Config
    case "unit_test":
        from pre_award.config.envs.unit_test import UnitTestConfig as Config
    case "production":
        from pre_award.config.envs.production import ProductionConfig as Config
    case _:
        from pre_award.config.envs.default import DefaultConfig as Config

try:
    Config.pretty_print()
except AttributeError:
    print({"msg": "Config doesn't have pretty_print function."})

__all__ = [Config]
