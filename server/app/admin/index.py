# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app import templates, get_db
from app.admin.auth import login_required

router = APIRouter()


@router.get('/admin/')
async def admin_index(request: Request):
    """后台管理首页"""
    admin_name = login_required(request)
    if not admin_name:
        return RedirectResponse(url='/login/')

    db = get_db()
    co_loginlog = db.loginlog
    co_image = db.image
    data = dict(
        image_total=co_image.count_documents({}),
        image_check=co_image.count_documents({'status': 1}),
        image_uncheck=co_image.count_documents({'status': 0}),
        loginlog_total=co_loginlog.count_documents({}),
    )
    return templates.TemplateResponse('admin/index.html', {
        'request': request,
        'admin_name': admin_name,
        'data': data,
    })
