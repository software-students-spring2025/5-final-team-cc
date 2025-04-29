import pytest
import os
from flask import Flask
from flask_pymongo import PyMongo
from bson import ObjectId
from app.routes import index, login, feed, create_post, post_reaction, home, logout, signup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'testsecret'
    
    # Configure MongoDB Atlas
    mongo_uri = os.getenv('MONGO_URI', '')
    if mongo_uri:
        # Append -test to the database name
        mongo_uri = mongo_uri.rsplit('/', 1)[0] + '/test_db'
        app.config["MONGO_URI"] = mongo_uri
        mongo = PyMongo(app)
        app.mongo = mongo
    else:
        raise ValueError("MONGO_URI environment variable is not set")

    # Configure template directory
    app.template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/templates')

    # Register all routes
    app.add_url_rule('/',         'index',  index)
    app.add_url_rule('/login',    'login',  login,   methods=['GET', 'POST'])
    app.add_url_rule('/feed',     'feed',   feed)
    app.add_url_rule('/post',     'create_post', create_post, methods=['GET','POST'])
    app.add_url_rule('/react',    'post_reaction', post_reaction, methods=['POST'])
    app.add_url_rule('/home',     'home',   home,    methods=['GET'])
    app.add_url_rule('/logout',   'logout', logout)
    app.add_url_rule('/signup',   'signup', signup,  methods=['GET', 'POST'])

    return app

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()

@pytest.fixture
def test_user_id():
    # Use a valid ObjectId for testing
    return ObjectId('680e7b6d99d1c4b173c2944a')  # Using one of the existing user IDs from your database