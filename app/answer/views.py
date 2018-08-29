"""This module handle the registering of the ANSWER_APP blue_print and
 adding the adds the url rule"""
"""Handle endpoints for the ANSWER_app blue prints """
from flask import Blueprint
from app.answer.api import AnswerAPI

ANSWER_APP = Blueprint('ANSWER_APP', __name__)

ANSWER_VIEW = AnswerAPI.as_view('answer_api')
ANSWER_APP.add_url_rule('/api/v2/questions/<question_id>/answers',
                        view_func=ANSWER_VIEW, methods=['POST', ])
ANSWER_APP.add_url_rule('/api/v2/questions/<question_id>/answers/<answer_id>',
                        view_func=ANSWER_VIEW, methods=['PUT', ])
