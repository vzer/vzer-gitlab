#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask import render_template,request,flash,Module,current_app,session,redirect,url_for
from flask_login import current_user,login_user
from vzerGit.froms.forms import GitlabUserLogin,GitlabRegeditForm
from vzerGit.models.data_wrappers import Data_Wrappers
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
wrapper=Data_Wrappers()
user=Module(__name__)

#index
@user.route("/")
def index():
    return render_template("gitlab_user/index.html")
#login
@user.route("/login",methods=["GET","POST"])
def gitlab_user_login():
    from vzerGit.models.DBmodels import Gitlab_Group
    form=GitlabUserLogin(request.form)
    form.loginFrom.choices=[(g.id,g.gitlab_name) for g in Gitlab_Group.query.all() ]
    if current_user.is_authenticated():
        return redirect(url_for("index"))
    if form.validate_on_submit():
        username=form.loginName.data
        password=form.loginPassword.data
        gitlab_id=form.loginFrom.data
        gitlaburl=Gitlab_Group.query.filter(Gitlab_Group.id==gitlab_id).first().gitlab_url
        (status,gituser)=wrapper.check_gitlab_login(username=username,password=password,gitlaburl=gitlaburl)
        if status:
            currentuser=wrapper.update_gitlab_user(gitlab_user=gituser,gitlab_group_id=gitlab_id,password=password)
            if currentuser:
                if currentuser.is_active():
                    login_user(currentuser)
                    flash("欢迎登录gitlab管理系统,%s"%current_user.name)
                    next=request.args.get("next")
                    return  redirect(next or url_for("index"))
        else:
            flash("ERROR：%s"%gituser)

    return render_template("gitlab_user/login.html",form=form)

#regedit
@user.route("/regedit",methods=["GET","POST"])
def gitlab_user_regedit():
    from vzerGit.models.DBmodels import Gitlab_Group
    form=GitlabRegeditForm(request.form)
    form.loginFrom.choices=[(g.id,g.gitlab_name) for g in Gitlab_Group.query.all()]

    return render_template("gitlab_user/regedit.html",form=form)

