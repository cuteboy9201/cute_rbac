#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-08-29 14:22:20
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 10:32:31
@Description:
'''

import logging

from oslo.form.form import form_error
from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from tornado.gen import coroutine

from dblib.crud import FunctionInterface, Menu, RoleFunction
from forms.menu import menuSaveForm
from utils.auth import PermissionCheck, auth_middleware
from utils.serialize import buildchildren, formatMenus

LOG = logging.getLogger(__name__)
uuid_re = "(?P<id>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})"


@route("/rbac/menu")
class MenuHandlers(MixinRequestHandler):
    @auth_middleware()
    @PermissionCheck
    @coroutine
    def get(self):
        '''
        @description:  获取全部菜单信息
        @param {type}
        @return:
        '''
        menu = Menu()
        menuList = menu.getMenuAllList()
        menuParentList = menu.getParentMenu()
        if menuList and menuParentList:
            for p_menu in menuParentList:
                buildchildren(p_menu, menuList)
            menuList = formatMenus(menuParentList)
            self.send_ok_json(data=menuList)
        else:
            self.send_fail_json(msg="获取菜单列表失败")
        return

    @auth_middleware()
    @PermissionCheck
    @coroutine
    def post(self):
        form = menuSaveForm(self)
        if form.is_valid():
            id = form.value_dict["id"]
            parentId = form.value_dict["parentId"]
            title = form.value_dict["title"]
            _type = form.value_dict["type"]
            path = form.value_dict["path"]
            icon = form.value_dict["icon"]
            permission = form.value_dict["permission"]
            sort = form.value_dict["sort"]
            isLock = True if form.value_dict["isLock"] else False
        else:
            form_error(self, form)
        if _type == 1:
            if not path:
                self.send_fail_json(msg="路径不能为空")
                return
        menu = Menu()
        code, msg = menu.saveMenu(parentId, title, icon, sort, _type, isLock,
                                  "", permission, path, id)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg=msg)
        return


@route(r"/rbac/menu/{}".format(uuid_re))
class MenuByIDHandlers(MixinRequestHandler):
    @auth_middleware()
    @PermissionCheck
    @coroutine
    def get(self, id):
        menu = Menu()
        menuDB = menu.getMenuById(id)
        if menuDB:
            data = {
                "id": menuDB.id,
                "parentId": menuDB.parentId,
                "title": menuDB.title,
                "path": menuDB.path,
                "icon": menuDB.icon,
                "type": menuDB.type,
                "permission": menuDB.permission,
                "sort": menuDB.sort
            }
            self.send_ok_json(data=data)
        else:
            self.send_fail_json(msg="获取菜单信息失败")
        return

    @auth_middleware()
    @PermissionCheck
    @coroutine
    def delete(self, id):
        rolefunction = RoleFunction()
        check_rolefunction = rolefunction.getRoleFunctionByMenuId(id)
        if check_rolefunction:
            self.send_fail_json(msg="请先解除相关角色权限绑定")
            return
        functioninterface = FunctionInterface()
        check_functioninterface = functioninterface.getFunctionInterfaceByFunction(
            id)
        if check_functioninterface:
            self.send_fail_json(msg="请先解除菜单绑定的接口信息")
            return
        menu = Menu()
        code = menu.delMenu(id)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg="删除失败")
        return


@route("/rbac/menu/1/")
class MenuGetType1Handler(MixinRequestHandler):
    @auth_middleware()
    @coroutine
    def get(self):
        menu = Menu()
        info = menu.getMenuList()
        ret = []
        for item in info:
            data = dict(value=item.path)
            ret.append(data)
        return self.send_ok_json(data=ret)
