import os

FLASK_ENV = os.getenv("FLASK_ENV")

if not FLASK_ENV:
    raise KeyError("FLASK_ENV does not exist in environ")

match FLASK_ENV:
    case "unit_test":
        from pre_award.config.envs.unit_test import UnitTestConfig as Config
    case "development":
        from pre_award.config.envs.development import DevelopmentConfig as Config
    case "dev":
        from pre_award.config.envs.dev import DevConfig as Config
    case "test" | "uat":
        from pre_award.config.envs.test import TestConfig as Config
    case "production":
        from pre_award.config.envs.production import ProductionConfig as Config
    case _:
        from pre_award.config.envs.default import DefaultConfig as Config

try:
    Config.pretty_print()
except AttributeError:
    print({"msg": "Config doesn't have pretty_print function."})

__all__ = [Config]
