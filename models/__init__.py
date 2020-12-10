# coding=utf-8
from datetime import datetime

from extends import db

class Role(db.Model):
  
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    display_name = db.Column(db.String(20), nullable=False)


class Department(db.Model):

    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, unique=True)  # 企业微信设置的id
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Boolean, default=False)


class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, nullable=False)
    usercode = db.Column(db.String(20), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    account_type = db.Column(db.Integer, default=0)
    name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(11), nullable=False)
    avatar = db.Column(db.String(255), default="")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
