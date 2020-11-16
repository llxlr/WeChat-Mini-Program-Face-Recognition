# -*- coding: utf-8 -*-
import tornado.web  # web框架
import tornado.ioloop  # 事件循环
import tornado.options  # 命令解析工具
import tornado.httpserver  # http服务

from tornado.options import options, define
from app.configs import configs, mongodb_configs
from app.urls import urls
from pymongo import MongoClient  # mongodb的客户端连接工具

# 配置一个服务启动的端口
define('port', type=int, default=8003, help='运行端口')


# 自定义应用
class CustomApplication(tornado.web.Application):
    def __init__(self, urls, configs):
        settings = configs
        handlers = urls
        # 集成mongodb
        self.md = MongoClient(
            host=mongodb_configs['db_host'],
            port=mongodb_configs['db_port']
        )
        super(CustomApplication, self).__init__(handlers=handlers, **settings)


# 创建服务
def create_server():
    tornado.options.parse_command_line()
    # 创建http服务
    # xheaders=True，获取用户访问的真实IP地址的时候
    http_server = tornado.httpserver.HTTPServer(
        CustomApplication(urls, configs),
        xheaders=True
    )
    # 监听端口
    http_server.listen(options.port)
    # 启动输入输出事件循环
    tornado.ioloop.IOLoop.instance().start()
