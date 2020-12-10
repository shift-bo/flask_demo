# coding=utf-8
from flask_login import LoginManager
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from corp_wx import CorpWx

db = SQLAlchemy()
login_manager = LoginManager()
redis_store = FlaskRedis()
corp_wx = CorpWx()