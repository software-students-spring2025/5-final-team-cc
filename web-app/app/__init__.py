from flask import Flask
from flask_pymongo import PyMongo
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#Waiting on larry for this
app.config["MONGO_URI"] = environ.get("MONGO_URI", "")

mongo = PyMongo(app)
from app import routes
