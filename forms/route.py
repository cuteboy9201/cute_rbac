#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-13 10:57:07
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 10:57:20
@Description: 
'''

from oslo.form.fields import (BoolField, EmailField, IntegerField, StringField,
                              StringListField)
from oslo.form.form import Form


class routeSaveForm(Form):
    def __init__(self, handler):
        self.id = StringField(required=False)
        self.parentId = StringField(required=True)
        self.title = StringField(required=True)
        self.component = StringField(required=False)
        self.componentPath = StringField(required=False)
        self.path = StringField(required=True)
        self.permission = StringField(required=False)
        self.sort = IntegerField(required=True)
        self.isLock = BoolField(required=False)
        self.cache = BoolField(required=False)
        self.name = StringField(required=True)
        return super(routeSaveForm, self).__init__(handler=handler)
