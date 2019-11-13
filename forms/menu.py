#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-13 10:08:33
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 10:31:42
@Description: 
'''
from oslo.form.fields import BoolField, EmailField, IntegerField, StringField, StringListField
from oslo.form.form import Form


class menuSaveForm(Form):
    def __init__(self, handler=None):
        self.id = StringField(required=False)
        self.parentId = StringField(required=True)
        self.title = StringField(required=True)
        self.type = IntegerField(required=True)
        self.path = StringField(required=False)
        self.icon = StringField(required=False)
        self.permission = StringField(required=False)
        self.sort = IntegerField(required=True)
        self.isLock = BoolField(required=False)
        return super(menuSaveForm, self).__init__(handler=handler)
