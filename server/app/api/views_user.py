# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.api.views_common import CommonHandler


# 定义用户授权登录的视图
class UserHandler(CommonHandler):
    # 运行进行跨域访问
    def check_xsrf_cookie(self):
        return True

    # POST请求
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    # 耗时处理
    @tornado.concurrent.run_on_executor
    def post_response(self):
        result = dict(
            code=0,
            msg='失败'
        )
        # 添加数据进行组装，**展开字典进行拼接
        data = dict(
            self.params,
            **self.common_params
        )
        # 插入记录到数据库
        # 切换到face_project数据库
        db = self.md.face_project
        # 把数据插入loginlog集合
        record = db.loginlog.insert_one(data)
        # 获取最近插入ID
        last_id = record.inserted_id
        # 判断是否插入成功
        if last_id:
            result = dict(
                code=1,
                msg='成功',
                last_id=str(last_id)
            )
        # 响应接口
        self.write(result)
