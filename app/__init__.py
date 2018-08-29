"""Creates module is the main application factory"""
from flask import Flask
from flask_cors import CORS
from config import app_config
from app.database import Database
from app.error_handler import *


def create_app(config_name):
    """Creates the application and registers the blueprints
        with the application
    """
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config.from_object(app_config[config_name])

    from app.question.views import QUESTION_APP
    from app.auth.views import AUTH_BLUEPRINT
    from app.answer.views import ANSWER_APP

    # register_blueprint
    app.register_blueprint(AUTH_BLUEPRINT)
    app.register_blueprint(QUESTION_APP)
    app.register_blueprint(ANSWER_APP)

    # register error handlers
    app.register_error_handler(404, not_found)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(405, method_not_allowed)

    return app
