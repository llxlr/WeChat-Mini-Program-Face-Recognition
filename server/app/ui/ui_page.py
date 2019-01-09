# -*- coding: utf-8 -*-
import tornado.web


# 自定义一个分页的UI组件

class PageUI(tornado.web.UIModule):
    def render(self, data=None, params=""):
        return self.render_string('ui/page.html', data=data, params=params)
