from flask import Flask
from flask_cors import CORS
import os

application = Flask(__name__)

cors = CORS(application, resourse={r"/*":{"origins":"*"}})

@application.route("/", methods=['GET'])
def index():
    # return "<h1>Hello there</h1>"
    with open('patter.html', 'r') as file:
        string = file.read()
    return string

@application.route("/about", methods=['GET'])
def about():
    return "<h1>About</h1>"

def main():
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()