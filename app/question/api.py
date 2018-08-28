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

   def get(self, current_user, question_id):
        """Method for user to view  questions"""
        database = Database(app.config['DATABASE_URL'])
        question_db = QuestionBbQueries()
        answer_db = AnswerBbQueries()
        # first check if the question was created by the logged in user
        qauthor = current_user.username
        if question_id:
            query = database.fetch_by_param('questions', 'id', question_id)
            if query:
                question = Question(query[0], query[1], query[2], query[3], query[4])
                question_answers = answer_db.fetch_by_id(question_id)
                response = {'id': question.question_id, "title": question.title,
                            'description1': question.description1,
                            "date_time": question.date_time, 'qauthor': question.qauthor,'question_answers':question_answers}
                return jsonify(response), 200
            elif question.qauthor == qauthor:
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
