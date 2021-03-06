"""Handles questions class based views"""
from flask.views import MethodView
from flask import jsonify, request, make_response, current_app as app
from app.models import Question
from app.auth.decorator import token_required
from app.validate import validate_question
from app.database import Database, QuestionBbQueries, AnswerBbQueries


class QuestionAPI(MethodView):
    """A class based view to handle questions"""
    decorators = [token_required]
    @staticmethod
    def post(current_user):
        """offers a new question"""
        question_db = QuestionBbQueries()
        data = request.get_json()

        if validate_question(data) == 'valid':
            qauthor = current_user.username
            questions_query = question_db.fetch_all()
            for question in questions_query:
                if question['title'] == data['title'] and \
                        question['description1'] == data['description1']and\
                        question['qauthor'] == current_user.username:
                    return jsonify({ 'message': 'This question already exists.'}), 409
            question_db.insert_question_data(data, qauthor)
            return jsonify({'message': 'You offered a question successfully.'}), 201
        return jsonify({'message': validate_question(data)}), 406
    @staticmethod
    def get(current_user, question_id):
        """Method for user to view  questions"""
        database = Database(app.config['DATABASE_URL'])
        question_db = QuestionBbQueries()
        answer_db = AnswerBbQueries()
        # first check if the question was created by the logged in user
        qauthor = current_user.username
        if question_id:
            query = database.fetch_by_param('questions', 'id', question_id)
            if query:
                question = Question(
                    query[0], query[1], query[2], query[3], query[4])
                question_answers = answer_db.fetch_by_id(question_id)
                response = {
                    'id': question.question_id,
                    "title": question.title,
                    'description1': question.description1,
                    "date_time": question.date_time,
                    'qauthor': question.qauthor,
                    'question_answers': question_answers}
                return jsonify(response), 200
                if question.qauthor == qauthor:
                    question_answers = answer_db.fetch_by_id(question_id)
                    if question_answers == []:
                        return jsonify({"msg": "You haven't recieved any " +
                                    " answers yet"}), 200
                    return jsonify(question_answers), 200
            return jsonify({'msg': "Question not found "}), 404

        else:
            questions = question_db.fetch_all()
            if questions == []:
                return jsonify(
                    {"msg": " There are no questions at the moment"
                     }), 200
            return jsonify(questions), 200
    @staticmethod
    def delete(current_user, question_id):
        """Method for user to view  questions"""
        database = Database(app.config['DATABASE_URL'])
        if question_id:
            database.fetch_by_paramss('questions', 'id', question_id)
            database.fetch_by_paramss('answers', 'question_id', question_id)
            return jsonify(
                {"msg": " Question has been deleted."
                 }), 200
