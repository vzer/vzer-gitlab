#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask_script import Manager,Server,prompt,prompt_pass,prompt_bool
from applications import create_app
from vzerGit.models.DBmodels import Manage_user
from vzerGit.extensions import db
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

server=Server(host="0.0.0.0",port=5001)
app=create_app()
manager=Manager(app)

@manager.option('-u', '--username', dest="username", required=False)
@manager.option('-p', '--password', dest="password", required=False)
@manager.option('-e', '--email', dest="email", required=False)
@manager.option('-n', '--nickname', dest="nickname", required=False)
def createuser(username=None, password=None, email=None,nickname=None,isactive=True,isadmin=True,updatetime=db.func.now()):
    """
    Create a new user
    """

    if username is None:
        while True:
            username = prompt("Username")
            user = Manage_user.query.filter(Manage_user.username == username).first()
            if user is not None:
                print "Username %s is already taken" % username
            else:
                break

    if email is None:
        while True:
            email = prompt("Email address")
            user = Manage_user.query.filter(Manage_user.email == email).first()
            if user is not None:
                print "Email %s is already taken" % email
            else:
                break

    if password is None:
        password = prompt_pass("Password")

        while True:
            password_again = prompt_pass("Password again")
            if password != password_again:
                print "Passwords do not match"
            else:
                break

    if nickname is None:
        nickname = prompt("Nick name")

    user = Manage_user(username=username,password=password,email=email,nickname=nickname,isactive=isactive,isadmin=isadmin,updatetime=updatetime)

    db.session.add(user)
    db.session.commit()

    print "User created with ID", user.id

@manager.command
def createall():
    "Creates database tables"

    db.create_all()

@manager.command
def dropall():
    "Drops all database tables"

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

manager.add_command("runserver", server)
if __name__ == '__main__':
    manager.run()
