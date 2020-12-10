# coding=utf-8
from pprint import pprint

import click


from app import app
from app import configure_blueprints

configure_blueprints(app)

import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 
@app.cli.command()
@click.option("--key", default="ALL")
def conf(key):
    """ 打印配置信息"""
    key = key.upper()
    if key == "ALL":
        pprint(app.config.items())
    elif key in app.config:
        pprint(app.config[key])
    else:
        print("App Not Found Key: `{}`".format(key))


def main():
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
