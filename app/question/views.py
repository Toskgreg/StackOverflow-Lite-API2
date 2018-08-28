"""Handles adding endponts to the blueprints"""
from flask import Blueprint
from app.question.api import QuestionAPI

QUESTION_APP = Blueprint('QUESTION_APP', __name__)

QUESTION_VIEW = QuestionAPI.as_view('question_api')

QUESTION_APP.add_url_rule('/api/v2/questions/', defaults={'question_id': None},
                      view_func=QUESTION_VIEW, methods=['GET', ])
QUESTION_APP.add_url_rule('/api/v2/questions/', view_func=QUESTION_VIEW,
                      methods=['POST', ])
QUESTION_APP.add_url_rule('/api/v2/questions/<int:question_id>', view_func=QUESTION_VIEW,
                      methods=['GET', ])
QUESTION_APP.add_url_rule('/api/v2/questions/<int:question_id>', view_func=QUESTION_VIEW,
                      methods=['DELETE', ])

