# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.api.index import router as index_router
from app.api.user import router as user_router
from app.api.grid import router as grid_router
from app.api.match import router as match_router

# API接口总路由
router = APIRouter()
router.include_router(index_router, tags=['API'])
router.include_router(user_router, tags=['API'])
router.include_router(grid_router, tags=['API'])
router.include_router(match_router, tags=['API'])
