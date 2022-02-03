from flask import Blueprint, request, jsonify
from schemas import login_schema
from utils import verify_password
from models import User
from oauth2 import create_access_token


login = Blueprint('login', __name__)


@login.route('/', methods=['POST'], strict_slashes=False)
def user_login():
    data = request.form
    error = login_schema.validate(data)

    if error:
        return jsonify(error=error, hint='Make sure to send credentials as form data'), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if user == None or verify_password(data['password'], user.password) == False:
        return jsonify(error='Invalid credentials'), 401
    
    data_dict = {'user_id': user.id}

    return jsonify(token=create_access_token(data_dict))