from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import os

application = Flask(__name__)

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
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@application.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

def main():
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()