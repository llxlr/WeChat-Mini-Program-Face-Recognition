# -*- coding: utf-8 -*-
import datetime
import math

from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import RedirectResponse, JSONResponse
from app import templates, get_db
from app.admin.auth import login_required
from app.common.forms import AccountAddForm
from werkzeug.security import generate_password_hash
from werkzeug.datastructures import MultiDict
from bson.objectid import ObjectId

router = APIRouter()


@router.get('/admin/account/add/')
async def account_add_page(request: Request):
    """添加账号页面"""
    admin_name = login_required(request)
    if not admin_name:
        return RedirectResponse(url='/login/')
    return templates.TemplateResponse('admin/account_add.html', {
        'request': request,
        'admin_name': admin_name,
    })


@router.post('/admin/account/add/')
async def account_add_action(
    request: Request,
    name: str = Form(...),
    pwd: str = Form(...),
    repwd: str = Form(...),
):
    """添加账号处理"""
    admin_name = login_required(request)
    if not admin_name:
        return RedirectResponse(url='/login/')

    res = dict(code=0, msg='失败')
    form_data = MultiDict({'name': name, 'pwd': pwd, 'repwd': repwd})
    form = AccountAddForm(form_data)
    if form.validate():
        db = get_db()
        db.account.insert_one(dict(
            name=form.data['name'],
            pwd=generate_password_hash(form.data['pwd']),
            createdAt=datetime.datetime.now(),
            updatedAt=datetime.datetime.now(),
        ))
        res['code'] = 1
        res['msg'] = '成功'
    else:
        res['data'] = form.errors
    return res


@router.get('/admin/account/')
async def account_list(request: Request):
    """账号列表"""
    admin_name = login_required(request)
    if not admin_name:
        return RedirectResponse(url='/login/')

    db = get_db()
    account = db.account.find()
    data = dict(account=account)
    return templates.TemplateResponse('admin/account.html', {
        'request': request,
        'admin_name': admin_name,
        'data': data,
    })


@router.get('/admin/account/delete/')
async def account_delete(request: Request, _id: str = Query(None)):
    """删除账号"""
    admin_name = login_required(request)
    if not admin_name:
        return RedirectResponse(url='/login/')

    if _id:
        db = get_db()
        db.account.delete_one({'_id': ObjectId(_id)})
    return RedirectResponse(url='/admin/account/')
