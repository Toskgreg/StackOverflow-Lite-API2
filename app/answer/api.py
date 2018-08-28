"""This module handles AnswerApi class and its methods"""
from flask import jsonify, make_response, request, abort, current_app as app
from flask.views import MethodView
from app.models import Question, Answer
from app.database import Database, AnswerBbQueries
from app.auth.decoractor import token_required


class AnswerAPI(MethodView):
    """This class-based view for answering a question."""
    decorators = [token_required]

    def post(self, current_user, question_id):
        """Post method view for answering a question"""
        database = Database(app.config['DATABASE_URL'])
        answer_db = AnswerBbQueries()
        data = request.get_json()

        aauthor = current_user.username
        query = database.fetch_by_param('questions', 'id', question_id)

        if query is None:
            abort(404)

        question = Question(query[0], query[1], query[2], query[3], query[4])

        if question.qauthor != aauthor:
            answer_db.post_answer(question_id,data ,aauthor)
            return jsonify({'msg': 'You have offered an answer' +
                            " Thank you."}), 201
        else:
            return jsonify(
                {'message': "You can't answer your own question"}), 403