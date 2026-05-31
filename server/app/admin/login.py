# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse
from app import templates
from app.common.forms import LoginForm
from app.admin.auth import set_admin_cookie, clear_admin_cookie, login_required
from werkzeug.datastructures import MultiDict

router = APIRouter()


@router.get('/login/')
async def login_page(request: Request):
    """登录页面"""
    return templates.TemplateResponse('admin/login.html', {'request': request})


@router.post('/login/')
async def login_action(request: Request, name: str = Form(...), pwd: str = Form(...)):
    """登录处理"""
    form_data = MultiDict({'name': name, 'pwd': pwd})
    form = LoginForm(form_data)
    res = dict(code=0, msg='失败')
    if form.validate():
        res['code'] = 1
        response = JSONResponse(content=res)
        set_admin_cookie(response, form.data['name'])
        return response
    else:
        res['data'] = form.errors
    return res


@router.get('/admin/logout/')
async def logout(request: Request):
    """退出登录"""
    admin_name = login_required(request)
    if not admin_name:
        return RedirectResponse(url='/login/')
    response = RedirectResponse(url='/login/')
    clear_admin_cookie(response)
    return response
