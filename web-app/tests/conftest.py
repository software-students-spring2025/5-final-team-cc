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
    mongo_uri = os.getenv('TEST_URI', '')
    if mongo_uri:
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
    return ObjectId('681057d55e6a93269c8c9155')  # Using the dummy johndoe test user

@pytest.fixture
def test_happiness_user_id():
    return ObjectId('68105df863a89476fe07f296') # Using the dummy test_happiness user