import psycopg2
from test_base import TestBase
from flask import json


class TestAnswer(TestBase):
    """ Defines tests for the view methods of answers """

    def setUp(self):
        self.create_valid_user()
        self.create_aauthor()
        

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
