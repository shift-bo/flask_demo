# coding=utf-8
# flake8: noqa
import _strptime
import os


from celery import Celery
from flask import Flask

# noqa: F401


def create_app():
    """ 创建应用"""
    app = Flask(__name__)

    configure_app(app)
    configure_extensions(app)
    configure_request_hook(app)
    return app


def configure_app(app, envconf="", defaultconf=""):
    """ 配置文件"""
    config = os.getenv(envconf, defaultconf) if envconf else defaultconf
    if config:
        if config.endswith(".py"):
            app.config.from_pyfile(config)
        else:
            app.config.from_object(config)


def configure_app_blueprints(app):
    """ 配置移动端蓝图"""
    pass


def configure_web_blueprints(app):
    """ 配置Web端蓝图"""
    pass


def configure_blueprints(app):
    """ 配置蓝图"""
    pass


def configure_extensions(app):
    """ 配置扩展"""
    from extends import db, redis_store,corp_wx
    db.init_app(app)
    redis_store.init_app(app)
    corp_wx.init_app(app)


def create_celery_app(app):
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def configure_request_hook(app):
    """ 请求钩子"""

    @app.before_request
    def before_request():
        """ 请求前钩子"""
        pass

    @app.after_request
    def after_request(response):
        """ 请求后钩子"""
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,OPTIONS,DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        return response



app = create_app()
celery_app = create_celery_app(app)
