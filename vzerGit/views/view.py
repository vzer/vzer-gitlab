#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask import render_template,request,flash,Module,current_app,session

gitmanage=Module(__name__)
#index
@gitmanage.route("/")
def index():
    return render_template("index.html")