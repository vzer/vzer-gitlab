#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from sqlalchemy import or_
from DBmodels import Manage_user,Gitlab_user
from vzerGit.extensions import db
import gitlab
from gitlab import exceptions

class Data_Wrappers(object):

    #根据后台管理id获取用户
    def get_user_byid(self,user_id):
        return Manage_user.query.get(user_id)
    #根据gitlab用户id获取用户
    def get_gitlabuser_byid(self,user_id):
        return Gitlab_user.query.get(user_id)
    #根据用户名获取用户
    def get_user_byname(self,username):
        return Manage_user.query.filter(Manage_user.username==username).first()
    #检查用户是否存在
    def check_user(self,account):
        user=Manage_user.query.filter(Manage_user.username==account).all()
        if user:
            return True
        else:
            return False
     #添加用户
    def insert_user(self,account=None,nickname=None,email=None,password=None):
        user=Manage_user(username=account,password=password,email=email,nickname=nickname)
        flag=self.check_user(account)
        if not flag:
            db.session.add(user)
            try:
               db.session.commit()
               return True
            except Exception:
                db.session.rollback()
        else:
            return False


    #检查gitlab用户能否登录
    def check_gitlab_login(self,username,password,gitlaburl):
        git=gitlab.Gitlab(host=gitlaburl)
        try:
            git.login(email=username,password=password)
            gituser=git.currentuser()
            return (True,gituser)
        except exceptions.HttpError,msg:
            return (False,msg)

    def get_key(self,key,dicts):
        if key in dicts.keys():
            return dicts[key]

    #insert/update用户信息
    def update_gitlab_user(self,gitlab_user=None,gitlab_group_id=None,password=None):
        try:
            user=Gitlab_user.query.filter(Gitlab_user.gitlab_group_id==gitlab_group_id,Gitlab_user.username==gitlab_user["username"]).update({Gitlab_user.password:password},synchronize_session=False)
            if not user:
                user=Gitlab_user(gitlab_group_id=gitlab_group_id,gitlab_id=gitlab_user["id"],username=gitlab_user["username"],password=password,name=gitlab_user["name"],email=gitlab_user["email"],\
                                        can_create_project=gitlab_user["can_create_project"],can_create_group=gitlab_user["can_create_group"],web_url=self.get_key("web_url",gitlab_user),projects_limit=self.get_key("projects_limit",gitlab_user),
                                        current_sign_in_at=self.get_key("current_sign_in_at",gitlab_user),state=gitlab_user["state"],is_admin=gitlab_user["is_admin"],created_at=gitlab_user["created_at"])
                db.session.merge(user)
            db.session.commit()
            return Gitlab_user.query.filter(Gitlab_user.gitlab_group_id==gitlab_group_id,Gitlab_user.username==gitlab_user["username"]).first()
        except Exception:
            db.session.rollback()
            return False
