#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-13 10:42:53
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 10:43:39
@Description:
'''
from oslo.form.fields import BoolField, EmailField, IntegerField, StringField
from oslo.form.form import Form


class RetPassForm(Form):
    def __init__(self, handler=None):
        self.name = StringField(required=True)
        self.repassword = StringField(required=True, key=True)
        self.newpassword = StringField(required=True, key=True)
        self.oldpassword = StringField(required=True, key=True)
        super(RetPassForm, self).__init__(handler)


class userSaveForm(Form):
    def __init__(self, handler=None):
        self.email = EmailField(required=True)
        self.name = StringField(required=True)
        self.phone = IntegerField(required=True)
        self.trueName = StringField(required=True)
        self.password = StringField(required=False, key=True)
        self.repassword = StringField(required=False, key=True)
        self.id = StringField(required=False)
        return super(userSaveForm, self).__init__(handler=handler)


class userPageListForm(Form):
    def __init__(self, handler=None):
        self.pageIndex = IntegerField(required=True)
        self.pageSize = IntegerField(required=True)
        self.sortBy = StringField(required=False)
        self.descending = BoolField(required=True)
        self.filter = StringField(required=False)
        return super(userPageListForm, self).__init__(handler=handler)


class userEditRoleUserForm(Form):
    def __init__(self, handler=None):
        self.action = IntegerField(required=True)
        self.roleId = StringField(required=True)
        self.userId = StringField(required=True)
        return super(userEditRoleUserForm, self).__init__(handler=handler)


class roleDelFrom(Form):
    def __init__(self, handler=None):
        self.id = StringField()
        return super(roleDelFrom, self).__init__(handler=handler)
