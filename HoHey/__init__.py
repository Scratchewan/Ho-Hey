from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

ENV = 'prod'

database = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    application = Flask(__name__)

    if ENV == 'dev':
        application.debug = True
        application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/Ho Hey'
        # application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    else:
        application.debug = False
        application.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ktjdyajigzjswv:ee6a1dfae558349472a7d3501cc77ea21b8a58fbb4d15ba19f8d6d7a1241e770@ec2-34-195-233-155.compute-1.amazonaws.com:5432/d371j372uho6t8'

    application.config['SECRET_KEY'] = 'cute'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # database.init_app(application)

    from .views import views
    from .auth import auth

    application.register_blueprint(views, url_prefix='/')
    application.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    database.create_all(app=application)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(application)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return application
