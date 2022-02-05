from flask import jsonify, request
from functools import wraps
import jwt
from datetime import datetime, timedelta
from .models import User
from .database import app


# Credit to: https://www.geeksforgeeks.org/using-jwt-for-user-authentication-in-flask/


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=int(app.config['ACCESS_TOKEN_EXPIRE_MINUTES']))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, app.config['SECRET_KEY'], algorithm=app.config['ALGORITHM'])

    return encoded_jwt


# Validates access token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if token == None:
            return jsonify(error='Access token is missing')
        
        bearer = token[0:7]
        if bearer != 'Bearer ':
            return jsonify(error='Bearer keyword is missing')

        token = token[7:(len(token))]

        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[app.config['ALGORITHM']])
            current_user = User.query.filter_by(id=payload.get("user_id")).first()

        except:
            return jsonify(error='Invalid access token'), 401

        return f(current_user, *args, **kwargs)
    
    return decorated
