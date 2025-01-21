from pre_award.common.blueprints import Blueprint
from pre_award.config import Config

from .assessment_routes import assessment_assessment_bp
from .comment_routes import assessment_comment_bp
from .flag_routes import assessment_flag_bp
from .progress_routes import assessment_progress_bp
from .qa_complete_routes import assessment_qa_bp
from .score_routes import assessment_score_bp
from .tag_routes import assessment_tag_bp
from .user_routes import assessment_user_bp

assessment_store_bp = Blueprint("assessment_store_bp", __name__)
assessment_store_bp.register_blueprint(assessment_comment_bp, host=Config.API_HOST)
assessment_store_bp.register_blueprint(assessment_flag_bp, host=Config.API_HOST)
assessment_store_bp.register_blueprint(assessment_progress_bp, host=Config.API_HOST)
assessment_store_bp.register_blueprint(assessment_qa_bp, host=Config.API_HOST)
assessment_store_bp.register_blueprint(assessment_score_bp, host=Config.API_HOST)
assessment_store_bp.register_blueprint(assessment_tag_bp, host=Config.API_HOST)
assessment_store_bp.register_blueprint(assessment_user_bp, host=Config.API_HOST)
assessment_store_bp.register_blueprint(assessment_assessment_bp, host=Config.API_HOST)
