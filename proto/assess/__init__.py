from common.blueprints import Blueprint
from config import Config
from proto.assess.application_routes import assessment_blueprint

proto_assess_blueprint = Blueprint("proto_assess_blueprint", __name__)
proto_assess_blueprint.register_blueprint(assessment_blueprint, host=Config.ASSESS_HOST)
