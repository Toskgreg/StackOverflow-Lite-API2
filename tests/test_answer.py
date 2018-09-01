
from test_base import TestBase
from flask import json


class TestAnswer(TestBase):
    """ Defines tests for the view methods of answers """

    def setUp(self):
        self.create_valid_user()
        self.create_valid_question()
        self.create_author()

    def test__answer_issuccesful(self):
        """Test API can succesfully send a answer to join
        a question (POST answer)"""
        response = self.client.post('api/v2/questions/1/answers',
                                    content_type='application/json',
                                    headers={'Auth':
                                             self.author_token()
                                             },
                                    data=json.dumps({
                                        "text1":"cccc"
                                    })
                                             )

        self.assertEqual(response.status_code, 201)

    def test_user_cannot_answer_own_question(self):
        """Test if a user can answer to join his own question"""
        response = self.client.post('api/v2/questions/1/answers',
                                    content_type='application/json',
                                    headers={'Auth':
                                             self.get_token()
                                             },
                                    data=json.dumps({
                                        "text1":"cccc"
                                    })         
                                             )
        self.assertEqual(response.status_code, 403)

    def test_users_can_only_view_their_own_question_answers(self):
        """Test if user can view question answer of a question he did not create"""
        response = self.client.get('api/v2/questions/1/answers',
                                   headers={'Auth':
                                            self.author_token()
                                            })
        self.assertEqual(response.status_code, 405)

    def test_respond_to_answer_with_accepted(self):
        """Tests if a question author can respond to a question answer with accepted"""
        response = self.client.put('api/v2/questions/1/answers/1',
                                   content_type='application/json',
                                   data=json.dumps({'status': 'accepted'}),
                                   headers={'Auth':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        self.assertIn('you have accepted this answer',
                      str(response.data))

    def test_respond_to_answer_with_rejected(self):
        """Tests if a question author can respond to a question answer with rejected"""
        response = self.client.put('api/v2/questions/1/answers/1',
                                   content_type='application/json',
                                   data=json.dumps({'status': 'not accepted'}),
                                   headers={'Auth':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        self.assertIn('you have not accepted this answer',
                      str(response.data))

    def test_respond_to_other_users_answers(self):
        """
        Tests if a user can respond to  answers for questions
         he did not create
        """
        response = self.client.put('api/v2/questions/1/answers/1',
                                   content_type='application/json',
                                   data=json.dumps({'status': 'rejected'}),
                                   headers={'Auth':
                                            self.author_token()
                                            })
        self.assertEqual(response.status_code, 404)

    def test_respond_to_answer_with_invalid_status(self):
        """Tests sending reponding without accepted/rejected """
        response = self.client.put('api/v2/questions/1/answers/1',
                                   content_type='application/json',
                                   data=json.dumps({'status': 'invalid'}),
                                   headers={'Auth':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 406)
