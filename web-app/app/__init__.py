import os
from flask import Flask
from flask_pymongo import PyMongo
from os import environ
from dotenv import load_dotenv
from app.routes import index, login, feed, create_post, post_reaction, home, logout, signup

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = environ.get("MONGO_URI", "")
app.config["SECRET_KEY"] = os.urandom(24)

mongo = PyMongo(app)
app.mongo = mongo

# Register routes
app.route("/")(index)
app.route("/login", methods=["GET", "POST"])(login)
app.route("/feed")(feed)
app.route("/post", methods=["GET", "POST"])(create_post)
app.route("/react", methods=["POST"])(post_reaction)
app.route("/home", methods=["GET"])(home)
app.route("/logout")(logout)
app.route("/signup", methods=["GET", "POST"])(signup)
