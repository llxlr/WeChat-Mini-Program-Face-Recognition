# -*- coding: utf-8 -*-
import os
import datetime
import uuid
import tornado.gen
import tornado.concurrent
from app.api.views_common import CommonHandler
from app.common.face import Face
from bson.objectid import ObjectId


# 人类识别视图
class MatchHandler(CommonHandler):
    # 允许跨域请求
    def check_xsrf_cookie(self):
        return True

    # POST请求
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    # POST响应
    @tornado.concurrent.run_on_executor
    def post_response(self):
        self.write(self.save_image())

    # 创建上传目录
    def make_upload_dir(self):
        upload_path = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            'static/uploads'
        )
        if not os.path.exists(upload_path):
            os.mkdir(upload_path)
        return upload_path

    # 时间
    @property
    def dt(self):
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 保存名称定义
    @property
    def image_name(self):
        # 名称构成：时间+唯一字符串
        prefix1 = self.dt
        prefix2 = uuid.uuid4().hex
        return prefix1 + prefix2

    # 1.上传原图
    def upload_image(self):
        # 获取客户端上传上来文件
        files = self.request.files['img']
        # 指定保存的目录
        # 2.执行保存
        imgs_http, imgs_name, upload_path = [], [], self.make_upload_dir()
        imgs_http, imgs_name = self.save_upload_image(files, upload_path, imgs_http, imgs_name)
        return imgs_http, imgs_name, upload_path

    # 2.执行保存
    def save_upload_image(self, files, upload_path, imgs_http, imgs_name):
        for file in files:
            newname = self.image_name + os.path.splitext(file['filename'])[-1]
            imgs_name.append(newname)
            img_path = os.path.join(upload_path, newname)
            # 写入文件中去
            with open(img_path, 'wb') as up:
                up.write(file['body'])
            imgs_http.append(
                self.site_url + '/static/uploads/{}'.format(newname)
            )
        return imgs_http, imgs_name

    # 保存并检测图片
    def save_image(self):
        res = {'code': 0}
        # 上传
        imgs_http, imgs_name, upload_path = self.upload_image()
        cate_type = self.get_argument('cate', None)
        cate_type = int(cate_type)
        # 检测
        fm = Face(upload_path, imgs_name[0], upload_path)
        if cate_type == 1:
            # 人脸检测
            known_image = fm.face_box()
            name = "人脸检测"
        if cate_type == 2:
            # 人脸勾勒
            known_image = fm.face_sense()
            name = "人脸勾勒"
        if cate_type == 3:
            # 人脸截取
            known_image = fm.face_find()
            name = "人脸截取"
        if cate_type == 4:
            # 人脸化妆
            known_image = fm.face_makeup()
            name = "人脸化妆"
        if cate_type == 5:
            # 人脸特征
            known_image = fm.face_68_point()
            name = "人脸特征"
        # 检测写入到数据库中保存
        db = self.md.face_project
        # 插入记录
        record = db.image.insert_one(
            dict(
                unknown_image=imgs_http,
                known_image=list(
                    map(
                        lambda v: self.site_url + '/static/uploads/{}'.format(v),
                        known_image
                    )
                ),
                name=name,
                cate=cate_type,
                status=0,
                **self.common_params
            )
        )
        # 最近插入记录的ID
        last_id = record.inserted_id
        if last_id:
            res = {
                'code': 1,
                'cate': cate_type,
                'uuid': str(last_id)
            }
        return res

    # 根据uuid查询记录
    def get_image(self, uid):
        image_data = dict()
        db = self.md.face_project
        record = db.image.find_one({'_id': ObjectId(uid)})
        image_data['name'] = record['name']
        image_data['cate'] = record['cate']
        image_data['unknown_image'] = record['unknown_image']
        image_data['known_image'] = record['known_image']
        return image_data

    # GET请求
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        uid = self.get_argument('uuid', None)
        if uid:
            # uid存在显示识别的结果
            self.write(self.get_image(uid))
        else:
            # uid不存在显示示例
            cate = self.get_argument('cate', 1)
            data = {
                1: {
                    'cate': 1,
                    'name': '人脸检测示例',
                    'unknown_image': [self.site_url + '/static/images/exp/g.png'],
                    'known_image': [self.site_url + '/static/images/exp/g_box.png']
                },
                2: {
                    'cate': 2,
                    'name': '人脸勾勒示例',
                    'unknown_image': [self.site_url + '/static/images/exp/g.png'],
                    'known_image': [self.site_url + '/static/images/exp/g_sense.png']
                },
                3: {
                    'cate': 3,
                    'name': '人脸截取示例',
                    'unknown_image': [self.site_url + '/static/images/exp/g.png'],
                    'known_image': [
                        self.site_url + '/static/images/exp/g1.png',
                        self.site_url + '/static/images/exp/g2.png',
                        self.site_url + '/static/images/exp/g3.png',
                        self.site_url + '/static/images/exp/g4.png'
                    ]
                },
                4: {
                    'cate': 4,
                    'name': '人脸化妆示例',
                    'unknown_image': [self.site_url + '/static/images/exp/g.png'],
                    'known_image': [self.site_url + '/static/images/exp/g_makeup.png']
                },
                5: {
                    'cate': 5,
                    'name': '人脸特征示例',
                    'unknown_image': [self.site_url + '/static/images/exp/face_68.jpg'],
                    'known_image': [self.site_url + '/static/images/exp/face_68_feature.png']
                }
            }
            self.write(data[int(cate)])
