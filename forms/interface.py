#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-13 09:52:42
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 10:31:51
@Description: 
'''
from oslo.form.fields import BoolField, EmailField, IntegerField, StringField, StringListField
from oslo.form.form import Form


class interfacePageListForm(Form):
    def __init__(self, handler=None):
        self.pageIndex = IntegerField(required=True)
        self.pageSize = IntegerField(required=True)
        self.sortBy = StringField(required=False)
        self.descending = BoolField(required=True)
        self.name = StringField(required=False)
        self.path = StringField(required=False)
        self.method = StringField(required=False)
        self.functionId = StringField(required=False)
        return super(interfacePageListForm, self).__init__(handler=handler)


class interfaveSave(Form):
    def __init__(self, handler=None):
        self.description = StringField(required=False)
        self.method = StringField()
        self.name = StringField()
        self.path = StringField()
        self.id = StringField(required=False)
        return super(interfaveSave, self).__init__(handler=handler)


class interfaceBatchdelForm(Form):
    def __init__(self, handler=None):
        self.ids = StringListField(required=False)
        return super(interfaceBatchdelForm, self).__init__(handler=handler)


class relateInterfaceForm(Form):
    def __init__(self, handler=None):
        self.functionId = StringField()
        self.interfaceId = StringField()
        self.action = IntegerField()
        return super(relateInterfaceForm, self).__init__(handler=handler)
