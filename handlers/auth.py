#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-12 12:38:15
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 09:51:41
@Description: 
'''
import logging

from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from tornado.gen import coroutine

from forms.auth import AuthLoginForm
from utils import auth
from utils.code import Captcha, get_captcha
from dblib.crud import User
LOG = logging.getLogger(__name__)


@route("/rbac/auth/login")
class AuthLogin(MixinRequestHandler):

    @coroutine
    def post(self):
        form = AuthLoginForm(self)
        if form.is_valid():
            username = form.value_dict["username"]
            password = form.value_dict["password"]
            code = form.value_dict["code"]
            codekey = form.value_dict["codekey"]
        else:
            LOG.error("req_data: %s, req_data: %s", self.request.path,
                      self.request_body())
            self.send_error(msg=form.error_dict)
            return

        check_code = auth.decode_md_code(codekey)
        if check_code:
            if check_code.lower() != code.lower():
                LOG.error("check_code: %s, code: %s", check_code, code)
                self.send_error(msg="验证码错误")
                return
        else:
            self.send_error(msg="验证码已过期, 请重新输入验证码")
            return
        password = auth.md5_password(username, password)
        user = User().getUserByNameAndPwd(username, password)
        if user:
            jwt_token = auth.create_token(user.id)
            data = {
                "id": user.id,
                "name": user.realName,
                "accessToken": jwt_token
            }
            self.send_ok(data=data)
            return
        else:
            self.send_error(msg="账号或者密码错误")
            return


@route("/rbac/image/(?P<code>.*)/")
class ImageHandler(MixinRequestHandler):

    @coroutine
    def get(self, code):
        code = auth.decode_md_code(code)
        if code:
            buf = Captcha.instance().generate(code)
            image = buf.getvalue()
            self.set_header("Content-Type", "image/png;charset=utf-8")
            self.write(image)
            buf.close()
            return
        else:
            return self.send_error(msg="验证码已经过期")


@route("/rbac/captcha/refresh")
class CaptchaHandler(MixinRequestHandler):
    def get(self):
        code = auth.get_captcha_text()
        md_code = auth.create_md_code(code)
        data = {"key": md_code, "image_url": "/rbac/image/{}/".format(md_code)}
        self.send_ok(data=data)
        return
