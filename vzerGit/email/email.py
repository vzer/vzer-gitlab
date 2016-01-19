#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

from flask import render_template,current_app
from flask_mail import Message
from vzerGit.extensions import mail
from threading import Thread


def async(func):
    def wrapper(*args,**kwargs):
        thr=Thread(target=func,args=args,kwargs=kwargs)
        thr.start()
    return wrapper

@async
def send_async_mail(msg):
    from manage import app
    with app.app_context():
        mail.send(msg)


def send_mail(subject,sender,recipients,html_body):
    msg=Message(subject,recipients=recipients,sender=sender)
    msg.html=html_body
    send_async_mail(msg)



def input_link_mail(contact,webname,weburl,webtip):
    send_mail(subject="[vzer.zhang]:友情链接提醒",sender=current_app.config.get("DEFAULT_MAIL_SENDER"),\
              recipients=current_app.config.get("ADMINS"),html_body=render_template("mail/email_inputlink.html",contact=contact,webname=webname,weburl=weburl,webtip=webtip))

#后台审核邮件通知
def admin_regegit_mail(nickname,email):
    send_mail(subject="[vzer.zhang]:友情链接提醒",sender=current_app.config.get("DEFAULT_MAIL_SENDER"),\
              recipients=email,html_body=render_template("mail/admin_regegit.html",nickname=nickname))

