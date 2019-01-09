# -*- coding: utf-8 -*-
import json
import tornado.web
import datetime
from tornado.escape import utf8
from tornado.util import unicode_type
from concurrent.futures import ThreadPoolExecutor
from app.common.ip2Addr import ip2addr
from werkzeug.datastructures import MultiDict


class CommonHandler(tornado.web.RequestHandler):
    # 定义线程池
    executor = ThreadPoolExecutor(1000)

    # 前缀地址
    @property
    def site_url(self):
        return 'http://127.0.0.1:8003'

    # mongodb连接会话
    @property
    def md(self):
        return self.application.md

    # 客户端像服务器端发送的数据进行处理
    @property
    def params(self):
        data = self.request.body
        # 包含字节类型，转化为python数据类型
        # 由于小程序端提交数据类型是json字符串
        # json字符串在后端进行获取的时候是字节类型，解码为字符串类型
        # 将json字符串转化为字典类型
        data = {
            k: v
            for k, v in json.loads(data.decode('utf-8')).items()
        }
        return data

    # 时间属性
    @property
    def dt(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 公共参数
    @property
    def common_params(self):
        data = dict(
            createdAt=datetime.datetime.now(),
            ip=self.request.remote_ip,  # 获取IP地址
            addr=ip2addr(self.request.remote_ip)['region'].decode('utf-8'),  # 解析地址
            headers=dict(self.request.headers)  # 转化为字典类型
        )
        return data

    # ajax异步提交数据方法
    @property
    def ajax_params(self):
        data = self.request.arguments
        data = {
            k: list(
                map(
                    lambda val: str(
                        val, encoding='utf-8'
                    ),
                    v
                )
            )
            for k, v in data.items()
        }
        return data

    # 表单数据
    @property
    def form_params(self):
        return MultiDict(self.ajax_params)

    # 渲染模板
    def html(self, template_name, **kwargs):
        if self._finished:
            raise RuntimeError("Cannot render() after finish()")
        html = self.render_string(template_name, **kwargs)

        # Insert the additional JS and CSS added by the modules on the page
        js_embed = []
        js_files = []
        css_embed = []
        css_files = []
        html_heads = []
        html_bodies = []
        for module in getattr(self, "_active_modules", {}).values():
            embed_part = module.embedded_javascript()
            if embed_part:
                js_embed.append(utf8(embed_part))
            file_part = module.javascript_files()
            if file_part:
                if isinstance(file_part, (unicode_type, bytes)):
                    js_files.append(file_part)
                else:
                    js_files.extend(file_part)
            embed_part = module.embedded_css()
            if embed_part:
                css_embed.append(utf8(embed_part))
            file_part = module.css_files()
            if file_part:
                if isinstance(file_part, (unicode_type, bytes)):
                    css_files.append(file_part)
                else:
                    css_files.extend(file_part)
            head_part = module.html_head()
            if head_part:
                html_heads.append(utf8(head_part))
            body_part = module.html_body()
            if body_part:
                html_bodies.append(utf8(body_part))

        if js_files:
            # Maintain order of JavaScript files given by modules
            js = self.render_linked_js(js_files)
            sloc = html.rindex(b'</body>')
            html = html[:sloc] + utf8(js) + b'\n' + html[sloc:]
        if js_embed:
            js = self.render_embed_js(js_embed)
            sloc = html.rindex(b'</body>')
            html = html[:sloc] + js + b'\n' + html[sloc:]
        if css_files:
            css = self.render_linked_css(css_files)
            hloc = html.index(b'</head>')
            html = html[:hloc] + utf8(css) + b'\n' + html[hloc:]
        if css_embed:
            css = self.render_embed_css(css_embed)
            hloc = html.index(b'</head>')
            html = html[:hloc] + css + b'\n' + html[hloc:]
        if html_heads:
            hloc = html.index(b'</head>')
            html = html[:hloc] + b''.join(html_heads) + b'\n' + html[hloc:]
        if html_bodies:
            hloc = html.index(b'</body>')
            html = html[:hloc] + b''.join(html_bodies) + b'\n' + html[hloc:]
        return self.write(html)
