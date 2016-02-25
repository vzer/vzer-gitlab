#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from vzerGit.adminview.admin import MyAdminIndexView
from vzerGit.adminview.adminview import UserAdmin,GitLabAdmin,GitLab_User_Admin

__all__=["db","lm","admin","mail"]
db=SQLAlchemy()
lm=LoginManager()
admin=Admin(name="Vzer.gitlab",index_view=MyAdminIndexView(),base_template="admins/master.html",template_mode="bootstrap3")
admin.add_view(UserAdmin(db.session))
admin.add_view(GitLabAdmin(db.session))
admin.add_view(GitLab_User_Admin(db.session))
mail=Mail()
