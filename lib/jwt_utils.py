from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, jsonify
from flask import g
from flask import request


def create_token(user):
    payload = {
        'sub': user.id,
        'name': user.name,
        'email': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=15)
    }
    return jwt.encode(payload, current_app.config['TOKEN_SECRET'])


def create_password_reset_link(user):
    payload = {
        'sub': user.id,
        'email': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=60)
    }
    return jwt.encode(payload, current_app.config['TOKEN_SECRET'])


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]

    return jwt.decode(token, current_app.config['TOKEN_SECRET'], algorithms=['HS256'])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except jwt.DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except jwt.ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']
        g.user_name = payload['name']
        g.user_email = payload['email']

        return f(*args, **kwargs)

    return decorated_function
