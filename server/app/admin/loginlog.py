# -*- coding: utf-8 -*-
import math
import pymongo

from fastapi import APIRouter, Request, Query
from fastapi.responses import RedirectResponse
from app import templates, get_db
from app.admin.auth import login_required
from bson.objectid import ObjectId

router = APIRouter()


def paginate(collection, page, url_path, per_page=15):
    """分页工具函数"""
    page = int(page)
    total = collection.count_documents({})
    if total:
        pagenum = int(math.ceil(total / per_page))
        if page < 1:
            page = 1
        if page > pagenum:
            page = pagenum
        offset = (page - 1) * per_page
        data = list(collection.find().sort('createdAt', pymongo.DESCENDING).skip(offset).limit(per_page))
        prev_page = max(page - 1, 1)
        next_page = min(page + 1, pagenum)
        return dict(
            page=page,
            total=total,
            pagenum=pagenum,
            shownum=per_page,
            prev_page=prev_page,
            next_page=next_page,
            data=data,
            url=url_path,
        )
    return None


@router.get('/admin/loginlog/')
async def loginlog_list(request: Request, page: int = Query(1)):
    """授权日志列表"""
    admin_name = login_required(request)
    if not admin_name:
        return RedirectResponse(url='/login/')

    db = get_db()
    co = db.loginlog
    log_data = paginate(co, page, str(request.url.path))
    return templates.TemplateResponse('admin/loginlog.html', {
        'request': request,
        'admin_name': admin_name,
        'data': dict(loginlog=log_data),
    })


@router.get('/admin/loginlog/detail/')
async def loginlog_detail(request: Request, _id: str = Query(None)):
    """授权日志详情"""
    admin_name = login_required(request)
    if not admin_name:
        return RedirectResponse(url='/login/')

    db = get_db()
    record = db.loginlog.find_one({'_id': ObjectId(_id)})
    return templates.TemplateResponse('admin/loginlog_detail.html', {
        'request': request,
        'admin_name': admin_name,
        'data': dict(loginlog=record),
    })
