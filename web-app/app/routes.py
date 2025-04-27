from flask import (
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
    current_app,
)
from bson.objectid import ObjectId

def get_mongo():
    """
    Helper function to get the current MongoDB instance
    """
    return current_app.mongo

def index():
    """
    temp route
    """
    return redirect(url_for("login"))

def login():
    """
    login
    """
    if request.method == "POST":
        username = request.form["username"]  # get username from form
        password = request.form["password"]  # get password from form

        # look for the user in the MongoDB 'users' collection
        user = get_mongo().db.user.find_one({"username": username})
        print(user)

        if user and user["password"] == password:
            session["user_id"] = str(user["_id"])  # user session
            return redirect(url_for("feed"))  # direct to home page
        flash("Invalid username or password. Please try again.")

    return render_template("login.html")  # render login page

def feed():
    """
    feed
    """
    return render_template("feed.html")

