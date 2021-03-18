from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import os
from datetime import timedelta

application = Flask(__name__)
application.secret_key = "cute"
application.permanent_session_lifetime = timedelta(days=5)

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