# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
import pymongo
from app.admin.views_admin import AdminHandler
from bson.objectid import ObjectId


# 人脸管理视图
class FaceHandler(AdminHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        db = self.md.face_project
        co = db.image
        # 按照创建时间降序排序
        model = co.find().sort('createdAt', pymongo.DESCENDING)
        data = dict(
            face=self.page(co, model)
        )
        self.html('admin/face.html', data=data)


# 删除人脸识别记录
class FaceDeleteHandler(AdminHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        status = yield self.get_response()
        if status:
            self.redirect("/admin/face/")

    @tornado.concurrent.run_on_executor
    def get_response(self):
        _id = self.get_argument('_id', None)
        if _id:
            db = self.md.face_project
            co = db.image
            co.remove({'_id': ObjectId(_id)})
            return True


# 人脸识别记录详情
class FaceDetailHandler(AdminHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        _id = self.get_argument("_id", None)
        if _id:
            db = self.md.face_project
            co = db.image
            data = dict(
                face=co.find_one({'_id': ObjectId(_id)})
            )
            self.html('admin/face_detail.html', data=data)


# 审核人脸识别记录视图
class FaceStatusHandler(AdminHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        status = yield self.get_response()
        if status:
            self.redirect('/admin/face/')

    @tornado.concurrent.run_on_executor
    def get_response(self):
        _id = self.get_argument("_id", None)
        if _id:
            db = self.md.face_project
            co = db.image
            co.update(
                {'_id': ObjectId(_id)},
                {'$set': {'status': 1}}
            )
            return True
