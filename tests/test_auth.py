import unittest
from flask import json
import psycopg2
from test_base import TestBase


class TestAuth(TestBase):

    def test_register_valid_details(self):
        """ Tests creating a new user with valid details """
        test_user = {
            'name': 'test user',
            'username': 'username',
            'password': 'password'
        }
        response = self.client.post('/api/v2/auth/signup',
                                    data=json.dumps(test_user),
                                    content_type='application/json')
        self.assertIn('You registered successfully. Please login.',
                      str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_register_invalid_characters(self):
        """ Tests creating a new user with invalid characters """
        inv_char = {
            'name': '@#$%',
            'username': '#$%',
            'password': '@#$%'
        }
        response = self.client.post('/api/v2/auth/signup',
                                    data=json.dumps(inv_char),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_register_with_blank_inputs(self):
        """ Tests creating a new user with blank """
        inv_char = {
            'name': '',
            'username': ' ',
            'password': ''
        }
        response = self.client.post('/api/v2/auth/signup',
                                    data=json.dumps(inv_char),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_register_non_json_input(self):
        """ Tests register with non valid JSON input """
        response = self.client.post('/api/v2/auth/signup',
                                    data='some non json data',
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)



    def test_login_valid_credentials(self):
        """ Tests login with valid credentials """
        """ Tests login with wrong username credentials """
        user = {
            'name': 'right user',
            'username': 'rightuser',
            'password': 'rightpassword'
        }
        self.client.post('/api/v2/auth/signup',
                         data=json.dumps(user),
                         content_type='application/json')
        user = {
            'username': 'rightuser',  # credentials for valid user.
            'password': 'rightpassword'
        }
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_characters(self):
        """ Test login with invalid characters """
        inv_char = {
            'username': '#$%',
            'password': '@#$%'
        }
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(inv_char),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_login_with_blank_inputs(self):
        """ Tests creating a new user with blank """
        inv_char = {

            'username': ' ',
            'password': ''
        }
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(inv_char),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 406)

    def test_login_wrong_username(self):
        """ Tests login with wrong username credentials """
        user = {
            'name': 'right user',
            'username': 'rightuser',
            'password': 'rightpassword'
        }
        self.client.post('/api/v2/auth/register',
                         data=json.dumps(user),
                         content_type='application/json')
        user_login = {
            'username': 'wrongusername',
            'password': 'rightpassword'
        }
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(user_login),
                                    content_type='application/json')

        self.assertIn(
            'user not found , please register',
            str(response.data))
        self.assertEqual(response.status_code, 401)

    def test_login_invalid_password(self):
        """ Tests login with wrong password  """
        user = {
            'name': 'right user',
            'username': 'rightuser',
            'password': 'rightpassword'
        }
        self.client.post('/api/v2/auth/register',
                         data=json.dumps(user),
                         content_type='application/json')
        user_login = {
            'username': 'rightuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(user_login),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_user_siginup_user_already_exissts(self):
        """Test API can signup already_exissts"""

        self.create_valid_user()
        res = self.create_valid_user()
        self.assertTrue(res.status_code, 409)
        self.assertIn('User already exists. Please login.', str(res.data))

