# coding=utf-8

from celery.schedules import crontab

DEBUG = True

#WX

WX_CORP_ID = "ww496415a282ed8602"
WX_CORP_SECRET = "j4ZlBHfoZbjVdUp8DueQG8hD2-rvKqzGtXiLWu_VIbg"
WX_AGENT_ID = "1000073"

# REDIS
REDIS_URL = "redis://localhost:6379/0"

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
CELERY_DEFAULT_QUEUE = 'wcard'
CELERY_DEFAULT_EXCHANGE = 'wcard'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_IMPORTS = [""]
CELERYBEAT_SCHEDULE = {
    
}

# DB
DB_CONFIG = dict(host="127.0.0.1", db="", username="", password="")
DB_URI = "mysql+pymysql://{}:{}@{}/{}?charset=utf8".format(
    DB_CONFIG["username"], DB_CONFIG["password"], DB_CONFIG["host"], DB_CONFIG["db"]
)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 测试用户
TEST_USERCODE = ''

