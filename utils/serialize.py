#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-13 10:20:38
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 10:58:51
@Description: 
'''


def buildchildren(parentobj, allobj):
    '''
    @description:  给parentobj对象添加children子对象
    @param {type} 
    @return: 
    '''
    children = []
    for item in allobj:
        if parentobj.id == item.parentId:
            children.append(item)

    for subobj in children:
        buildchildren(subobj, allobj)
    parentobj.children = children
    return parentobj


def formatMenus(menus):

    def f(kv, children):
        kv.setdefault("children", [])
        for child in children:
            kvChile = dict(title=child.title, path=child.path, icon=child.icon,
                           id=child.id, sort=child.sort, type=child.type, permssion=child.permission)
            if child.children and len(child.children) > 0:
                f(kvChile, child.children)
            kv["children"].append(kvChile)

    accessMenuList = []
    for menu in menus:
        kv = dict(title=menu.title, path=menu.path, icon=menu.icon,
                  id=menu.id, sort=menu.sort, type=menu.type, permssion=menu.permission)
    if menu.children and len(menu.children) > 0:
        f(kv, menu.children)
    accessMenuList.append(kv)
    return accessMenuList


def buildUserPagesList(totalCount, userList, sortBy, rules, descending):
    '''
    @description: 格式化用户返回信息 
    @param {type} 
    @return: 
    '''
    response = []
    for user in userList:
        row = {
            "name": user.name,
            "password": "",
            "email": user.email,
            "id": user.id,
            "phone": user.phone,
            "trueName": user.realName
        }
        if rules.get("roleId"):
            row.setdefault("isAdd", user.isAdd)
        response.append(row)
    if sortBy and sortBy != "None":
        response = sorted(response,
                          key=lambda x: x[sortBy],
                          reverse=descending)
    if rules.get("roleId"):
        response = sorted(response,
                          key=lambda x: x["isAdd"],
                          reverse=descending)
    return {"totalCount": totalCount, "rows": response}


def formatAccessRoutes(routes):
    def f(kv, children):
        kv.setdefault("children", [])
        for child in children:
            kvChild = {
                "name": child.name,
                "path": child.path,
                "component": child.component,
                "componentPath": child.componentPath,
                "meta": {
                    "title": child.title,
                    "cache": child.cache
                }
            }
            if child.children and len(child.children) > 0:
                f(kvChild, child.children)
            kv["children"].append(kvChild)

    accessRouteList = []
    for route in routes:
        kv = {
            "name": route.name,
            "path": route.path,
            "component": route.component,
            "componentPath": route.componentPath,
            "meta": {
                "title": route.title,
                "cache": route.cache
            }
        }
        if route.children and len(route.children) > 0:
            f(kv, route.children)
        accessRouteList.append(kv)
    return accessRouteList


def formatAccessMenu(menus):
    def f(kv, children):
        kv.setdefault("children", [])
        for child in children:
            kvChild = {
                "title": child.title,
                "path": child.path,
                "icon": child.icon
            }
            if child.children and len(child.children) > 0:
                f(kvChild, child.children)
            kv["children"].append(kvChild)

    accessMenuList = []
    for menu in menus:
        kv = {"title": menu.title, "path": menu.path, "icon": menu.icon}
        if menu.children and len(menu.children) > 0:
            f(kv, menu.children)
        accessMenuList.append(kv)
    return accessMenuList


def checkAccess(parentobj, allobj):

    for obj in allobj:
        for item in parentobj:
            if len(item.children) == 0 and item.id == obj.parentId:
                parentobj.remove(item)
            if item.children:
                checkAccess(item.children, allobj)


def builduserchildren(parentobj, allobj, userpermission):
    '''
    @description: 根据父ID进行 children 分层结构
    @param parentobj 是父级菜单对象
    @param allobj 是所有菜单对象 
    @param userpermission 是用户权限
    @return: 
    '''
    children = []
    for item in allobj:
        # 当此条menu 信息的父级ID等于当前 parentobj.id的时候 把其信息添加到 parentobj.children中
        if parentobj.id == item.parentId and (
                not item.permission or item.permission in userpermission):
            children.append(item)

    # 检测children的children
    for subobj in children:
        builduserchildren(subobj, allobj, userpermission)
    parentobj.children = children
    return parentobj


def buildRolePagesList(totalCount, roles, sortBy, rules, descending):
    roleList = []
    for role in roles:
        row = {
            "name": role.name,
            "code": role.code,
            "description": role.desc,
            "id": role.id,
        }
        if rules.get("userId"):
            row.setdefault("isAdd", role.isAdd)
        roleList.append(row)
    if sortBy and sortBy != "None":
        roleList = sorted(roleList,
                          key=lambda x: x[sortBy],
                          reverse=descending)
    if rules.get("userId"):
        roleList = sorted(roleList,
                          key=lambda x: x["isAdd"],
                          reverse=descending)
    return {"totalCount": totalCount, "rows": roleList}


def formatRoutes(routes):
    def f(kv, children):
        kv.setdefault("children", [])
        for child in children:
            kvChild = {
                "title": child.title,
                "path": child.path,
                "id": child.id,
                "sort": child.sort,
                "permssion": child.permission,
                "parentId": child.parentId,
                "name": child.name,
                "component": child.component,
                "componentPath": child.componentPath,
                "isLock": child.isLock,
                "cache": child.cache,
            }
            if child.children and len(child.children) > 0:
                f(kvChild, child.children)
            kv["children"].append(kvChild)

    accessRouteList = []
    for route in routes:
        kv = {
            "title": route.title,
            "path": route.path,
            "id": route.id,
            "sort": route.sort,
            "permssion": route.permission,
            "parentId": route.parentId,
            "name": route.name,
            "component": route.component,
            "componentPath": route.componentPath,
            "isLock": route.isLock,
            "cache": route.cache,
        }
        if route.children and len(route.children) > 0:
            f(kv, route.children)
        accessRouteList.append(kv)
    return accessRouteList
