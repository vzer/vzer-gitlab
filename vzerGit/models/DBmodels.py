#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from vzerGit.extensions import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
import base64

#后台用户认证
class Manage_user(db.Model,UserMixin):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="manage_user"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True,unique=True,doc="表主键id")
    username=db.Column(db.String(50),unique=True,doc="用户名")
    password=db.Column(db.String(100),doc="密码")
    email=db.Column(db.String(100),doc="email地址")
    nickname=db.Column(db.String(100),doc="真实姓名")
    isactive=db.Column(db.Boolean,default=False,doc="是否激活")
    isadmin=db.Column(db.Boolean,default=False,doc="是否管理员")
    pending=db.Column(db.Boolean,default=False,doc="审核状态")
    createtime=db.Column(db.DateTime,default=db.func.now(),doc="创建时间")
    updatetime=db.Column(db.DateTime,doc="跟新时间")
    logintime=db.Column(db.DateTime,doc="登录时间")

    def __init__(self,username=None,password=None,email=None,nickname=None,isactive=False,isadmin=False,updatetime=None,pending=False):
        self.username=username
        self.set_password(password=str(password))
        self.email=email
        self.nickname=nickname
        self.isactive=isactive
        self.isadmin=isadmin
        self.updatetime=updatetime
        self.pending=pending

    def set_password(self,password):
        self.password=generate_password_hash(password=password)

    def check_password(self,password):
        return check_password_hash(self.password,password=password)

    def set_logintime(self,logintime):
        self.logintime=logintime

    def get_logtime(self):
        return self.logintime

    def set_updatetime(self):
        self.updatetime=db.func.now()

    def get_updatetime(self):
        return self.updatetime

    def is_active(self):
        if self.isactive and self.pending:
            return True
        else:
            return False

    def is_admin(self):
        if self.isadmin:
            return True
        else:
            return False


    def is_authenticated(self):
        return True


    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


    def __repr__(self):
        return "<User '{:s}'> ".format(self.nick_name)


#gitlab分组
class Gitlab_Group(db.Model):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="gitlab_group"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True,doc="表主键id")
    gitlab_name=db.Column(db.String(100),doc="gitlab名称")
    gitlab_url=db.Column(db.String(200),doc="gitlab地址")
    gitlab_username=db.Column(db.String(100),doc="gitlab管理账户")
    gitlab_password=db.Column(db.String(100),doc="gitlab管理密码")
    is_active=db.Column(db.Boolean,default=False,doc="是否启用")
    create_time=db.Column(db.DateTime,default=db.func.now(),doc="时间时间")
    last_use_time=db.Column(db.DateTime,doc="最后登录时间")

    def __init__(self,gitlab_name=None,gitlab_url=None,gitlab_username=None,gitlab_password=None,is_avtice=False):
        self.gitlab_name=gitlab_name
        self.gitlab_url=gitlab_url
        self.gitlab_username=gitlab_username
        self.set_password(passowrd=str(gitlab_password))
        self.is_active=is_avtice

    def set_password(self,passowrd):
        encrypt_world=base64.encodestring(passowrd)
        self.gitlab_password="encrypt_"+encrypt_world

    def get_password(self):
        return base64.decodestring(self.gitlab_password[8:])

    def __repr__(self):
        return "GitLab Name:%s"%self.gitlab_name

#gitlab_user
class Gitlab_user(db.Model):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="gitlab_user"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True,doc="表用户id")
    gitlab_group_id=db.Column(db.INTEGER,db.ForeignKey("gitlab_group.id"),doc="所属gitlab id")
    gitlab_id=db.Column(db.INTEGER,default=None,doc="gitlab中id")
    username=db.Column(db.String(100),doc="登录名")
    password=db.Column(db.String(100),doc="gitlab账户密码")
    name=db.Column(db.String(100),doc="用户名")
    email=db.Column(db.String(200),doc="email地址")
    can_create_project=db.Column(db.Boolean,default=False,doc="能否创建工程")
    can_create_group=db.Column(db.Boolean,default=False,doc="能否创建组")
    web_url=db.Column(db.String(200),doc="个人web地址")
    projects_limit=db.Column(db.INTEGER,default=None,doc="能创建工程数量")
    current_sign_in_at=db.Column(db.DateTime,doc="最后登录时间")
    state=db.Column(db.String(100),doc="状态")
    is_admin=db.Column(db.Boolean,default=False,doc="是否是管理员")
    created_at=db.Column(db.DateTime,doc="创建时间")

    def set_password(self,passowrd):
        self.password=generate_password_hash(password=passowrd)

    def check_password(self,password):
        return check_password_hash(self.password,password=password)

    def __repr__(self):
        return "GitLab User:%s"%self.name

#gitlab_projects
class Gitlab_projects(db.Model):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="gitlab_projects"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True,doc="表项目id")
    gitlab_group_id=db.Column(db.INTEGER,db.ForeignKey("gitlab_group.id"),doc="所属gitlab id")
    gitlab_id=db.Column(db.INTEGER,default=None,doc="gitlab中id")
    project_name=db.Column(db.String(200),doc="工程名称")
    project_web_url=db.Column(db.String(300),doc="工程web地址")
    project_http_url_to_repo=db.Column(db.String(300),doc="工程仓库web地址")
    project_wiki_enabled=db.Column(db.Boolean,default=True,doc="是否启用wiki")
    project_merge_requests_enabled=db.Column(db.Boolean,default=True,doc="是否启用merge请求")
    created_at=db.Column(db.DateTime,default=db.func.now(),doc="创建时间")
    updated_at=db.Column(db.DateTime,doc="创建时间")
    description=db.Column(db.Text,doc="工程描述")