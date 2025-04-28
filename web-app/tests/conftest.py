import pytest
from flask import Flask
from routes import index, login, feed, post, logout  # Need import all our route functions (might be missing a few)

def create_app():
    app = Flask(__name__)
    app.secret_key = 'testsecret'

    # Routes throughout our app
    app.add_url_rule('/',         'index',  index)
    app.add_url_rule('/login',    'login',  login,   methods=['GET', 'POST'])
    app.add_url_rule('/feed',     'feed',   feed)
    app.add_url_rule('/post',     'post',   post,    methods=['GET','POST'])
    app.add_url_rule('/logout',   'logout', logout)

    return app

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()