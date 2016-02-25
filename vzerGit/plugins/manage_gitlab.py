#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
import gitlab
from gitlab import exceptions
import logging
from threading import Thread
from flask import flash


class data_gitlab_wrapper(object):
    git=None
    gitlab_url=None
    username=None
    password=None
    def __init__(self,gitlab_url=None,username=None,password=None):
        self.gitlab_url=gitlab_url
        self.username=username
        self.password=password
        try:
            self.git=gitlab.Gitlab(host=self.gitlab_url)
            print "current git is",self.git
            self.git.login(email=self.username,password=self.password)
        except exceptions.HttpError,msg:
            logging.error(msg)
            flash(msg)
            #return False

    def get_key(self,key,dicts):
        if key in dicts.keys():
            return dicts[key]


    def async(func):
        def wrapper(*args,**kwargs):
            thr=Thread(target=func,args=args,kwargs=kwargs)
            thr.start()
        return wrapper

    @async
    def get_all_users(self,gitlab_group_id=None):
        from vzerGit.models.DBmodels import Gitlab_user
        from vzerGit.extensions import db
        users=self.git.getall(self.git.getusers)
        from manage import app
        with app.app_context():
            for user in users:
                gitlab_user=Gitlab_user(gitlab_group_id=gitlab_group_id,gitlab_id=user["id"],username=user["username"],name=user["name"],email=user["email"],\
                                        can_create_project=user["can_create_project"],can_create_group=user["can_create_group"],web_url=self.get_key("web_url",user),projects_limit=self.get_key("projects_limit",user),
                                        current_sign_in_at=self.get_key("current_sign_in_at",user),state=user["state"],is_admin=user["is_admin"],created_at=user["created_at"])
                db.session.add(gitlab_user)
            try:
                db.session.commit()
                return True
            except:
                db.session.rollback()
                return False

