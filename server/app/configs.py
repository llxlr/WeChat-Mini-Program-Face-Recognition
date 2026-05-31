# -*- coding: utf-8 -*-
import os

root_path = os.path.dirname(__file__)

# 应用配置
app_configs = dict(
    debug=True,
    site_url='http://127.0.0.1:8003',
    cookie_secret='fdf6a806164946fb944bcef6c7083fe2',
    static_path=os.path.join(root_path, 'static'),
    template_path=os.path.join(root_path, 'templates'),
)

# MongoDB配置
mongodb_configs = dict(
    db_host='127.0.0.1',
    db_port=27017,
    db_name='face_project',
)
