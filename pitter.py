from enum import unique
from flask import Flask, app, render_template, request, redirect, url_for, session, flash, Blueprint
from flask_cors import CORS
import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import *

application = Flask(__name__)
application.secret_key = "cute"
# application.config['SECRET_KEY'] = 'cute'
# application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/Ho Hey'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.permanent_session_lifetime = timedelta(days=5)

database = SQLAlchemy(application)

class users(database.Model):
    _id = database.Column("id", database.Integer, primary_key=True)
    name = database.Column(database.String(16))
    username = database.Column(database.String(16), unique=True)
    # password = database.Column(database.String(16))

    def __init__(self, name, username):
        self.name = name
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username

# auth = Blueprint('auth', __name__)

# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(application)

# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# cors = CORS(application, resourse={r"/*":{"origins":"*"}})

# @application.route("/", methods=['GET'])
# def index():
#     # return "<h1>Hello there</h1>"
#     with open('patter.html', 'r') as file:
#         string = file.read()
#     return string

@application.route("/", methods=['GET'])
def index():
    return render_template('patter.html')

@application.route("/about", methods=['GET'])
def about():
    return "<h1>About</h1>"

@application.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form['username']
        user = users.query.filter_by(username=username).first()
        # session["user"] = user
        
        if user:
            session["username"] = user.username
        else:
            usr = users(user, None)
            database.session.add(usr)
            database.session.commit()

        flash("Login succesful!")
        # return redirect(url_for("user", usr=user))
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")

# @application.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}</h1>"

@application.route("/user", methods=["POST", "GET"])
def user():
    username = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            username = request.form["username"]
            session["username"] = username
            found_user = users.query.filter_by(name=user).first()
            found_user.username = username
            database.session.commit()
            flash("Username was saved!")
        else:
            if "username" in session:
                username = session["username"]
        
        return render_template("user.html", username=username)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@application.route("/logout")
def logout():
    # if "user" in session:
    #     user = session["user"]
    flash("You have been logged out!", "info")
    session.pop("user", None)
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    database.create_all()
    application.run(host="0.0.0.0", port=port, debug=True)