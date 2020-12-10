from models import Employee,Role
from extends import db

@app.cli.command()
def sync():
    """同步部门和员工"""
    from tasks.employee import sync
    sync()

@app.cli.command()
def init_role():
    """初始化权限"""
    role = [{'id':'1','name':'MEMBER','display_name':'用户'},{'id':'2','name':'MODELADMIN','display_name':'模块管理员'},
    {'id':'3','name':'SUPERADMIN','display_name':'超级管理员'},]
    for i in role:
        db.session.add(Role(name=i['name'],display_name=i['display_name']))
    else:
        db.session.commit()

