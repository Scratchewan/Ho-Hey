from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
# import sqlite3

# current_directory = os.path.dirname(os.path.abspath(__file__))

database = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    application = Flask(__name__)
    application.config['SECRET_KEY'] = 'cute'
    application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/Ho Hey'
    # application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    database.init_app(application)

    from .views import views
    from .auth import auth

    application.register_blueprint(views, url_prefix='/')
    application.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(application)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(application)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return application

def create_database(application):
    if not path.exists('HoHey/' + DB_NAME):
        database.create_all(app=application)
