# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.admin.login import router as login_router
from app.admin.index import router as index_router
from app.admin.account import router as account_router
from app.admin.face import router as face_router
from app.admin.loginlog import router as loginlog_router

# 后台管理系统路由
router = APIRouter()
router.include_router(login_router, tags=['Admin'])
router.include_router(index_router, tags=['Admin'])
router.include_router(account_router, tags=['Admin'])
router.include_router(face_router, tags=['Admin'])
router.include_router(loginlog_router, tags=['Admin'])
