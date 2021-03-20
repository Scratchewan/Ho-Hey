from . import database
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data = database.Column(database.String(16384))
    date = database.Column(database.DateTime(timezone=True), default=func.now())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(128), unique=True)
    password = database.Column(database.String(128))
    first_name = database.Column(database.String(128))
    notes = database.relationship('Note')
