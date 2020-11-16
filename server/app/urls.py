# -*- coding: utf-8 -*-
from app.admin.views_index import IndexHandler as admin_index
from app.admin.views_login import LoginHandler as admin_login
from app.admin.views_login import LogoutHandler as admin_logout
from app.admin.views_account import AccountAddHandler as admin_account_add
from app.admin.views_account import AccountListHandler as admin_account_list
from app.admin.views_account import AccountDeleteHandler as admin_account_delete
from app.admin.views_face import FaceHandler as admin_face
from app.admin.views_face import FaceDeleteHandler as admin_face_delete
from app.admin.views_face import FaceDetailHandler as admin_face_detail
from app.admin.views_face import FaceStatusHandler as admin_face_status
from app.admin.views_loginlog import LoginlogHandler as admin_loginlog
from app.admin.views_loginlog import LoginDetailHandler as admin_loginlog_detail

from app.api.views_index import IndexHandler as api_index
from app.api.views_user import UserHandler as api_user
from app.api.views_grid import GridHandler as api_grid
from app.api.views_match import MatchHandler as api_match

# 相同视图名称可以用不同的别名来区分命名

# API接口
api_urls = [
    (r'/', api_index),
    (r'/user/', api_user),
    (r'/grid/', api_grid),
    (r'/match/', api_match),
]

# 后台系统
admin_urls = [
    (r'/admin/', admin_index),
    (r'/login/', admin_login),
    (r'/admin/logout/', admin_logout),
    (r'/admin/account/add/', admin_account_add),
    (r'/admin/account/', admin_account_list),
    (r'/admin/account/delete/', admin_account_delete),
    (r'/admin/face/', admin_face),
    (r'/admin/face/delete/', admin_face_delete),
    (r'/admin/face/detail/', admin_face_detail),
    (r'/admin/face/status/', admin_face_status),
    (r'/admin/loginlog/', admin_loginlog),
    (r'/admin/loginlog/detail/', admin_loginlog_detail),
]

# urls汇总
urls = api_urls + admin_urls
