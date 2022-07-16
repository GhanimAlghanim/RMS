from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask import Blueprint

models = Blueprint('models', __name__)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(300))
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), unique=True)


class Group(db.Model):  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20),  unique=True)

class User_groups(db.Model): 
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)    

class Tag(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)



    

