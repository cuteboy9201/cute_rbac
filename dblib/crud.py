#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-12 16:33:41
@LastEditors: Please set LastEditors
@LastEditTime: 2019-11-26 10:04:13
@Description: 
'''

import datetime
import logging

from oslo.db.module import mysqlHanlder
from oslo.util import create_id, dbObjFormatToJson
from sqlalchemy import and_, desc, or_, asc

from configs.setting import ADMIN_LIST, RBAC_NAME
from dblib import models as ORM

session_type = mysqlHanlder().get_session(RBAC_NAME)

LOG = logging.getLogger(__name__)


class MixDbObj(object):
    def __init__(self, table=None):
        self.table = table
        self.session = session_type
        self.db_obj = self.session.query(self.table)

    def getById(self, id):
        item = self.db_obj.filter(self.table.id == id).first()
        return item

    def delById(self, id):
        del_data = self.getById(id)
        if del_data:
            try:
                self.session.delete(del_data)
                self.session.commit()
                return True
            except Exception as e:
                LOG.error("delete_menu: {}".format(e))
                self.session.rollback()
                return False

    def __del__(self):
        self.session.close()


class User(MixDbObj):
    def __init__(self):
        self.table = ORM.RbacUser
        super(User, self).__init__(self.table)

    def getUserById(self, userId):
        user = self.db_obj.filter(self.table.id == userId).first()
        return user

    def getUserByNameAndPwd(self, name, password):
        user = self.db_obj.filter(self.table.name == name,
                                  self.table.password == password).first()
        return user

    def saveUser(self,
                 user="",
                 realName="",
                 password="",
                 email="",
                 phone="",
                 id=None,
                 isLock=False):
        check_user = self.db_obj.filter(self.table.name == user).first()
        if check_user and check_user.id != id:
            return False, u"用户已经存在"

        check_email = self.db_obj.filter(self.table.email == email).first()
        if check_email and check_email.id != id:
            return False, u"邮箱已经存在"

        try:
            if id:
                userobj = self.db_obj.filter(self.table.id == id).first()
                if userobj:
                    if user:
                        userobj.name = user
                    if email:
                        userobj.email = email
                    if realName:
                        userobj.realName = realName
                    if password:
                        userobj.password = password
                    if phone:
                        userobj.phone = phone
                    userobj.isLock = False
                    self.session.commit()
                    return True, userobj
            else:
                add_user = self.table(name=user,
                                      realName=realName,
                                      password=password,
                                      email=email,
                                      phone=phone,
                                      isLock=isLock,
                                      id=create_id(),
                                      create_at=datetime.datetime.now())
                self.session.add(add_user)
                self.session.commit()
                return True, add_user
        except Exception as e:
            LOG.error("save_user: {}".format(e))
            self.session.rollback()
            return False, ""
        return True, ""

    def isAdmin(self, userId):
        user = self.getById(userId)
        if user:
            if user.name in ADMIN_LIST:
                return True
        return False

    def delUserById(self, id):
        user = self.db_obj.filter(self.table.id == id).first()
        try:
            if user:
                self.session.delete(user)
                self.session.commit()
                return True, ""
        except Exception:
            self.session.rollback()
            return False, ""

    def getUserPagedList(self, pageIndex, pageSize, rule):
        offset_nu = (pageIndex - 1) * pageSize
        user_obj = self.db_obj
        if rule.get("name"):
            user_obj = user_obj.filter(
                self.table.name.like("%{}%".format(rule["name"])))
        if rule.get("email"):
            user_obj = user_obj.filter(
                self.table.email.like("%{}%".format(rule["email"])))
        userdb = user_obj.all()
        totalCount = len(userdb)
        get_user_db = user_obj.limit(pageSize).offset(offset_nu).all()
        if rule.get("roleId"):
            roleuser = RoleUser()
            userids = roleuser.getUserIds(rule["roleId"])
            userlist = [item.userId for item in userids]
            for user in get_user_db:
                if user.id in userlist:
                    user.isAdd = 1
                else:
                    user.isAdd = 2
        return True, totalCount, get_user_db


class Role(object):
    def __init__(self):
        self.table = ORM.RbacRole
        self.session = session_type
        self.db_obj = self.session.query(self.table)

    def getRoleById(self, id):
        role = self.db_obj.filter(self.table.id == id).first()
        return role

    def getRoleByCode(self, code):
        role = self.db_obj.filter(self.table.code == code).first()
        return role

    def getRoleByIds(self, ids):
        roles = self.db_obj.filter(self.table.id.in_(ids)).all()
        return roles

    def saveRole(self, name, code, desc, isLock=False, id=None):
        check_name = self.db_obj.filter(self.table.name == name).first()
        if check_name and check_name.id != id:
            return False, ""
        check_code = self.db_obj.filter(self.table.code == code).first()
        if check_code and check_code.id != id:
            return False, ""
        try:
            if id:
                role = self.db_obj.filter(self.table.id == id).first()
                if role:
                    role.name = name
                    role.code = code
                    role.desc = desc
                    role.isLock = isLock
                    self.session.commit()
            else:
                add_role = self.table(name=name,
                                      code=code,
                                      desc=desc,
                                      isLock=isLock,
                                      id=create_id())
                self.session.add(add_role)
                self.session.commit()
        except Exception as e:
            LOG.error("save_user: {}".format(e))
            self.session.rollback()
            return False, ""
        return True, ""

    def delRole(self, id):
        try:
            role = self.db_obj.filter(self.table.id == id).first()
            if role:
                self.session.delete(role)
                self.session.commit()
        except Exception as e:
            LOG.error("save_user: {}".format(e))
            self.session.rollback()
            return False
        return True

    def getRolePagedList(self, pageIndex, pageSize, rule):
        offset_nu = (pageIndex - 1) * pageSize
        role_obj = self.db_obj
        if rule.get("code"):
            role_obj = role_obj.filter(
                self.table.code.like("%{}%".format(rule["code"])))
        if rule.get("name"):
            role_obj = role_obj.filter(
                self.table.name.like("%{}%".format(rule["name"])))
        roeldb = role_obj.all()
        totalCount = len(roeldb)
        get_role_db = role_obj.limit(pageSize).offset(offset_nu).all()
        if rule.get("userId"):
            roleuser = RoleUser()
            roleids = roleuser.getRoleIds(rule["userId"])
            rolelist = [item.roleId for item in roleids]
            reponse_list = []
            for role in get_role_db:
                if role.id in rolelist:
                    role.isAdd = 1
                else:
                    role.isAdd = 2
                reponse_list.append(role)
        if get_role_db:
            return True, totalCount, get_role_db
        return True, 0, []

    def __del__(self):
        self.session.close()


class Menu(object):
    def __init__(self):
        self.table = ORM.RbacMenu
        self.session = session_type
        self.db_obj = self.session.query(self.table)

    def getMenuById(self, id):
        menu = self.db_obj.filter(self.table.id == id).first()
        return menu

    def getMenuList(self):
        """
        type ==1
        """
        menulist = self.db_obj.filter(self.table.type == 1).order_by(
            asc(self.table.sort)).all()
        return menulist

    def getMenuAllList(self):
        menulist = self.db_obj.order_by(asc(self.table.sort)).all()
        return menulist

    def getParentMenu(self):
        menu = self.db_obj.filter(self.table.parentId == "0",
                                  self.table.isLock == False).order_by(
                                      asc(self.table.sort)).all()
        return menu

    def getMenuListByIds(self, ids):
        menulist = self.db_obj.filter(self.table.id.in_(ids)).all()
        return menulist

    def saveMenu(self,
                 parentId,
                 title,
                 icon,
                 sort,
                 _type,
                 isLock=False,
                 desc="",
                 permission="",
                 path="",
                 id=""):
        try:
            if id and id != "0":
                menu = self.getMenuById(id)
                if menu:
                    menu.title = title
                    menu.type = int(_type)
                    menu.isLock = isLock
                    menu.icon = icon
                    menu.permission = permission
                    menu.sort = sort
                    self.session.commit()
                    return True, ""
            check_permission = self.db_obj.filter(
                self.table.permission == permission,
                self.table.type == int(_type)).first()
            if check_permission:
                return False, "权限标识已经存在"
            if int(_type) == 1:
                check_path = self.db_obj.filter(
                    self.table.path == path).first()
                if check_path:
                    return False, "前端路径已经存在"
            add_menu = self.table(parentId=parentId,
                                  path=path,
                                  title=title,
                                  icon=icon,
                                  permission=permission,
                                  type=int(_type),
                                  sort=sort,
                                  isLock=isLock,
                                  desc=desc,
                                  id=create_id())
            self.session.add(add_menu)
            self.session.flush()
            self.session.commit()
            return True, add_menu
        except Exception as e:
            LOG.error("save_user: {}".format(e))
            self.session.rollback()
            return False, ""

    def delMenu(self, id):
        menu = self.getMenuById(id)
        if menu:
            try:
                self.session.delete(menu)
                self.session.commit()
                return True
            except Exception as e:
                LOG.error("delete_menu: {}".format(e))
                self.session.rollback()
                return False

    def __del__(self):
        self.session.close()


class Route(MixDbObj):
    def __init__(self):
        self.table = ORM.RbacRoute
        super(Route, self).__init__(self.table)

    def getRouteById(self, id):
        route = self.db_obj.filter(self.table.id == id).first()
        return route

    def getRouteByIds(self, ids):
        routeList = self.db_obj.filter(self.table.id.in_(ids)).all()
        return routeList

    def getRoute(self):
        route = self.db_obj.order_by(asc(self.table.sort)).all()
        return route

    def getParentRoute(self):
        route = self.db_obj.filter(self.table.parentId == "0",
                                   self.table.isLock == False).all()
        return route

    def saveRoute(self,
                  parentId="",
                  name="",
                  path="",
                  title="",
                  component="",
                  sort="",
                  componentPath="",
                  isLock=False,
                  cache=True,
                  permission="",
                  id=""):
        try:
            if id and id != "0":
                route = self.getRouteById(id)
                if route:
                    route.title = title,
                    route.path = path
                    route.isLocak = isLock,
                    route.name = name
                    route.permission = permission
                    route.sort = sort
                    route.component = component,
                    route.componentPath = componentPath,
                    route.cache = cache
                    self.session.commit()
                    return True, ""
            else:
                add_route = self.table(parentId=parentId,
                                       path=path,
                                       name=name,
                                       title=title,
                                       permission=permission,
                                       component=component,
                                       componentPath=componentPath,
                                       sort=sort,
                                       isLock=isLock,
                                       cache=cache,
                                       id=create_id())
                self.session.add(add_route)
                self.session.flush()
                self.session.commit()
                return True, add_route
        except Exception as e:
            import traceback
            traceback.print_exc()
            LOG.error("save_route: {}".format(e))
            self.session.rollback()
            return False, ""


class Interface(MixDbObj):
    def __init__(self):
        self.table = ORM.RbacInterface
        super(Interface, self).__init__(self.table)

    def getByIds(self, ids):
        interface = self.db_obj.filter(self.table.id.in_(ids)).all()
        return interface

    def saveInterface(self, name, path, method, desc, id=""):
        try:
            if id:
                interface = self.getById(id)
                if interface:
                    interface.name = name
                    interface.method = method
                    interface.desc = desc
                    interface.path = path
                    self.session.commit()
                    return True, ""
            else:
                check_path_method = self.db_obj.filter(
                    self.table.path == path,
                    self.table.method == method).first()
                if check_path_method:
                    return False, u"方法和路径必须唯一"
                add_interface = self.table(name=name,
                                           path=path,
                                           method=method,
                                           desc=desc,
                                           id=create_id())
                self.session.add(add_interface)
                self.session.commit()
                return True, add_interface
        except Exception as e:
            LOG.error("save_interface: {}".format(e))
            self.session.rollback()
            return False, ""
        return True, ""

    def getInterfacePagedList(self, pageIndex, pageSize, rule):
        offset_nu = (pageIndex - 1) * pageSize
        interfaceObj = self.db_obj
        if rule.get("name"):
            interfaceObj = interfaceObj.filter(
                self.table.name.like("%{}%".format(rule["name"])))
        if rule.get("path"):
            LOG.debug("path: {}".format(rule.get("path")))
            interfaceObj = interfaceObj.filter(
                self.table.path.like("%{}%".format(rule["path"])))
        if rule.get("method"):
            interfaceObj = interfaceObj.filter(
                self.table.method.like("%{}%".format(rule.get("method"))))

        # 接口总数
        interfaceDB = interfaceObj.all()
        totalCount = len(interfaceDB)

        # 本页展示数据
        get_interface_db = interfaceObj.limit(pageSize).offset(offset_nu).all()

        if rule.get("functionId"):
            interfaceListObj = FunctionInterface()
            interfaceListObj = interfaceListObj.getFunctionInterfaceByFunction(
                rule.get("functionId"))
            rolinterfaceListlist = [
                item.interfaceId for item in interfaceListObj
            ]
            for itmes in get_interface_db:
                if itmes.id in rolinterfaceListlist:
                    itmes.isAdd = 1
                else:
                    itmes.isAdd = 2
        if get_interface_db:
            return True, totalCount, get_interface_db
        return True, 0, []


class RoleUser(MixDbObj):
    def __init__(self):
        self.table = ORM.RbacRoleuser
        super(RoleUser, self).__init__(self.table)

    def getUserIds(self, roleId):
        roleuser = self.db_obj.filter(self.table.roleId == roleId).all()
        return roleuser

    def getRoleIds(self, userId):
        roleuser = self.db_obj.filter(self.table.userId == userId).all()
        return roleuser

    def saveRoleUser(self, action, roleId, userId):
        try:
            roleuser = self.db_obj.filter(self.table.userId == userId,
                                          self.table.roleId == roleId).first()
            if action == 1 or action == "1":
                if not roleuser:
                    add_roleuser = self.table(userId=userId,
                                              roleId=roleId,
                                              id=create_id())
                    self.session.add(add_roleuser)
                else:
                    return False, "已经存在"
            if action == "0" or action == 0:
                self.session.delete(roleuser)
            self.session.commit()
            return True, ""
        except Exception as e:
            LOG.error("save_interface: {}".format(e))
            self.session.rollback()
            return False, ""
        return True, ""


class RoleFunction(MixDbObj):
    def __init__(self, table=None):
        self.table = ORM.RbacRolefunction
        super(RoleFunction, self).__init__(table=self.table)

    def getRoleFunctionByRoleId(self, roleId):
        rolefunction = self.db_obj.filter(self.table.roleId == roleId).all()
        return rolefunction

    def getRoleFunctionByRoleIds(self, roleIds):
        if roleIds:
            rolefunction = self.db_obj.filter(
                self.table.roleId.in_(roleIds)).all()
            return rolefunction
        return []

    def getRoleFunctionByMenuId(self, menuId):
        rolefunction = self.db_obj.filter(self.table.menuId == menuId).all()
        return rolefunction

    def saveRoleFunction(self, roleId, permission):
        try:
            role_data = self.db_obj.filter(self.table.roleId == roleId).all()
            if len(permission) == 0:
                for data in role_data:
                    self.session.delete(data)
                    self.session.commit()
                return True, ""
            else:
                for item in role_data:
                    if item.menuId in permission:
                        permission.remove(item.menuId)
                        continue
                    else:
                        self.session.delete(item)
                        self.session.commit()
                for i in permission:
                    add_data = self.table(roleId=roleId,
                                          menuId=i,
                                          id=create_id())
                    self.session.add(add_data)
                    self.session.commit()
                return True, ""

        except Exception as e:
            LOG.error(e)
            return False, ""


class FunctionInterface(MixDbObj):
    def __init__(self, table=None):
        self.table = ORM.RbacFunctioninterface
        super(FunctionInterface, self).__init__(table=self.table)

    def getFunctionInterface(self):
        functioninterface = self.db_obj.all()
        return functioninterface

    def getFunctionInterfaceByFunctions(self, functions):
        functioninterface = self.db_obj.filter(
            self.table.menuId.in_(functions)).all()
        return functioninterface

    def getFunctionInterfaceByFunction(self, function):
        functioninterface = self.db_obj.filter(
            self.table.menuId == function).all()
        return functioninterface

    def saveFunctionInterface(self, action, funcrionId, interfaceId):
        functioninterface = self.db_obj.filter(
            self.table.menuId == funcrionId,
            self.table.interfaceId == interfaceId).first()

        if action == 0 and functioninterface:
            self.session.delete(functioninterface)
            self.session.commit()
            return True
        elif action == 1 and not functioninterface:
            add_data = self.table(menuId=funcrionId,
                                  interfaceId=interfaceId,
                                  id=create_id())
            self.session.add(add_data)
            self.session.commit()
            return True
        else:
            return False
