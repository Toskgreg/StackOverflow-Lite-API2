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
                                   headers={'Authorization':
                                            'XBA5567SJ2K119'})
        self.assertEqual(response.status_code, 401)

    def test_create_question_with_valid_details(self):
        """ Tests adding a question with valid details """
        response = self.client.post('/api/v2/questions/',
                                    data=json.dumps({
                                    'title': 'title',
                                   'description1': "description1",
                                   'qauthor':"qauthor"
                                     }),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        self.assertEqual(response.status_code, 201)

    def test_create_question_with_blank_attributes(self):
        """ Tests creating a question with a blank title or description1 """
        question = {
            'title': '',
            'description1': ''
        }
        response = self.client.post('/api/v2/questions/',
                                    data=json.dumps(question),
                                    content_type='application/json',
                                    headers={'Authorization':
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
                                    headers={'Authorization':
                                             self.get_token()})
        self.assertEqual(response.status_code, 406)

    def test_get_questions(self):
        """ Tests fetching all questions  """
        self.create_valid_question()
        response = self.client.get('/api/v2/questions/',
                                   headers={'Authorization':
                                            self.get_token()})
        self.assertEqual(response.status_code, 200)




    def test_questions_view_with_invalid_id(self):
        """ Tests querying for a question with a none existent ID """
        response = self.client.get('/api/v2/questions/x',
                                   headers={'Authorization':
                                            self.get_token()})
        self.assertEqual(response.status_code, 404)
    
    def test_api_can_delete_question_by_id(self):
        """Test API can fetch a single question by using it's id."""
        response = self.client.post('/api/v2/questions/',
                                    data=json.dumps({
                                    'title': 'title',
                                   'description1': "description1",
                                   'qauthor':"qauthor"
                                     }),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        self.assertEqual(response.status_code, 201)
        response = self.client.get('api/v2/questions/')
        results = json.loads(response.data.decode())
        for question in results:
            result = self.client.delete(
                'api/v2/questions/1',
                content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
            self.assertEqual(result.status_code, 200)

    def test_post_answer_is_not_successful_with_invalid_authentication(self):
        """Test API can succesfully send answer to question (POST request)"""
        response = self.client.post('/api/v2/questions/',
                                    data=json.dumps({
                                    'title': 'title',
                                   'description1': "description1",
                                   'qauthor':"qauthor"
                                     }),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        self.assertEqual(response.status_code, 201)

        response = self.client.get('api/v2/questions/')
        results = json.loads(response.data.decode())

        for question in results:
            response = self.client.post('api/v2/questions/1/answers',
                                        content_type ='application/json',
                                        data=json.dumps({
                                         "text1": "This is a simple answer",
                                        }),
                                        headers={'Authorization':
                                             "xxxxxxxxxxxxxxxxxxxxxx"}
                                        )
            self.assertEqual(response.status_code, 401)
    
