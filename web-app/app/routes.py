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
    Display feed
    """

    posts = list(get_mongo().db.posts.find().sort("_id", -1))
    
    for post in posts:
        post["user_id"] = str(post["user_id"])
    
    return render_template("feed.html", posts=posts)

def create_post():
    """
    Create a post
    """
    if request.method == "POST":
        if "user_id" not in session:
            flash("You must be logged in to create a post")
            return redirect(url_for("login"))
        
        game_title = request.form.get("game_title")
        rating = int(request.form.get("rating"))
        description = request.form.get("description")
        recommends = request.form.get("recommends") == "true"
        
        post = {
            "user_id": ObjectId(session["user_id"]),
            "game_title": game_title,
            "rating": rating,
            "description": description,
            "recommends": recommends,
            "likes": 0,
            "dislikes": 0
        }
        
        get_mongo().db.posts.insert_one(post)
        flash("Your review has been posted!")
        
        return redirect(url_for("feed"))
    
    return render_template("post.html")

