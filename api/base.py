#coding=utf-8


from flask.views import MethodView
from flask import jsonify,Blueprint


class ApiJsonify(object):
  @classmethod
  def response(cls,status,errmsg="",**kw):
    dic = {'status':status,errmsg:errmsg,"data":kw}
    return jsonify(dic)

  @classmethod
  def ok(cls,**kw):
    return cls.response(200,**kw)

  @classmethod
  def no(cls,errmsg,status=500,**kw):
    return cls.response(status,errmsg=errmsg,**kw)

class RestView(MethodView,ApiJsonify):
  pass

class RestApi(object):
  def __init__(self,name,import_name,**kw):
    self.bp= Blueprint(name,import_name,**kw)
  def route(self,url,**options):
    """ 通过装饰器注册路由

        以下是例子:

            api = RestApi('home', __name__)

            @api.route('/')
            @api.route('/home, endpoint='home')
            class HomeApi(RestView):

                def get(self):

                    return self.ok()

        也可以限制每个路由接受的方法

            @api.route('/', methods=['GET'])
            @api.route('/create, methods=['POST'])
            class EmployeeCreateApi(RestView):

                def get(self):
                    return self.ok()

                def post(self):
                    name = request.form.get('name')
                    ...
                    return self.ok()

    """
    def decorator(cls):
      endpoint = options.pop("endpoint",None) or cls.__name__
      methods = options.pop('methods',None) or cls.methods
      self.bp.add_url_rule(
        url,view_func=cls.as_view(endpoint),methods=methods
      )
      return cls
    return decorator