# -*- coding: utf-8 -*-
from pymongo import MongoClient
from app.configs import mongodb_configs
from werkzeug.security import check_password_hash  # 检测哈希密码


# 验证类
class Check:
    # 初始化构造方法
    def __init__(self):
        # 实例连接属性
        self.md = MongoClient(
            host=mongodb_configs['db_host'],
            port=mongodb_configs['db_port']
        )

    # 检测名称是否存在
    def check_name(self, data):
        db = self.md.face_project
        co = db.account
        match_user = co.find({'name': data}).count()
        if int(match_user):
            return True
        else:
            return False

    # 检测密码是否正确
    def check_pwd(self, name, pwd):
        db = self.md.face_project
        co = db.account
        match_user = co.find_one({'name': name})
        if match_user:
            # True匹配，False不匹配
            return check_password_hash(match_user['pwd'], pwd)
