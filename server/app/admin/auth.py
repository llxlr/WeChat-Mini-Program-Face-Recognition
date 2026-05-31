# -*- coding: utf-8 -*-
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from itsdangerous import URLSafeSerializer
from app.configs import app_configs


def get_serializer():
    """获取序列化器"""
    return URLSafeSerializer(app_configs['cookie_secret'])


def set_admin_cookie(response, name):
    """设置管理员cookie"""
    serializer = get_serializer()
    cookie_value = serializer.dumps(name)
    response.set_cookie(
        key='admin_name',
        value=cookie_value,
        httponly=True,
    )


def get_admin_name(request: Request):
    """从cookie获取管理员名称"""
    cookie_value = request.cookies.get('admin_name')
    if not cookie_value:
        return None
    try:
        serializer = get_serializer()
        return serializer.loads(cookie_value)
    except Exception:
        return None


def clear_admin_cookie(response):
    """清除管理员cookie"""
    response.delete_cookie('admin_name')


def login_required(request: Request):
    """登录验证 - 用于页面路由"""
    admin_name = get_admin_name(request)
    if not admin_name:
        return admin_name
    return admin_name
