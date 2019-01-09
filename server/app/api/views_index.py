# -*- coding: utf-8 -*-
import time
import tornado.gen
import tornado.concurrent
from app.api.views_common import CommonHandler


class IndexHandler(CommonHandler):
    # 定义一个GET请求的方法
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    # 让阻塞的代码在线程池里面运行
    # 尽量避免写耗时的代码，即使有耗时代码采用线程池的模式运行
    @tornado.concurrent.run_on_executor
    def get_response(self):
        # time.sleep(6)
        # self.write("<h1 style='color:blue'>这是API接口！</h1>")
        # self.write("<h1 style='color:red'>{}</h1>".format(str(self.md)))
        self.write(self.common_params)  # 字典默认转化为json响应给浏览器端
