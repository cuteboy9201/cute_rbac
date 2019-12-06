'''
@Author: your name
@Date: 2019-11-28 10:05:17
@LastEditTime: 2019-11-29 11:00:16
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /rbac/handlers/api.py
'''
import json
import logging

from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from tornado.gen import coroutine

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
            self.send_fail(msg="没有权限")
            return
        code, auth_info = get_user_info_bytoken(check_auth)
        LOG.debug("get_user_info_bytoken: {} {}".format(code, auth_info))

        if not code:
            self.send_fail(msg="没有权限")
            return

        try:
            LOG.debug("jwt解密信息为: %s", auth_info)
            # auth_info = json.loads(auth_info)
            self.user_id = auth_info["userId"]
        except Exception as e:
            LOG.error(str(e))
            self.send_fail(msg="没有权限")
            return

        if not self.user_id:
            self.send_fail(msg="没有权限")
            return
            
        check_permission = api_check_permission(self, check_path, check_method)

        if check_permission:
            self.send_ok(data="")
            return
        self.send_fail(msg="没有权限")
        return
