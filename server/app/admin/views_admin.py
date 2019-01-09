# -*- coding: utf-8 -*-
import math
from app.api.views_common import CommonHandler


class AdminHandler(CommonHandler):
    # 获取用户名称
    @property
    def admin_name(self):
        return self.get_secure_cookie('name', None)

    # 请求预处理
    def prepare(self):
        # 如果会话中没有用户账号，直接跳转登录页面
        if not self.admin_name:
            self.redirect('/login/')


    # 分页方法
    def page(self, collection, model):
        # 获取页码
        page = self.get_argument('page', 1)
        page = int(page)
        # 统计总记录数
        total = collection.count()
        if total:
            # 每页显示多少条
            shownum = 15
            # 计算总页数，总记录数/每页显示数目，向上取整
            pagenum = int(
                math.ceil(total / shownum)
            )
            # 判断page小于1的情况
            if page < 1:
                page = 1
            # 判断page大于pagenum的情况
            if page > pagenum:
                page = pagenum
            # 计算分页的偏移量
            """
            1，0->15
            2，15->15
            3，30->15
            4，45->15
            """
            offset = (page - 1) * shownum
            # 分页查询
            data = model.skip(offset).limit(shownum)
            # 上一页和下一页
            prev_page = page - 1
            next_page = page + 1
            if prev_page < 1:
                prev_page = 1
            if next_page > pagenum:
                next_page = pagenum
            arr = dict(
                page=page,
                total=total,
                pagenum=pagenum,
                shownum=shownum,
                prev_page=prev_page,
                next_page=next_page,
                data=data,
                url=self.request.path
            )
        else:
            arr = []
        return arr
