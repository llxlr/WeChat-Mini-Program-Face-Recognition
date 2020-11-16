# -*- coding: utf-8 -*-
import os
from app.ui.ui_page import PageUI

root_path = os.path.dirname(__file__)

# 公共配置
configs = dict(
    xsrf_cookies=True,
    cookie_secret='fdf6a806164946fb944bcef6c7083fe2',
    static_path=os.path.join(root_path, 'static'),
    template_path=os.path.join(root_path, 'templates'),
    ui_modules=dict(
        page=PageUI
    ),
    debug=True  # True开启调试模式，False关闭调试模式
)

# mongodb配置
mongodb_configs = dict(
    db_host='127.0.0.1',
    db_port=27017
)
