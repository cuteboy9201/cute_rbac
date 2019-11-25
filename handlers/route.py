#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-08-29 16:27:13
@LastEditors: Youshumin
@LastEditTime: 2019-11-14 16:09:16
@Description:
'''

import logging

from tornado.gen import coroutine

from forms.route import routeSaveForm

from dblib.crud import Route
from utils.serialize import buildchildren, formatRoutes
from utils.auth import PermissionCheck, auth_middleware
from oslo.web.route import route
from oslo.form.form import form_error
from oslo.web.requesthandler import MixinRequestHandler

LOG = logging.getLogger(__name__)

uuid_re = "(?P<id>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})"


@route("/rbac/route/")
class RouteHandlers(MixinRequestHandler):

    @auth_middleware()
    @PermissionCheck
    @coroutine
    def get(self):
        routeDB = Route()
        route_info_list = routeDB.getRoute()
        route_info_parent = routeDB.getParentRoute()
        if route_info_list and route_info_parent:
            for route_info in route_info_parent:
                buildchildren(route_info, route_info_list)
            route_list = formatRoutes(route_info_parent)
            return self.send_ok_json(data=route_list)
        return self.send_fail_json(msg=u"获取路由信息失败", code=500)

    @auth_middleware()
    @PermissionCheck
    @coroutine
    def post(self):
        form = routeSaveForm(self)
        if form.is_valid():
            isLock = True if form.value_dict["isLock"] else False
            id = form.value_dict["id"]
            parentId = form.value_dict["parentId"]
            title = form.value_dict["title"]
            path = form.value_dict["path"]
            permission = form.value_dict["permission"]
            sort = form.value_dict["sort"]
            component = form.value_dict["component"]
            componentPath = form.value_dict["componentPath"]
            cache = True if form.value_dict["cache"] else False
            name = form.value_dict["name"]
            if not component and not componentPath:
                return self.send_fail_json(msg="组件和组件路径不能同时为空")
        else:
            form_error(self, form)
        route = Route()
        code, _ = route.saveRoute(parentId, name, path, title, component, sort,
                                  componentPath, isLock, cache, permission, id)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg="保存失败")
        return


@route(r"/rbac/route/{}".format(uuid_re))
class RouteByIDHandlers(MixinRequestHandler):

    @auth_middleware()
    @PermissionCheck
    @coroutine
    def get(self, id):
        route = Route()
        routeDB = route.getById(id)
        if routeDB:
            data = {
                "id": routeDB.id,
                "parentId": routeDB.parentId,
                "title": routeDB.title,
                "name": routeDB.name,
                "path": routeDB.path,
                "component": routeDB.component,
                "componentPath": routeDB.componentPath,
                "sort": routeDB.sort,
                "cache": routeDB.cache
            }
            self.send_ok_json(data=data)
        else:
            self.send_fail_json(msg="获取路由信息失败")
        return

    @auth_middleware()
    @PermissionCheck
    @coroutine
    def delete(self, id):
        route = Route()
        code = route.delById(id)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg="删除失败")
        return
