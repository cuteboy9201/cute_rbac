#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-12 17:03:02
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 10:33:34
@Description: 
'''
from oslo.form.fields import (BoolField, EmailField, IntegerField, StringField,
                              StringListField)
from oslo.form.form import Form


class AuthLoginForm(Form):
    def __init__(self, handler=None):
        self.username = StringField(required=True)
        self.password = StringField(required=True)
        self.code = StringField(required=True)
        self.codekey = StringField(required=True)
        super(AuthLoginForm, self).__init__(handler)
