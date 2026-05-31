# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.configs import app_configs, mongodb_configs
from pymongo import MongoClient


# 创建模板引擎
templates = Jinja2Templates(directory=app_configs['template_path'])

# MongoDB全局连接
db_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global db_client
    db_client = MongoClient(
        host=mongodb_configs['db_host'],
        port=mongodb_configs['db_port']
    )
    yield
    if db_client:
        db_client.close()


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title='人脸识别小助手',
        debug=app_configs['debug'],
        lifespan=lifespan,
    )

    # 挂载静态文件
    app.mount('/static', StaticFiles(directory=app_configs['static_path']), name='static')

    # 注册API路由
    from app.api.router import router as api_router
    app.include_router(api_router)

    # 注册后台管理路由
    from app.admin.router import router as admin_router
    app.include_router(admin_router)

    return app


def get_db():
    """获取MongoDB数据库依赖"""
    return db_client[mongodb_configs['db_name']]
