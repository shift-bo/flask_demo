# coding=utf-8
from corp_wx.error import CorpWxError
from extends import corp_wx
from logger import logger
from model import db
from model import Department
from model import Role
from model import User as Employee
from worker import celery_app
from sqlalchemy import exc

@celery_app.task(ignore_result=True)
def sync_employee():
  app_info = corp_wx.service.get_app_info()
  if not app_info:
    return
  users = app_info["allow_userinfos"]["user"]
  usercodes = [item["userid"] for item in users]
  role = Role.query.filter_by(name="MEMBER").first()

   # 判断并添加用户
  for usercode in usercodes:
    employee = Employee.query.filter_by(usercode=usercode).first()
    if not employee:
      user_info = corp_wx.service.get_user_info(usercode)
      if not user_info:
          continue
      update_employee(user_info, role_id=role.id)
  elif employee.deleted:
      employee.deleted = False
def update_employee(member, department_id=None, role_id=None):
    """ 更新成员
    :param member: 成员信息
    :param department_id: 部门id
    :param role_id: 角色id
    """

    if not member["email"]:
        logger.error(
            u"MemberNotFoundEmail: {}, {}".format(member["userid"], member["name"])
        )
        return

    if not member['mobile']:
        logger.error(
            u"MemberNotFoundMobile: {}, {}".format(member["userid"], member["name"])
        )
        return

    if len(member['mobile']) > 11:
        logger.error(
            u"MemberMobileLengthError: {}, {}".format(member["userid"], member["name"])
        )
        return

    if not department_id:
        department_id = member["department"][-1] if member["department"] else 0

    # 默认为普通员工
    if not role_id:
        role = Role.query.filter_by(name="MEMBER").first()
        role_id = role.id

    username = member["email"].split("@")[0]
    avatar = member["avatar"][:-1] + "100"

    employee = Employee.query.filter_by(usercode=member["userid"]).first()
    if not employee:
        try:
            employee = Employee(
                usercode=member["userid"],
                name=member["name"],
                username=username,
                avatar=avatar,
                role_id=role_id,
                department_id=department_id,
                mobile=member["mobile"].strip(),
            )
            db.session.add(employee)
            logger.info("AddEmployee: {}".format(member["userid"]))
            db.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error('InsertError: {}'.format(str(e)))
            db.session.rollback()
    else:
        try:
            employee.name = member["name"]
            employee.username = username
            employee.avatar = avatar
            employee.department_id = department_id
            if employee.deleted:
                employee.deleted = False
            logger.info(
                "UpdateEmployee: {}, {}".format(employee.usercode, employee.name)
            )
            db.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error('InsertError: {}'.format(str(e)))
            db.session.rollback()


def update_department_employee(department_id):
    """ 更新部门成员
    :param department_id: 更新的部门id
    """
    logger.info("GetDepartmentMembers: {}".format(department_id))
    members = corp_wx.service.get_department_member_detail(department_id)

    if not members:
        return

    role = Role.query.filter_by(name="MEMBER").first()
    for member in members:
        update_employee(member, department_id=department_id, role_id=role.id)
    else:
        db.session.commit()


def update_delete_employee():
    """ 更新删除的人员"""
    app_info = corp_wx.service.get_app_info()
    if app_info:
        users = app_info["allow_userinfos"]["user"]
        usercodes = [item["userid"] for item in users]
    else:
        usercodes = []

    departments = Department.query.filter_by(deleted=0)
    for department in departments:
        try:
            members = corp_wx.service.get_department_member_detail(department.uid)
            usercodes.extend([member["userid"] for member in members])
        except CorpWxError as e:
            department.deleted = 1
            department.commit()

    # 现有的微信成员架构
    usercodes = list(set(usercodes))

    # 删除用户
    employees = Employee.query.filter(
        Employee.deleted == 0, ~Employee.usercode.in_(usercodes)
    )
    for employee in employees:
        employee.deleted = True
    else:
        db.session.commit()


@celery_app.task(ignore_result=True)
def sync_department():
    """ 更新部门"""
    departments = corp_wx.service.get_department_list()
    if not departments:
        return

    department_ids = [item["id"] for item in departments]

    for department in departments:
        dep = Department.query.filter_by(uid=department["id"]).first()

        if department["parentid"] in department_ids:
            parent_id = department["parentid"]
        else:
            parent_id = 0

        if not dep:
            dep = Department(
                uid=department["id"],
                name=department["name"],
                parent_id=parent_id,
                order=department["order"],
            )
            db.session.add(dep)
        else:
            dep.name = department["name"]
            dep.parent_id = parent_id
            dep.order = department["order"]
    else:
        db.session.commit()

    for department_id in department_ids:
        # 更新部门下的成员
        update_department_employee(department_id)



@celery_app.task(ignore_result=True)
def sync():
    sync_department()
    sync_employee()
    update_delete_employee()
