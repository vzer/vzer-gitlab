#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo

#管理登录
class LoginForm(Form):
    loginName=StringField("登录账户",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    loginPassword=PasswordField("登录密码",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    submit=SubmitField(label="点击登录")


#管理注册
class RegeditForm(Form):
    regeditName=StringField("登录账户",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    nickName=StringField("真实姓名",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    password=PasswordField("登录密码",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    repeatpassword=PasswordField("登录密码",validators=[DataRequired(message="ERROR！栏位不能为空！"),EqualTo("password",message="两次密码不一致！")])
    email=StringField("联系邮箱",validators=[Email(message="邮件地址格式不正确！")])
    invitationCode=StringField("邀请码",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    submit=SubmitField(label="点击注册")

#gitlab用户登录
class GitlabUserLogin(Form):
    loginName=StringField("登录账户",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    loginPassword=PasswordField("登录密码",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    loginFrom=SelectField(label="注册gitlab",coerce=int,validators=[DataRequired(message="ERROR,栏位不能为空")])
    submit=SubmitField(label="点击登录")

#gitlab用户注册
class GitlabRegeditForm(Form):
    username=StringField("登录账户",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    name=StringField("真实姓名",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    password=PasswordField("登录密码",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    repeatpassword=PasswordField("登录密码",validators=[DataRequired(message="ERROR！栏位不能为空！"),EqualTo("password",message="两次密码不一致！")])
    email=StringField("联系邮箱",validators=[Email(message="邮件地址格式不正确！")])
    loginFrom=SelectField(label="注册gitlab",coerce=int,validators=[DataRequired(message="ERROR,栏位不能为空")])
    submit=SubmitField(label="点击注册")


