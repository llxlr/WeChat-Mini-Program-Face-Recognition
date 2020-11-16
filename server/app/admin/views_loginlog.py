# -*- coding: utf-8 -*-
import pymongo
import tornado.gen
import tornado.concurrent
from app.admin.views_admin import AdminHandler
from bson.objectid import ObjectId


# 授权日志列表
class LoginlogHandler(AdminHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        db = self.md.face_project
        co = db.loginlog
        model = co.find().sort('createdAt', pymongo.DESCENDING)
        data = dict(
            loginlog=self.page(co, model)
        )
        self.html('admin/loginlog.html', data=data)


# 授权日志详情
class LoginDetailHandler(AdminHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        _id = self.get_argument("_id", None)
        if _id:
            db = self.md.face_project
            co = db.loginlog
            data = dict(
                loginlog=co.find_one({'_id': ObjectId(_id)})
            )
            self.html('admin/loginlog_detail.html', data=data)
