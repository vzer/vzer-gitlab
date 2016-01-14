#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

__all__=["db","lm","admin","mail"]
db=SQLAlchemy()
lm=LoginManager()
admin=Admin(name="Vzer.gitlab",template_mode="bootstrap3")
mail=Mail()
