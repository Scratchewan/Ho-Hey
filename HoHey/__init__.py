from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

database = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    application = Flask(__name__)

    application.config['SECRET_KEY'] = 'cute'

    # application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/Ho Hey'
    # application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    application.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://elqleapqbfkcsb:02471740e9f3900006d8010e9ac3835cbca0855abf8851d6016fa41230364f84@ec2-52-45-73-150.compute-1.amazonaws.com:5432/dch8gpsf54f4m9'
    
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    database.init_app(application)

    from .views import views
    from .auth import auth

    application.register_blueprint(views, url_prefix='/')
    application.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    # if not path.exists('HoHey/' + DB_NAME):
    #     database.create_all(app=application)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(application)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return application
