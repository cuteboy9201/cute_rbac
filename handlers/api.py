'''
@Author: your name
@Date: 2019-11-28 10:05:17
@LastEditTime: 2019-11-28 10:34:07
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /rbac/handlers/api.py
'''
import json 
import logging 

from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route 
from tornado.gen import coroutine
from utils.auth import get_user_info_bytoken,api_check_permission

LOG = logging.getLogger(__name__)

@route("/rbac/check_permission")
class checkPermissionHandler(MixinRequestHandler):

    @coroutine
    def post(self):
        req_data = self.request_body()
        check_path = req_data.get("check_path", [])
        check_auth = req_data.get("check_auth", [])
        if not check_auth or not check_path:
            self.send_fail(msg="没有权限")
            return
        auth_info = get_user_info_bytoken(check_auth)
        self.user_id = auth_info["userId"]
        if not self.user_id:
            self.send_fail(msg="没有权限")
            return 
        check_permission = api_check_permission(self, check_path)
        if check_permission:
            self.send_ok(data="")
            return
        self.send_fail(msg="没有权限")
        return 

    @coroutine
    def get(self):
        req_data = self.request_body()
        check_path = req_data.get("check_path", [])
        check_auth = req_data.get("check_auth", [])
        if not check_auth or not check_path:
            self.send_fail(msg="没有权限")
            return
        auth_info = get_user_info_bytoken(check_auth)
        self.user_id = auth_info["userId"]
        if not self.user_id:
            self.send_fail(msg="没有权限")
            return 
        check_permission = api_check_permission(self, check_path)
        if check_permission:
            self.send_ok(data="")
            return
        self.send_fail(msg="没有权限")
        return 