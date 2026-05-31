# -*- coding: utf-8 -*-
import datetime
from pymongo import MongoClient
from app.configs import mongodb_configs, app_configs
from app.common.ip2Addr import ip2addr


class CommonUtils:
    """FastAPI通用工具类"""

    site_url = app_configs['site_url']

    @staticmethod
    def get_db():
        """获取MongoDB数据库连接"""
        client = MongoClient(
            host=mongodb_configs['db_host'],
            port=mongodb_configs['db_port']
        )
        return client[mongodb_configs['db_name']]

    @staticmethod
    def current_time():
        """获取当前时间字符串"""
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def current_datetime():
        """获取当前datetime对象"""
        return datetime.datetime.now()

    @staticmethod
    def common_params(client_ip, headers):
        """构建公共参数"""
        data = dict(
            createdAt=datetime.datetime.now(),
            ip=client_ip,
            addr=ip2addr(client_ip)['region'].decode('utf-8'),
            headers=dict(headers),
        )
        return data
