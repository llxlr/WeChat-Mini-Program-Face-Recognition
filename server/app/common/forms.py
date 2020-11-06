# -*- coding: utf-8 -*-
from wtforms import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.common.check import Check


# 添加账号表单验证模型
class AccountAddForm(Form):
    name = StringField(
        '账号名称',
        validators=[
            DataRequired('账号名称不能为空！')
        ]
    )
    pwd = PasswordField(
        '账号密码',
        validators=[
            DataRequired('账号密码不能为空！')
        ]
    )
    repwd = PasswordField(
        '确认密码',
        validators=[
            DataRequired('确认密码不能为空！'),
            EqualTo('pwd', message="两次输入密码不一致！")
        ]
    )


# 登录表单验证模型
class LoginForm(Form):
    name = StringField(
        '账号名称',
        validators=[
            DataRequired("账号名称不能为空！")
        ]
    )
    pwd = PasswordField(
        '账号密码',
        validators=[
            DataRequired("账号密码不能为空！")
        ]
    )

    # 验证名称
    def validate_name(self, field):
        data = field.data
        c = Check()
        match_user = c.check_name(data)
        if not match_user:
            raise ValidationError("账号名称不存在！")

    # 验证密码
    def validate_pwd(self, field):
        pwd = field.data
        name = self.name.data
        c = Check()
        match_user = c.check_pwd(name, pwd)
        if not match_user:
            raise ValidationError("账号密码不正确！")
