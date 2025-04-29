from flask import (
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
    current_app,
    jsonify,
)
from bson.objectid import ObjectId
from datetime import datetime, timezone

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
        username = request.form.get("username")  # get username from form
        password = request.form.get("password")  # get password from form

        # look for the user in the MongoDB 'users' collection
        user = get_mongo().db.user.find_one({"username": username})

        if user and user["password"] == password:
            session["user_id"] = str(user["_id"])  # user session
            return redirect(url_for("home"))  # direct to home page
        flash("Invalid username or password. Please try again.")

    return render_template("login.html")  # render login page

def signup():
    """
    signup
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
    
        # check if username already in use
        existing_user = get_mongo().db.user.find_one({"username": username})
        if existing_user:
                flash("Username is already in use. Please choose another username.")
                return render_template("signup.html")

        # create a user
        get_mongo().db.user.insert_one(
            {
                "username": username,
                "password": password,
                "last_post_time": datetime.fromtimestamp(0, tz=timezone.utc)
            }
        )
        flash("Account created successfully! Please log in.")
        return redirect(url_for("login"))

    return render_template("signup.html")

def logout():
    """
    logout
    """
    session.clear()
    flash("Thanks for using GameLog!")

    return redirect(url_for("login"))

def home():
    """
    home (tamagotchi)
    """
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id_obj = ObjectId(session["user_id"])
    user = get_mongo().db.user.find_one({"_id": user_id_obj})

    last_posted = user.get("last_post_time")

    if last_posted.tzinfo is None:
        last_posted = last_posted.replace(tzinfo=timezone.utc)
    now = datetime.now(tz=timezone.utc)

    delta = now - last_posted
    hours_since = delta.total_seconds() / 3600

    happiness = max(0, min(1, 1-(hours_since/120)))
    happiness = round(happiness*100)

    user_posts = list(get_mongo().db.post.find(
        {
            "user_id": user_id_obj
        }
    ).sort("_id", -1))

    return render_template(
      "home.html",
      user=user,
      hours_since=hours_since,
      happiness=happiness,
      user_posts=user_posts
    )


def feed():
    """
    Display feed
    """
    if "user_id" not in session:
        return redirect(url_for("login"))
 
    posts = list(get_mongo().db.post.find().sort("_id", -1))
    
    # Initialize user_reactions as empty dict if user not logged in
    user_reactions = {}
    
    # If user is logged in, get their reactions to posts
    if "user_id" in session:
        user_id_obj = ObjectId(session["user_id"])
        reactions = get_mongo().db.reactions.find({"user_id": user_id_obj})
        
        # Create a dict mapping post_id to reaction_type
        for reaction in reactions:
            post_id_str = str(reaction["post_id"])
            user_reactions[post_id_str] = reaction["reaction_type"]
    
    for post in posts:
        user_id = post["user_id"]
        post["user_id"] = str(user_id)
        
        # Convert post._id to string for the template
        post_id_str = str(post["_id"])
        post["_id"] = post_id_str
        
        # Add user's reaction to this post if it exists
        post["user_reaction"] = user_reactions.get(post_id_str, None)

        print(user_id)
        
        user = get_mongo().db.user.find_one({"_id": ObjectId(user_id)})
        print(user)
        # dk if it makes sense to employ checks here, session checking should already do that
        post["username"] = user["username"]
    
    return render_template("feed.html", posts=posts)

def create_post():
    """
    Create a post
    """
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        
        game_title = request.form.get("game_title")
        rating = int(request.form.get("rating"))
        description = request.form.get("description")
        hours_played = float(request.form.get("hours_played", 0))
        recommend = request.form.get("recommends") == "true"
        
        post = {
            "user_id": ObjectId(session["user_id"]),
            "game": game_title,
            "rating": rating,
            "description": description,
            "hours_played": hours_played,
            "recommend": recommend,
            "likes": 0,
            "dislikes": 0
        }
        
        get_mongo().db.post.insert_one(post)

        get_mongo().db.user.update_one(
            {"_id": ObjectId(session["user_id"])},
            {"$set": {"last_post_time": datetime.now(timezone.utc)}}
        )
        
        flash("Your review has been posted!")
        
        return redirect(url_for("feed"))
    
    return render_template("post.html")

def post_reaction():
    """
    Handle like/dislike reactions for posts
    """
    if request.method == "POST":
        if "user_id" not in session:
            return jsonify({"success": False, "message": "You must be logged in to react"})
        
        post_id = request.form.get("post_id")
        reaction_type = request.form.get("reaction_type")  # "like" or "dislike"
        user_id = session["user_id"]
        
        if not post_id or reaction_type not in ["like", "dislike"]:
            return jsonify({"success": False, "message": "Invalid request"})
        
        try:
            post_id_obj = ObjectId(post_id)
            user_id_obj = ObjectId(user_id)
            
            post = get_mongo().db.post.find_one({"_id": post_id_obj})
            if not post:
                return jsonify({"success": False, "message": "Post not found"})
            
            # Check if the user already reacted to this post
            existing_reaction = get_mongo().db.reactions.find_one({
                "user_id": user_id_obj,
                "post_id": post_id_obj
            })
            
            likes_count = post.get("likes", 0)
            dislikes_count = post.get("dislikes", 0)
            
            if existing_reaction:
                old_reaction_type = existing_reaction["reaction_type"]
                
                if old_reaction_type == reaction_type:
                    get_mongo().db.reactions.delete_one({"_id": existing_reaction["_id"]})
                    
                    if reaction_type == "like":
                        likes_count -= 1
                    else: 
                        dislikes_count -= 1
                    
                    # Update the counters of the post
                    get_mongo().db.post.update_one(
                        {"_id": post_id_obj},
                        {"$set": {"likes": likes_count, "dislikes": dislikes_count}}
                    )
                    
                    return jsonify({
                        "success": True,
                        "message": f"{reaction_type} removed",
                        "action": "removed",
                        "likes": likes_count,
                        "dislikes": dislikes_count
                    })
                
                else:
                    get_mongo().db.reactions.update_one(
                        {"_id": existing_reaction["_id"]},
                        {"$set": {"reaction_type": reaction_type}}
                    )
                    
                    if old_reaction_type == "like":
                        likes_count -= 1
                        dislikes_count += 1
                    else:
                        likes_count += 1
                        dislikes_count -= 1
                    
                    get_mongo().db.post.update_one(
                        {"_id": post_id_obj},
                        {"$set": {"likes": likes_count, "dislikes": dislikes_count}}
                    )
                    
                    return jsonify({
                        "success": True,
                        "message": f"Changed from {old_reaction_type} to {reaction_type}",
                        "action": "changed",
                        "likes": likes_count,
                        "dislikes": dislikes_count
                    })
            
            else:
                new_reaction = {
                    "user_id": user_id_obj,
                    "post_id": post_id_obj,
                    "reaction_type": reaction_type,
                    "timestamp": datetime.fromtimestamp(0, tz=timezone.utc)
                }
                get_mongo().db.reactions.insert_one(new_reaction)
                
                if reaction_type == "like":
                    likes_count += 1
                else:
                    dislikes_count += 1
                
                get_mongo().db.post.update_one(
                    {"_id": post_id_obj},
                    {"$set": {"likes": likes_count, "dislikes": dislikes_count}}
                )
                
                return jsonify({
                    "success": True,
                    "message": f"{reaction_type} added",
                    "action": "added",
                    "likes": likes_count,
                    "dislikes": dislikes_count
                })
                
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    
    return jsonify({"success": False, "message": "Invalid method"})

