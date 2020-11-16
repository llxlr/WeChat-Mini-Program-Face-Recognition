# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.api.views_common import CommonHandler
from app.common.forms import LoginForm
from app.admin.views_admin import AdminHandler


# 登录视图，登录页面不需要权限
class LoginHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        self.html('admin/login.html')

    @tornado.gen.coroutine
    def post(self):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        form = LoginForm(self.form_params)
        res = dict(code=0, msg='失败')
        if form.validate():
            # 验证通过
            res['code'] = 1
            # 把登录后用户信息保存到会话中去
            self.set_secure_cookie('name', form.data['name'])
        else:
            res['data'] = form.errors
        self.write(res)


# 退出需要把会话清除
class LogoutHandler(AdminHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie('name')
        self.redirect('/login/')
