from common.blueprints import Blueprint
from config import Config
from proto.assess.applications import applications_blueprint
from proto.assess.web import web_blueprint

assess_blueprint = Blueprint("proto_assess", __name__)
assess_blueprint.register_blueprint(web_blueprint, host=Config.ASSESS_HOST)
assess_blueprint.register_blueprint(applications_blueprint, host=Config.ASSESS_HOST)
