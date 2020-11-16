# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.admin.views_admin import AdminHandler


class IndexHandler(AdminHandler):
    # 定义一个GET请求的方法
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # self.write("<h1 style='color:green'>这是后台管理系统！</h1>")
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        db = self.md.face_project
        co_loginlog = db.loginlog
        co_image = db.image
        data = dict(
            image_total=co_image.count(),
            image_check=co_image.find({'status': 1}).count(),
            image_uncheck=co_image.find({'status': 0}).count(),
            loginlog_total=co_loginlog.count()
        )
        self.html('admin/index.html', data=data)
