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

    def put(self, current_user, question_id, answer_id):
        """Accept an answer or update it."""
        database = Database(app.config['DATABASE_URL'])
        answer_db = AnswerBbQueries()
        # first check if the question was created by the logged in author
        qauthor = current_user.username
        aauthor = current_user.username
        query = database.fetch_by_param('questions', 'id', question_id)
        query1 = database.fetch_by_param('answers', 'id', answer_id)
        if query is None:
            abort(404)
        question = Question(query[0], query[1], query[2], query[3], query[4])
        if question.qauthor == qauthor:
            data = request.get_json()
            print(data['status'])
            if data['status'] == 'accepted' or data['status'] == 'rejected':

                answer_db.update_answer_status(answer_id, data)
                response = {
                    'message': 'you have {} this answer'
                    .format(data['status'])
                }
                return make_response(jsonify(response)), 200

            response = {
                'message': 'The status can only be in 3 states,' +
                'answered, accepted and rejected'
            }
            return make_response(jsonify(response)), 406

        query1 = database.fetch_by_param('answers', 'id', answer_id)
        if query1 is None:
            abort(404)
        answer = Answer(query1[0], query1[1], query1[2], query1[3], query1[4])
        if answer.aauthor ==aauthor:
            data = request.get_json()
            text1 = data['text1']
            answer_db.update_answer(answer_id, text1)
            return jsonify ({"message":"You have updated your answer"}),201