import pytest
from flask import Flask
from app.routes import index, login, feed, create_post # Need import all our route functions (might be missing a few)

def create_app():
    app = Flask(__name__)
    app.secret_key = 'testsecret'

    # Routes throughout our app
    app.add_url_rule('/',         'index',  index)
    app.add_url_rule('/login',    'login',  login,   methods=['GET', 'POST'])
    app.add_url_rule('/feed',     'feed',   feed)
    app.add_url_rule('/post',     'post',   create_post,    methods=['GET','POST'])

    return app

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()