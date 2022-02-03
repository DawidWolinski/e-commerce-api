from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv

# Init app
app = Flask(__name__)

# Loads variables from .env
load_dotenv()

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{environ.get("DATABASE_USERNAME")}:{environ.get("DATABASE_PASSWORD")}@{environ.get("DATABASE_HOSTNAME")}:{environ.get("DATABASE_PORT")}/{environ.get("DATABASE_NAME")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Access token variables
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['ALGORITHM'] = environ.get('ALGORITHM')
app.config['ACCESS_TOKEN_EXPIRE_MINUTES'] = environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')

# Allows custom sorting of json key values
app.config ['JSON_SORT_KEYS'] = False

