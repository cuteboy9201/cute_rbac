#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-08-29 09:48:41
@LastEditors: Youshumin
@LastEditTime: 2019-11-14 16:39:13
@Description: 
'''
import json
import logging
# from types import UnicodeType

from tornado import gen

from forms.role import (BatchdelForm, roleDelFrom, rolePageListForm,
                        roleSaveForm, savePermissionForm)
from dblib import crud as crudmixin
from utils.serialize import buildRolePagesList
from utils.auth import PermissionCheck, auth_middleware
from oslo.util import dbObjFormatToJson
from oslo.form.form import form_error
from oslo.web.route import route
from oslo.web.requesthandler import MixinRequestHandler

LOG = logging.getLogger(__name__)

uuid_re = "(?P<id>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})"


@route(r"/rbac/role/")
class RoleHandlers(MixinRequestHandler):
    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def get(self):
        '''
        @description: 获取角色列表
        @param
        @return: 
        '''
        form = rolePageListForm(self)
        if form.is_valid():
            pageIndex = form.value_dict["pageIndex"]
            pageSize = form.value_dict["pageSize"]
            sortBy = form.value_dict["sortBy"]
            descending = form.value_dict["descending"]
            rules = form.value_dict["filter"]
            if rules:
                import json
                rules = json.loads(rules)
            else:
                rules = {}
        else:
            LOG.error("req_path: %s, req_data: %s", self.request.path,
                      self.from_data())
            self.send_fail_json(msg=form.error_dict)
            return
        role = crudmixin.Role()
        code, totalCount, roleList = role.getRolePagedList(
            pageIndex, pageSize, rules)
        data = buildRolePagesList(totalCount, roleList, sortBy, rules,
                                  descending)
        self.send_ok_json(data=data)
        return

    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def delete(self):
        '''
        @description: 删除角色信息
        @param {type} 
        @return: 
        '''
        form = roleDelFrom(self)
        if form.is_valid():
            id = form.value_dict["id"]
        else:
            LOG.error("req_path: %s, req_data: %s", self.request.path,
                      self.from_data())
            self.send_fail_json(msg=form.error_dict)
            return
        roleuser = crudmixin.RoleUser()
        check_role_info = roleuser.getUserIds(id)
        if check_role_info:
            self.send_fail_json(msg="请先解除绑定用户关系")
            return
        role = crudmixin.Role()
        code = role.delRole(id)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg="删除角色信息失败")
        return

    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def post(self):
        '''
        @description: 保存修改角色信息
        @param {type} 
        @return: 
        '''
        form = roleSaveForm(self)
        if form.is_valid():
            code = form.value_dict["code"]
            name = form.value_dict["name"]
            desc = form.value_dict["description"]
            id = form.value_dict["id"]
        else:
            form_error(self, form)
        role = crudmixin.Role()
        code, _ = role.saveRole(name, code, desc, id=id)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg="")
        return


@route("/rbac/role/{}".format(uuid_re))
class RoleGetByIdHandler(MixinRequestHandler):
    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def get(self, id):
        role = crudmixin.Role()
        roleDB = role.getRoleById(id)
        if roleDB:
            data = dict(name=roleDB.name,
                        code=roleDB.code,
                        description=roleDB.desc,
                        id=roleDB.id)
            self.send_ok_json(data=data)
        else:
            self.send_fail_json(msg="角色信息不存在")
        return


@route("/rbac/role/batchdel")
class RoleBatchDelHandler(MixinRequestHandler):
    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def delete(self):
        form = BatchdelForm(self)
        if form.is_valid():
            ids = form.value_dict["ids"]
        else:
            form_error(self, form)
        if isinstance(ids, str):
            ids = json.loads(ids)
        role = crudmixin.Role()
        for id in ids:
            role.delRole(id)
        return self.send_ok_json(data="")


@route("/rbac/role/permissions/{}".format(uuid_re))
class RolePermissionGetHandler(MixinRequestHandler):
    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def get(self, id):
        ret_data = []
        rolefunctionDB = crudmixin.RoleFunction()
        rolefunction = rolefunctionDB.getRoleFunctionByRoleId(id)
        if rolefunction:
            ret_data = [
                dbObjFormatToJson(item,
                                  field_to_expand=["menuId", "roleId", "id"])
                for item in rolefunction
            ]

        # bug 由于创建数据的字段对应关系导致2019.08.30发现 后期修改
        for ret in ret_data:
            ret["functionId"] = ret["menuId"]
        self.send_ok_json(data=ret_data)
        return


@route("/rbac/role/savepermission/")
class RolePermissionSaveHanlder(MixinRequestHandler):
    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def post(self):

        form = savePermissionForm(self)
        if form.is_valid():
            rid = form.value_dict["roleId"]
            permission = form.value_dict["permissions"]
        else:
            form_error(self, form)
        rolefunction = crudmixin.RoleFunction()
        code, msg = rolefunction.saveRoleFunction(rid, permission)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg=msg)
        return
