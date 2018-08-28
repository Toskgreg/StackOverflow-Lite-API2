"""Handles questions class based views"""
from flask.views import MethodView
from flask import jsonify, request, make_response, current_app as app
from app.models import Question
from app.auth.decoractor import token_required
from app.validate import validate_date, validate_question
from app.database import Database, QuestionBbQueries


class QuestionAPI(MethodView):
    """A class based view to handle questions"""
    decorators = [token_required]

    def post(self, current_user):
        """offers a new question"""
        database = Database(app.config['DATABASE_URL'])
        question_db = QuestionBbQueries()
        data = request.get_json()

        if validate_date(data['date']) != 'valid':
            return jsonify({'message': validate_date(data['date'])}), 406

        elif validate_question(data) == 'valid':

            posted_by = current_user.username

            questions_query = question_db.fetch_all()
            for question in questions_query:
                if question['title'] == data['title'] and \
                        question['description1'] == data['description1']\
                        and str(question['date']) == str(data['date']) and \
                        question['posted_by'] == current_user.username:
                    response = {
                        'message': 'This question already exists.',
                    }
                    return make_response(jsonify(response)), 409
            question_db.insert_question_data(data, posted_by)
            response = {
                'message': 'You offered a question successfully.',
            }
            return make_response(jsonify(response)), 201
        return jsonify({'message': validate_question(data)}), 406

