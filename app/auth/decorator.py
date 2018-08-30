"""creates a token required decorator help in securing endpoints"""
from functools import wraps
from flask import request, jsonify, current_app as app
import jwt
from app.models import User
from app.database import Database


def token_required(x):
    """ Function to be decorated"""
    @wraps(x)
    def decorated(*args, **kwargs):
        """creates the decorator"""
        token = None
        if 'Auth' in request.headers:
            token = request.headers['Auth']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, 'freebobiwine')
            database = Database(app.config['DATABASE_URL'])   
            query = database.fetch_by_param(
                'users', 'username', data['username'])
            current_user = User(query[0], query[1], query[2], query[3])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return x(current_user, *args, **kwargs)

    return decorated
