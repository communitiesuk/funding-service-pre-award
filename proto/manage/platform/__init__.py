from common.blueprints import Blueprint
from config import Config
from proto.manage.platform.application_rounds import rounds_blueprint
from proto.manage.platform.grants import grants_blueprint
from proto.manage.platform.recipients import recipients_blueprint
from proto.manage.platform.reporting_rounds import reporting_rounds_blueprint
from proto.manage.platform.templates import templates_blueprint

platform_blueprint = Blueprint("platform", __name__)


# FIXME not good registering here
platform_blueprint.register_blueprint(grants_blueprint, host=Config.FUNDING_HOST)
platform_blueprint.register_blueprint(rounds_blueprint, host=Config.FUNDING_HOST)
platform_blueprint.register_blueprint(reporting_rounds_blueprint, host=Config.FUNDING_HOST)
platform_blueprint.register_blueprint(recipients_blueprint, host=Config.FUNDING_HOST)
platform_blueprint.register_blueprint(templates_blueprint, host=Config.FUNDING_HOST)
