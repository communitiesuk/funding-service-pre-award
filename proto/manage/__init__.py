from common.blueprints import Blueprint
from config import Config
from proto.manage.assess import assess_blueprint
from proto.manage.platform import platform_blueprint
from proto.manage.web import web_blueprint

manage_blueprint = Blueprint("proto_manage", __name__)
manage_blueprint.register_blueprint(web_blueprint, host=Config.MANAGE_HOST)
manage_blueprint.register_blueprint(platform_blueprint, host=Config.MANAGE_HOST)
manage_blueprint.register_blueprint(assess_blueprint, host=Config.MANAGE_HOST)
