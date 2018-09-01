"""Creates module is the main application factory"""
from flask import Flask,jsonify
from config import app_config
from flask_cors import CORS
from app.database import Database


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
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': "Bad request please input all fields"}),400
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'message': "Please use an appropiate request method"}),405
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message': "Internal server error"}),500
    @app.errorhandler(404)
    def url_not_found(error):
        return jsonify({'message': "Requested URL is invalid"}),404

    return app
