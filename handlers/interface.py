#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-08-30 09:47:44
@LastEditors: Youshumin
@LastEditTime: 2019-11-18 16:00:32
@Description: 
'''
import json
import logging
# from types import UnicodeType

from oslo.form.form import form_error
from oslo.util import dbObjFormatToJson
from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from tornado.gen import coroutine

from dblib.crud import FunctionInterface, Interface
from forms.interface import (interfaceBatchdelForm, interfacePageListForm,
                             interfaveSave, relateInterfaceForm)
from utils.auth import PermissionCheck, auth_middleware

LOG = logging.getLogger(__name__)

uuid_re = "(?P<id>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})"


@route('/rbac/interface/')
class InterfaceHandlers(MixinRequestHandler):
    @auth_middleware()
    @PermissionCheck
    @coroutine
    def get(self):
        form = interfacePageListForm(self)
        if form.is_valid():
            pageIndex = form.value_dict["pageIndex"]
            pageSize = form.value_dict["pageSize"]
            sortBy = form.value_dict["sortBy"]
            descending = form.value_dict["descending"]
            name = form.value_dict["name"]
            path = form.value_dict["path"]
            method = form.value_dict["method"]
            functionId = form.value_dict["functionId"]
            rule = {
                "name": name,
                "method": method,
                "path": path,
                "functionId": functionId
            }
        else:
            form_error(self, form)
        interfaceDB = Interface()
        code, totalCount, interfaceList = interfaceDB.getInterfacePagedList(
            pageIndex, pageSize, rule)
        ret = []
        if code:
            for item in interfaceList:
                ret_dict = dbObjFormatToJson(item)
                ret_dict.setdefault("description", ret_dict["desc"])
                ret.append(ret_dict)
            if sortBy and sortBy != "None" and ret:
                ret = sorted(ret, key=lambda x: x[sortBy], reverse=descending)
            if functionId:
                ret = sorted(ret, key=lambda x: x["isAdd"], reverse=False)
            data = dict(totalCount=totalCount, rows=ret)
        else:
            data = dict(totalCount=0, rows=ret)
        self.send_ok_json(data=data)
        return

    @auth_middleware()
    @PermissionCheck
    @coroutine
    def post(self):
        form = interfaveSave(self)
        if form.is_valid():
            desc = form.value_dict["description"]
            method = form.value_dict["method"]
            path = form.value_dict["path"]
            name = form.value_dict["name"]
            id = form.value_dict["id"]
        else:
            form_error(self, form)
        interface = Interface()
        LOG.debug("修改接口信息: {}".format((name, path, method, desc, id)))
        code, msg = interface.saveInterface(name, path, method, desc, id)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg=msg)
        return

    @auth_middleware()
    @PermissionCheck
    @coroutine
    def delete(self):
        form = interfaceBatchdelForm(self)
        if form.is_valid():
            ids = form.value_dict["ids"]
            if isinstance(ids, str):
                ids = json.loads(ids)
        else:
            form_error(self, form)
        all_num = len(ids)
        delete_num = 0
        fail_num = 0
        fail_ids = []
        funcrioninterface = FunctionInterface()
        interface = Interface()
        for id in ids:
            check_data = funcrioninterface.getFunctionInterfaceByFunction(id)
            if check_data:
                fail_num += 1
                fail_ids.append(id)
            else:
                reponse = interface.delById(id)
                if reponse:
                    delete_num += 1
                else:
                    fail_num += 1
                    fail_ids.append(id)
        data = {
            "ok_num": delete_num,
            "all_num": all_num,
            "err_num": fail_num,
            "err_ids": fail_ids
        }
        self.send_ok_json(data=data)
        return


@route("/rbac/interface/{}/".format(uuid_re))
class InterfaceByIDHandlers(MixinRequestHandler):
    @auth_middleware()
    @PermissionCheck
    @coroutine
    def get(self, id):
        interface = Interface()
        get_info = interface.getById(id)
        if get_info:
            data = dict(name=get_info.name,
                        id=get_info.id,
                        path=get_info.path,
                        description=get_info.desc,
                        method=get_info.method)
            self.send_ok_json(data=data)
        else:
            self.send_fail_json(msg="接口信息不存在")
        return

    @auth_middleware()
    @PermissionCheck
    @coroutine
    def delete(self, id):
        interface = Interface()
        interfacefunction = FunctionInterface()
        check_data = interfacefunction.getFunctionInterfaceByFunction(id)
        if check_data:
            self.send_fail_json(msg="请先解除接口绑定的权限")
            return
        del_info = interface.delById(id)
        if del_info:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg="删除失败")
        return


@route("/rbac/interface/relate/")
class InterfaceRelateHandler(MixinRequestHandler):
    @auth_middleware()
    @PermissionCheck
    @coroutine
    def post(self):
        '''
        @description:  添加或者删除 接口和角色绑定
        @param {type} 
        @return: 
        '''
        form = relateInterfaceForm(self)
        if form.is_valid():
            action = form.value_dict["action"]
            functionId = form.value_dict["functionId"]
            interfaceId = form.value_dict["interfaceId"]
        else:
            form_error(self, form)

        DB = FunctionInterface()
        code = DB.saveFunctionInterface(action, functionId, interfaceId)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg="")
        return
