from flask import json
from test_base import TestBase


class Testquestion(TestBase):
    """ Defines tests for the view methods of questions """

    def setUp(self):
        self.create_valid_user()

    def test_accessing_question_view_without_token(self):
        """ Tests accessing the question endpoint without a token """
        response = self.client.get('/api/v2/questions/')
        self.assertEqual(response.status_code, 401)

    def test_accessing_question_view_with_invalid_or_expired_token(self):
        """ Tests accessing the question endpoint with an invalid
        or expired token """
        response = self.client.get('/api/v2/questions/',
                                   headers={'Auth':
                                            'XBA5567SJ2K119'})
        self.assertEqual(response.status_code, 401)

    def test_create_question_with_valid_details(self):
        """ Tests adding a question with valid details """
        response = self.create_post_question()
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            'You offered a question successfully.',
            str(response.data))

    def test_create_question_with_blank_attributes(self):
        """ Tests creating a question with a blank title or description1 """
        question = {
            'title': '',
            'description1': ''
        }
        response = self.client.post('/api/v2/questions/',
                                    data=json.dumps(question),
                                    content_type='application/json',
                                    headers={'Auth':
                                             self.get_token()})
        self.assertEqual(response.status_code, 406)

    def test_create_question_with_invalid_characters(self):
        """ Tests creating a question with a blank title or description1 """
        question = {
            'title': '@#$%',
            'description1': '@#$%'
        }
        response = self.client.post('/api/v2/questions/',
                                    data=json.dumps(question),
                                    content_type='application/json',
                                    headers={'Auth':
                                             self.get_token()})
        self.assertEqual(response.status_code, 406)

    def test_create_duplicate_question(self):
        """ Tests creating a duplicate question (same attributes) """
        self.create_valid_question()
        response = self.create_valid_question()
        self.assertEqual(response.status_code, 409)

    def test_get_questions(self):
        """ Tests fetching all questions  """
        self.create_valid_question()
        response = self.client.get('/api/v2/questions/',
                                   headers={'Auth':
                                            self.get_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_questions_valid_id(self):
        """ Tests querying a questions by a valid ID """
        self.create_valid_question()
        response = self.client.get('api/v2/questions/',
                                   headers={'Auth':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        RESULTS = json.loads(response.data.decode())
        for question in RESULTS:
            print(question)
            print(RESULTS)
            response = self.client.get('api/v2/questions/{}'
                                       .format(question['id']),
                                       headers={'Auth':
                                                self.get_token()
                                                })
            self.assertEqual(response.status_code, 200)

    def test_questions_view_with_invalid_id(self):
        """ Tests querying for a question with a none existent ID """
        response = self.client.get('/api/v2/questions/x',
                                   headers={'Auth':
                                            self.get_token()})
        self.assertEqual(response.status_code, 404)
    

    def test_delete_questions_valid_id(self):
        """ Tests deleting a questions by a valid ID """
        self.create_valid_question()
        response = self.client.get('api/v2/questions/',
                                   headers={'Auth':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        RESULTS = json.loads(response.data.decode())
        for question in RESULTS:
            print(question)
            print(RESULTS)
            response = self.client.delete('api/v2/questions/{}'
                                       .format(question['id']),
                                       headers={'Auth':
                                                self.get_token()
                                                })
            self.assertEqual(response.status_code, 200)