from datetime import datetime, timedelta
from functools import wraps

import jwt as jwt
from flask import current_app, jsonify
from flask import g
from flask import request
import jwt


def create_token(user):
    payload = {
        'sub': user.id,
        'name': user.name,
        'image_url': user.image_url,
        'email': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    token = jwt.encode(payload, current_app.config['TOKEN_SECRET'])

    return token.decode('unicode_escape')


def parse_token(req):

    token = req.headers.get('Authorization').split()[0]

    return jwt.decode(token, current_app.config['TOKEN_SECRET'])


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

        """

        payload = parse_token_dummy(request)

        """
        g.user_id = payload['sub']
        g.user_name = payload['name']
        g.user_image_url = payload['image_url']
        g.user_email = payload['email']
        
        return f(*args, **kwargs)

    return decorated_function

def parse_token_dummy(req):

    token = req.headers.get('Authorization').split()[0]

    if token == 'abcd':
        payload = {
            "sub": 1,
            "name": "Siddharth",
            "image_url": None,
            "email": "siddharthnarayan27@gmail.com"
        }

        return payload

    elif token == 'efgh':
        payload = {
            "sub": 2,
            "name": "Sushant",
            "image_url": None,
            "email": "ahujasushant97@gmail.com"
        }

        return payload
