# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request
from app import get_db
from app.common.utils import CommonUtils

router = APIRouter()


@router.post('/user/')
async def user_login(request: Request):
    """用户授权登录"""
    result = dict(code=0, msg='失败')

    body = await request.json()
    data = dict(**body, **CommonUtils.common_params(request.client.host, request.headers))

    db = get_db()
    record = db.loginlog.insert_one(data)
    last_id = record.inserted_id

    if last_id:
        result = dict(code=1, msg='成功', last_id=str(last_id))

    return result
