"""This module handles class based views for authentication"""
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
import jwt
from flask.views import MethodView
from flask import jsonify, request
from flask import current_app as app
from app.models import User
from app.validate import validate_user, validate_login
from app.database import Database, UserBbQueries
import re
from app.auth.decorator import token_required
decorators = [token_required]
class RegistrationView(MethodView):
    """This class-based view registers a new user."""
    def post(self):
        """registers a user"""
        database = Database(app.config['DATABASE_URL'])
        user_db = UserBbQueries()
        data = request.get_json()
        validate = validate_user(data)
        if validate == 'valid':
            user_query = database.fetch_by_param(
                'users', 'username', data['username'])
            if user_query:
                return jsonify({'message': 'User already exists. Please login.'}),409
            else:
                user_db.insert_user_data(data)
                return jsonify({'message': 'You registered successfully. Please login.'}),201
        return jsonify({'message': validate}), 406

class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""
    def post(self):
        '''Logs in a registered user and returns a token'''
        database = Database(app.config['DATABASE_URL'])
        data = request.get_json()
        validate = validate_login(data)
        if validate == 'valid':
            try:
                query = database.fetch_by_param(
                    'users', 'username', data['username'])
                if not query:
                    return jsonify({ 'message': 'user not found ,' +
                        ' please register an account to continue.'}),401
                the_user = User(query[0], query[1], query[2], query[3])
                if the_user.username == data['username'] and\
                        check_password_hash(the_user.password,
                                            data['password']):
                    # Generates the access token
                    token = jwt.encode(
                        {'username': the_user.username,
                         'exp': datetime.utcnow() +
                         timedelta(days=1)
                         },'freebobiwine')
                    if token:
                        return jsonify({'message': 'You logged in successfully.',
                            'token': token.decode('UTF-8')}),200
                else:
                    return jsonify({'message': 'Invalid username or password,' +
                        ' Please try again.'}),403
            except Exception as e:
                return jsonify({'message':str(e) }),500
        return jsonify({'message': validate}), 406



        
        
