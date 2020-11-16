# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.api.views_common import CommonHandler


# 菜单接口
class GridHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        grid = {
            'style': 'width:50%;',
            'logo': self.site_url + '/static/images/bg.png',
            'name': '快捷导航',
            'data': [
                {
                    'name': '人脸检测',
                    'image': self.site_url + '/static/images/g1-1.png',
                    'url': '/pages/match/match?cate=1&uuid='
                },
                {
                    'name': '人脸勾勒',
                    'image': self.site_url + '/static/images/g1-2.png',
                    'url': '/pages/match/match?cate=2&uuid='
                },
                {
                    'name': '人脸截取',
                    'image': self.site_url + '/static/images/g1-3.png',
                    'url': '/pages/match/match?cate=3&uuid='
                },
                {
                    'name': '人脸化妆',
                    'image': self.site_url + '/static/images/g1-4.png',
                    'url': '/pages/match/match?cate=4&uuid='
                },
                {
                    'name': '人脸特征',
                    'image': self.site_url + '/static/images/g1-5.png',
                    'url': '/pages/match/match?cate=5&uuid='
                },
                {
                    'name': '关于作者',
                    'image': self.site_url + '/static/images/g1-6.png',
                    'url': '/pages/about/about'
                }
            ]
        }
        self.write(grid)
