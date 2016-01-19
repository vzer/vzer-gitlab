#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from sqlalchemy import or_
from DBmodels import Manage_user
from vzerGit.extensions import db

class Data_Wrappers(object):

    #根据id获取用户
    def get_user_byid(self,user_id):
        return Manage_user.query.get(user_id)
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