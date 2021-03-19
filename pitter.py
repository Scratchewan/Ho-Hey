from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin
from os import path

database = SQLAlchemy()
DB_NAME = "database.db"

application = Flask(__name__)
application.secret_key = "cute"
application.permanent_session_lifetime = timedelta(days=5)

application.config['SECRET_KEY'] = 'cute'
application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
database.init_app(application)

def create_database(application):
    if not path.exists('website/' + DB_NAME):
        database.create_all(application=application)

create_database(application)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(application)

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    password = database.Column(database.String(255))
    first_name = database.Column(database.String(255))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

cors = CORS(application, resourse={r"/*":{"origins":"*"}})

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
        user = request.form["nm"]
        session["user"] = user
        # return redirect(url_for("user", usr=user))
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

# @application.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}</h1>"

@application.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

@application.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

def main():
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()