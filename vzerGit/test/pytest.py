#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

import gitlab

git=gitlab.Gitlab(host="http://192.168.20.100")
git.login(email="test",password="wwwlin123")
print git.currentuser()

'''
for user in git.getusers():
    print user
    #print user["id"],user["username"],user["name"],user["email"],user["can_create_project"],user["can_create_group"],user["web_url"],user["projects_limit"],user["current_sign_in_at"],user["state"],user["is_admin"],user["created_at"]
'''

