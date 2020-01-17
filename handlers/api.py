#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: YouShumin
@Date: 2020-01-17 16:49:00
@LastEditTime: 2020-01-17 17:18:49
@LastEditors: YouShumin
@Description: 
@FilePath: /cute_rbac/handlers/api.py
'''
import json
import logging

from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from tornado.gen import coroutine
from dblib.crud import User, Role
from utils.auth import api_check_permission, get_user_info_bytoken

LOG = logging.getLogger(__name__)


@route("/rbac/check_permission")
class checkPermissionHandler(MixinRequestHandler):
    @coroutine
    def post(self):
        req_data = self.request_body()
        check_path = req_data.get("check_path", [])
        check_auth = req_data.get("check_auth", [])
        check_method = req_data.get("check_method", [])
        if not check_auth or not check_path or not check_method:
            self.send_fail(msg=u"没有权限")
            return
        code, auth_info = get_user_info_bytoken(check_auth)
        LOG.debug("get_user_info_bytoken: {} {}".format(code, auth_info))

        if not code:
            self.send_fail(msg=u"没有权限")
            return

        try:
            LOG.debug(u"jwt解密信息为: %s", auth_info)
            # auth_info = json.loads(auth_info)
            self.user_id = auth_info["userId"]
        except Exception as e:
            LOG.error(str(e))
            self.send_fail(msg=u"没有权限")
            return

        if not self.user_id:
            self.send_fail(msg=u"没有权限")
            return

        check_permission = api_check_permission(self, check_path, check_method)

        if check_permission:
            self.send_ok(data="")
            return
        self.send_fail(msg=u"没有权限")
        return


@route("/rbac/select/")
class rbacSelectHandler(MixinRequestHandler):
    @coroutine
    def get(self):
        db_info = []
        req_data = self.request_body()
        msg_id = req_data.get("msg_id", None)
        if msg_id == "role":
            role = Role()
            db_info = role.getAllByKeyValue("isLock", 0)
        elif msg_id == "user":
            user = User()
            db_info = user.getAllByKeyValue("isLock", 0)
        else:
            return self.send_fail(msg="")
        ret_info = []
        for item in db_info:
            ret_info.append(dict(id=item.id, value=item.name))
        self.send_ok(data=ret_info)
        return