#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
import gitlab
GITLAB_URL='http://192.168.3.100'
MANAGE_USERNAME='xiniunet'
MANAGE_PASSWD='root@xiniu'

git=gitlab.Gitlab(GITLAB_URL)
git.login(MANAGE_USERNAME,MANAGE_PASSWD)

class manage_gitlab(object):
    def create_user(self):
        pass

projects=git.getprojectsall()
for pro in projects:
    print pro

