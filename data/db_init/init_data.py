#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-15 14:07:31
@LastEditors: Youshumin
@LastEditTime: 2019-11-15 14:46:31
@Description: 
'''
from dblib import crud
from utils.auth import md5_password
import logging

LOG = logging.getLogger(__name__)
user = crud.User()
menu = crud.Menu()
route = crud.Route()


# 添加超级用户
superuser = dict(user="superuser",
                 realName="超级管理员",
                 password=md5_password("superuser", "Admin@123"),
                 email="admin@gmail.com",
                 phone="13800000000",
                 isLock=False)

# 添加基础菜单
menu_sys = {
    "parentId": "0",
    "title": u"系统管理",
    "path": "/system",
    "icon": "cogs",
    "sort": "1",
    "_type": 1
}

# 基础路由添加
insert_route_system = {
    "parentId": "0",
    "name": "System",
    "title": u"系统设置",
    "path": "/system",
    "permission": "",
    "component": "layoutHeaderAside",
    "componentPath": "layout/header-aside/layout",
    "sort": "1",
    "isLock": False,
    "cache": True
}

def menu_options(menu_obj):
    insert_menu_man = {
        "parentId": menu_obj.id,
        "title": u"菜单管理",
        "path": "/system/menu",
        "icon": "th-list",
        "sort": "1",
        "_type": 1,
        "permission": "p_menu_menu"
    }
    insert_mune_route = {
        "parentId": menu_obj.id,
        "title": u"路由管理",
        "_type": "1",
        "permission": "p_route_menu",
        "sort": 2,
        "icon": "share-alt-square",
        "path": "/system/route"
    }
    inster_menu_role = {
        "parentId": menu_obj.id,
        "title": u"角色管理",
        "path": "/system/role",
        "_type": 1,
        "sort": "3",
        "icon": "users",
        "permission": "p_role_menu"
    }
    inster_menu_user = {
        "parentId": menu_obj.id,
        "title": u"用户管理",
        "path": "/system/user",
        "sort": "4",
        "_type": 1,
        "icon": "user",
        "permission": "p_user_menu"
    }

    insert_menu_interface = {
        "parentId": menu_obj.id,
        "title": u"接口管理",
        "path": "/system/interface",
        "_type": 1,
        "sort": "5",
        "icon": "paper-plane",
        "permission": "p_interface_menu"
    }

    return [
        insert_menu_man, insert_menu_interface, inster_menu_user,
        insert_mune_route, inster_menu_role
    ]


def route_options(route_obj):
    insert_route_menu = {
        "parentId": route_obj.id,
        "name": "MenuPage",
        "title": u"菜单管理",
        "path": "/system/menu",
        "component": "menu",
        "componentPath": "pages/sys/menu/index",
        "sort": "2",
        "isLock": False,
        "cache": True
    }
    instert_route_route = {
        "parentId": route_obj.id,
        "name": "RoutePage",
        "title": u"路由管理",
        "path": "/system/route",
        "component": "route",
        "componentPath": "pages/sys/route/index",
        "sort": "3",
        "cache": True
    }
    insert_route_role = {
        "parentId": route_obj.id,
        "name": "RolePage",
        "title": u"角色管理",
        "path": "/system/role",
        "component": "role",
        "componentPath": "pages/sys/role/index",
        "sort": "4",
        "cache": True
    }
    insert_route_user = {
        "parentId": route_obj.id,
        "name": "UserPage",
        "title": u"用户管理",
        "path": "/system/user",
        "component": "user",
        "componentPath": "pages/sys/user/index",
        "sort": "5",
        "cache": True
    }
    insert_route_interface = {
        "parentId": route_obj.id,
        "name": "InterfacePage",
        "title": u"接口管理",
        "path": "/system/interface",
        "component": "interface",
        "sort": "5"
    }    
    return [ insert_route_menu,insert_route_interface,insert_route_user,insert_route_role,instert_route_route ]

def init_base():
    user_list = []
    menu_list = []
    route_list = []
    try:
        usercode, userinfo = user.saveUser(**superuser)
        if usercode:
            user_list.append([dict(user=userinfo)])
        else:
            pass
        
        menucode, menuinfo = menu.saveMenu(**menu_sys)
        if menucode:
            menu_list.append(menuinfo)
            menuList = menu_options(menuinfo)
            
            for item in menuList:
                code,info = menu.saveMenu(**item)
                if code:
                    menu_list.append(info)
        
        routecode, routeinfo = route.saveRoute(**insert_route_system)
        if routecode:
            route_list.append(routeinfo)
            routeList = route_options(routeinfo)

            for item in menuList:
                code, info = route.saveRoute(**item)
                if code:
                    route_list.append(info)
    except:
        if route_list:
            