import unittest
import psycopg2
from flask import json
from app import create_app
from app.database import Database


class TestBase(unittest.TestCase):
    """ Base class for all test classess """
    app = create_app('TESTING')
    app.app_context().push()
    client = app.test_client()

    user = {
        'name': ' name',
        'username': 'namet',
        'password': 'password'
    }

    valid_user = {
        'name': 'TestUser',
        'username': 'validuser',
        'password': 'password'
    }

    valid_question = {
        'title': 'title',
        'description1': "description1"
    }
    post_question = {
        'title': 'What is flask',
        'description1': "Am a newbie in programmming and would love to know what flask is in python?"
    }
    post_answer = {
        'text1':'toppppppppppppppppp'
    }



    def setUp(self):
        db = Database(
            'postgresql://postgres:andela@localhost:5432/test_db')
        db.create_tables()
        self.create_valid_user()

    def create_valid_user(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/auth/register',
                                    data=json.dumps(self.valid_user),
                                    content_type='application/json')
        return response

    def get_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(self.valid_user),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return data['token']

    def create_valid_question(self):
        """ Creates a valid question to be used for tests """
        response = self.client.post('api/v2/users/questions/',
                                    data=json.dumps(self.valid_question),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        return response

    def create_post_question(self):
        """ Creates a valid question to be used for tests """
        response = self.client.post('api/v2/questions/',
                                    data=json.dumps(self.post_question),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        return response

    def create_aauthor(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/auth/register',
                                    data=json.dumps(self.user),
                                    content_type='application/json')
        return response

    def author_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps({
                                        'username': 'passenger',
                                        'password': 'password'}),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return data['token']

    def tearDown(self):
        db = Database(
            'postgresql://postgres:andela@localhost:5432/test_db')
        db.trancate_table("users")
        db.trancate_table("questions")
        db.trancate_table("answers")
       
