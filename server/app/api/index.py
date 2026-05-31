# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request
from app.common.utils import CommonUtils

router = APIRouter()


@router.get('/')
async def index(request: Request):
    """API首页"""
    return CommonUtils.common_params(request.client.host, request.headers)
