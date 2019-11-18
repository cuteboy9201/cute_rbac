#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-15 14:07:31
@LastEditors: Youshumin
@LastEditTime: 2019-11-18 10:07:15
@Description: 
'''
import logging

from app import DB
DB().rbac_init()
from dblib import crud
from utils.auth import md5_password

LOG = logging.getLogger(__name__)
user = crud.User()
menu = crud.Menu()
route = crud.Route()
interface = crud.Interface()
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
    return [
        insert_route_menu, insert_route_interface, insert_route_user,
        insert_route_role, instert_route_route
    ]


def interface_option():

    interfaece_infos = [
        ('0317ee55-c941-4cde-950b-3943e3941bb6', '保存接口', '/rbac/interface/',
         'post', '保存接口信息'),
        ('061360da-42ea-4ced-a389-d1d84d5be561', '用户密码修改[管理]',
         '/rbac/user/adminchangepassword', 'post', '管理员直接修改用户密码'),
        ('06e60a5a-6e8b-46ef-8bbb-b9c8505eac93', '用户批量删除',
         '/rbac/user/batchdel', 'delete', '用户批量删除'),
        ('07e63371-4d47-4f0b-a389-0e873d7f8cd7', '用户删除', '/rbac/user/del',
         'delete', '根据ID删除用户'),
        ('08437312-0c3a-4d76-84da-72b4d0902ee4', '菜单列表获取', '/rbac/menu', 'get',
         '查看菜单信息'),
        ('1a7fb5df-9392-4a59-b654-5d1c301e2316', '用户添加', '/rbac/user/save',
         'post', '添加用户'),
        ('1dc000a8-89af-49b6-a930-9ee81a8066d9', '路由信息', '/rabc/route/:id',
         'get', '根据ID获取路由信息'),
        ('22e5b39c-1e89-4881-9b1d-3deae5496298', '角色列表', '/rbac/role/', 'get',
         '获取角色列表'),
        ('3e9697ec-ffcb-4f92-9deb-c10d7cd7c91c', '接口ID信息',
         '/rbac/interface/:id', 'get', '根据ID查看菜单信息'),
        ('428c359b-aa1a-4987-9087-67b58faed3c9', '角色权限保存',
         '/rbac/role/savepermission/', 'post', '保存角色权限'),
        ('5378c831-6e86-4f96-9ac7-2fec85d7ff05', '用户修改密码',
         '/rbac/user/changepassword', 'post', '修改自己的密码'),
        ('5b2f1df5-db0b-47b4-b2d7-e3ad063a8866', '角色权限获取',
         '/rbac/role/permissions/:id', 'get', '根据ID获取角色已经有的权限'),
        ('668a3300-7706-4a0f-b360-2c6a1fdea57b', '接口列表', '/rbac/interface/',
         'get', '获取接口列表'),
        ('8106085e-55c3-456d-a63e-2baa5baedfb4', '用户权限', '/rbac/user/info',
         'get', '获取用户权限'),
        ('81af2c6a-da9a-41f7-976b-2fb9dc497f6e', '路由获取', '/rbac/route/', 'get',
         '获取路由列表'),
        ('89d1cf91-c7ea-48d0-9c93-4ed2d1f4c8bf', '角色保存', '/rbac/role/', 'post',
         '保存角色信息'),
        ('92a15e56-213f-49f5-ad70-bd639a8c7d9d', '角色删除', '/rbac/role/',
         'delete', '删除角色信息'),
        ('9b0fc3ab-28d0-4241-9af4-226b2dc41cfd', '角色批量删除',
         '/rbac/role/batchdel', 'delete', '批量删除角色信息'),
        ('a190d99c-4026-463b-9cf7-0b7343e881f0', '用户修改',
         '/rbac/user/editrole/', 'post', '修改用户信息'),
        ('a6f4d4ae-e4f1-4e99-b1b6-43a70303feb0', '角色信息', '/rbac/role/:id',
         'get', '根据ID获取角色信息'),
        ('aded0794-f714-4b10-8cb2-54e118bd2a1f', '用户信息', '/rbac/user/:id',
         'get', '根据ID过去用户信息'),
        ('be18e4dd-4373-4157-a9dc-727b036eb4c4', '接口批量删除', '/rbac/interface/',
         'delete', '批量删除接口'),
        ('bfd8ca00-06e4-434e-b256-cb76a7b368f9', '菜单删除', '/rbac/menu/:id',
         'delete', '根据ID删除菜单'),
        ('c1ed76b8-499f-42c1-b063-e854a7798c72', '接口绑定角色',
         '/rbac/interface/relate/', 'post', '添加或者删除角色权限【关联接口信息】'),
        ('c6275469-62f8-4aac-b52f-b94193552d92', '接口删除', '/rbac/interface/:id',
         'delete', '根据ID删除接口信息'),
        ('d956d997-2a91-4864-9fe5-ca0ea479ef9b', '获取菜单', '/rbac/menu/:id',
         'get', '根据:id获取菜单信息'),
        ('e4e162af-5e7b-4eaf-9512-5e6b1f86459d', '获取菜单路径', '/rbac/menu/1/',
         'get', '绑定路径搜索使用'),
        ('ed7cab17-f738-4fa4-a977-6fa016f81379', '用户列表',
         '/rbac/user/pagedlist', 'get', '获取用户列表'),
        ('f0dbdc50-42ae-43bd-b63b-f51e886d8d5c', '路由保存', '/rbac/route/',
         'post', '保存路由信息'),
        ('f60012b4-1970-4b76-bf9e-a01dfaa89af3', '菜单信息修改', '/rbac/menu',
         'post', '修改菜单信息'),
        ('fed43e88-44cd-4ca6-b739-34236643f780', '路由删除', '/rbac/route/:id',
         'delete', '根据ID删除路由')
    ]

    for item in interfaece_infos:
        _, name, path, method, desc = item
        interface.saveInterface(name, path, method, desc)


def init_base():
    user_list = []
    menu_list = []
    route_list = []
    try:
        usercode, userinfo = user.saveUser(**superuser)
        if usercode:
            user_list.append(userinfo)
        else:
            raise
        menucode, menuinfo = menu.saveMenu(**menu_sys)
        if menucode:
            menu_list.append(menuinfo)
            menuList = menu_options(menuinfo)

            for item in menuList:
                code, info = menu.saveMenu(**item)
                if code:
                    menu_list.append(info)
                else:
                    raise
        else:
            raise
        routecode, routeinfo = route.saveRoute(**insert_route_system)
        if routecode:
            route_list.append(routeinfo)
            routeList = route_options(routeinfo)
            for item in routeList:
                code, info = route.saveRoute(**item)
                if code:
                    route_list.append(info)
                else:
                    raise
        else:
            raise
        interface_option()
    except:
        if route_list:
            for del_route in route_list:
                route.delById(del_route.id)
        if menu_list:
            for del_menu in menu_list:
                menu.delMenu(del_menu.id)
        if user_list:
            for del_user in user_list:
                LOG.info("del user_id: {}".format(del_user.id))
                user.delById(del_user.id)
