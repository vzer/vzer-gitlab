#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

import sys

from flask import flash,redirect,url_for,request
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user
from wtforms import fields, widgets
from wtforms.validators import required,Email
reload(sys)
sys.setdefaultencoding("utf-8")


#用户管理
class UserAdmin(ModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_searchable_list = ["username","nickname","email"]
    column_filters = ["pending"]
    column_exclude_list = ["password","isactive","isadmin"]
    column_details_exclude_list =["password","isactive","isadmin"]
    form_excluded_columns = ["createtime","updatetime","logintime","isactive","isadmin"]
    column_labels = dict(username="登录账户",email="电子邮箱",nickname="用户姓名",isadmin="管理",isactive="状态",createtime="创建日期",updatetime="修改时间",password="用户密码",logintime="登录时间",pending="审核状态")
    form_args = {
        "username":{
            "label":"登录账户",
            "validators":[required()]
        },
        "email":{
            "label":"电子邮箱",
            "validators":[required(),Email()]
        },
        "nickname":{
            "label":"用户名称",
            "validators":[required()]
        },
        "isactive":{
            "label":"是否激活",
        },
        "isadmin":{
            "label":"是否admin",
        },
        "createtime":{
            "label":"创建时间",
            "validators":[required()]
        },
        "password":{
            "label":"用户密码",
            "validators":[required()]
        },
        "updatetime":{
            "label":"更新时间",
            "validators":[required()]
        },
        "logintime":{
            "label":"登录时间",
            "validators":[required()]
        },
    }
    def __init__(self,session):
        from vzerGit.extensions import db
        from vzerGit.models.DBmodels import Manage_user
        super(UserAdmin,self).__init__(Manage_user,db.session,endpoint="user_view",name="用户管理")

    def is_accessible(self):
        return current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.login",next=request.url))

    def create_model(self, form):
        try:
            model=self.model()
            form.populate_obj(model)
            model.set_password(model.password)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to create record. %(error)s', error=str(ex))
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, True)
        return model

    def update_model(self, form, model):
        try:
            form.populate_obj(model)
            if not("pbkdf2:sha1" in model.password):
                model.set_password(model.password)
            model.set_updatetime()

            self._on_model_change(form, model, False)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to update record. %(error)s', error=str(ex))

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, False)

        return True

#gitlab_分组
class GitLabAdmin(ModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_searchable_list = ["gitlab_name","gitlab_url"]
    column_labels = dict(gitlab_name="gitlab名称",gitlab_url="gitlab地址",gitlab_username="用户名",gitlab_password="密码",is_active="是否可用",create_time="创建时间",last_use_time="最后登录时间")
    form_args = {
        "gitlab_name":{
            "label":"gitlab名称",
            "validators":[required()]
        },
        "gitlab_url":{
            "label":"gitlab地址",
            "validators":[required()]
        },
        "gitlab_username":{
            "label":"用户名",
            "validators":[required()]
        },
        "gitlab_password":{
            "label":"密码",
            "validators":[required()]
        },
        "is_active":{
            "label":"是否可用",
            "validators":[required()]
        },

    }

    def is_accessible(self):
        return current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.login",next=request.url))

    def create_model(self, form):
        try:
            model=self.model()
            form.populate_obj(model)
            model.set_password(model.gitlab_password)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to create record. %(error)s', error=str(ex))
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, True)
        return model

    def update_model(self, form, model):
        try:
            form.populate_obj(model)
            if not("encrypt_" in model.gitlab_password):
                model.set_password(model.gitlab_password)
            self._on_model_change(form, model, False)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to update record. %(error)s', error=str(ex))
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, False)

        return True

    def __init__(self,session):
        from vzerGit.extensions import db
        from vzerGit.models.DBmodels import Gitlab_Group
        super(GitLabAdmin,self).__init__(Gitlab_Group,db.session,endpoint="gitlab_view",name="gitlab管理")
