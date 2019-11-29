#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-13 10:51:22
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 10:52:07
@Description: 
'''
from oslo.form.fields import (BoolField, EmailField, IntegerField, StringField,
                              StringListField)
from oslo.form.form import Form


class roleDelFrom(Form):
    def __init__(self, handler=None):
        self.id = StringField()
        return super(roleDelFrom, self).__init__(handler=handler)


class rolePageListForm(Form):
    def __init__(self, handler=None):
        self.pageIndex = IntegerField(required=True)
        self.pageSize = IntegerField(required=True)
        self.sortBy = StringField(required=False)
        self.descending = BoolField(required=True)
        self.filter = StringField(required=False)
        return super(rolePageListForm, self).__init__(handler=handler)


class roleSaveForm(Form):
    def __init__(self, handler=None):
        self.code = StringField(required=True)
        self.name = StringField(required=True)
        self.description = StringField(required=True)
        self.id = StringField(required=False)
        return super(roleSaveForm, self).__init__(handler=handler)


class BatchdelForm(Form):
    def __init__(self, handler=None):
        self.ids = StringListField(required=False)
        return super(BatchdelForm, self).__init__(handler=handler)


class savePermissionForm(Form):
    def __init__(self, handler=None):
        self.roleId = StringField()
        self.permissions = StringListField(required=False)
        return super(savePermissionForm, self).__init__(handler=handler)
