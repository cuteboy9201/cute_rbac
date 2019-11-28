#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-08-26 10:26:19
@LastEditors: Please set LastEditors
@LastEditTime: 2019-11-28 10:03:45
'''

import logging
import json
from oslo.form.form import form_error
from oslo.util import dbObjFormatToJson
from oslo.web.requesthandler import MixinRequestHandler
from oslo.web.route import route
from tornado import gen

from dblib import crud as crudmixin
from forms.role import BatchdelForm
from forms.user import (RetPassForm, roleDelFrom, userEditRoleUserForm,
                        userPageListForm, userSaveForm)
from utils.auth import PermissionCheck, auth_middleware, md5_password
from utils.serialize import (buildchildren, builduserchildren,
                             buildUserPagesList, checkAccess, formatAccessMenu,
                             formatAccessRoutes)

LOG = logging.getLogger(__name__)


@route("/rbac/user/info")
class UserInfoHandler(MixinRequestHandler):

    @auth_middleware()
    def get(self):

        userId = self.user_id
        isAdmin = crudmixin.User().isAdmin(userId)

        # @1用户数据对象
        user = crudmixin.User().getById(userId)
        if not user:
            self.send_fail_json("用户不存在")
            return
        # 用户角色对象
        user_role = crudmixin.RoleUser().getRoleIds(userId)
        LOG.debug(u"用户ID: %s", userId)
        # @2用户角色列表
        uesr_role_list = [item.roleId for item in user_role]
        LOG.debug("用户角色列表: %s", uesr_role_list)

        if not uesr_role_list and not isAdmin:
            ret_json_data = {
                "userName": user.name,
                "userRoles": [],
                "userPermissions": [],
                "accessMenus": [],
                "accessRoutes": [],
                "isAdmin": isAdmin,
                "accessInterfaces": []
            }
            self.send_ok_json(data=ret_json_data)
            return

        # 角色权限对象
        role_function = crudmixin.RoleFunction().getRoleFunctionByRoleIds(
            uesr_role_list)

        # 用户权限ID列表
        functions = [item.menuId for item in role_function]
        LOG.debug(u"用户对应菜单页面接口的权限: %s", functions)
        # 用户权限对象
        menu = crudmixin.Menu().getMenuListByIds(functions)

        # @3用户权限列表
        user_permission = [item.permission for item in menu]

        # 菜单type==1 对象
        menu_type1 = crudmixin.Menu().getMenuList()
        # 菜单 父级菜单对象
        menu_parent = crudmixin.Menu().getParentMenu()

        # 前端路由对象
        route = crudmixin.Route().getRoute()
        # 路由 父级菜单
        route_parent = crudmixin.Route().getParentRoute()

        # @4 @5获取用户能访问对菜单列表和前端路由
        if not menu_type1 and not menu_parent:
            accessMenu = []
        if not route and route_parent:
            accessRoute = []

        if isAdmin:
            for parent in menu_parent:
                buildchildren(parent, menu_type1)
            for route_item in route_parent:
                buildchildren(route_item, route)
        else:
            for parent in menu_parent:
                builduserchildren(parent, menu_type1, user_permission)
            for route_item in route_parent:
                builduserchildren(route_item, route, user_permission)
        multilevel_menu = menu_parent
        multilevel_route = route_parent

        checkAccess(multilevel_menu, menu_type1)
        checkAccess(multilevel_route, route)
        accessMenu = formatAccessMenu(multilevel_menu)
        accessRoute = formatAccessRoutes(multilevel_route)

        # 用户接口权限对象
        userFunctionInterface = crudmixin.FunctionInterface(
        ).getFunctionInterfaceByFunctions(functions)
        userFunctionInterfaceList = [
            item.interfaceId for item in userFunctionInterface
        ]
        interfacedb = crudmixin.Interface().getByIds(userFunctionInterfaceList)
        dict_interface = [dbObjFormatToJson(item) for item in interfacedb]

        ret_json_data = {
            "userName": user.name,
            "userRoles": uesr_role_list,
            "userPermissions": user_permission,
            "accessMenus": accessMenu,
            "accessRoutes": accessRoute,
            "isAdmin": isAdmin,
            "accessInterfaces": dict_interface
        }

        self.send_ok_json(data=ret_json_data)
        return


@route("/rbac/user/save")
class UserSaveHandler(MixinRequestHandler):

    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def post(self):
        form = userSaveForm(self)
        if form.is_valid():
            email = form.value_dict["email"]
            name = form.value_dict["name"]
            phone = form.value_dict["phone"]
            realName = form.value_dict["trueName"]
            password = form.value_dict.get("password", "")
            repassword = form.value_dict.get("repassword", "")
            id = form.value_dict.get("id", "")
            if repassword != password:
                return self.send_fail_json(msg=u"输入两次密码不一致")
            save_password = md5_password(name, password)
            LOG.debug("befor_md5_info: [%s:%s]", name, password)
            LOG.debug("md5_passowrd: [%s]", save_password)
        else:
            LOG.error("req_path: %s, req_data: %s", self.request.path,
                      self.from_data())
            self.send_fail_json(msg=form.error_dict)
            return
        userDB = crudmixin.User()
        code, msg = userDB.saveUser(name, realName, save_password, email,
                                    phone, id)
        if code:
            return self.send_ok_json(data="")
        else:
            return self.send_fail_json(msg=msg, code=403)


@route("/rbac/user/del")
class UserDelHandler(MixinRequestHandler):

    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def delete(self):
        form = roleDelFrom(self)
        if form.is_valid():
            id = form.value_dict["id"]
        else:
            LOG.error("req_path: %s, req_data: %s", self.request.path,
                      self.from_data())
            self.send_fail_json(msg=form.error_dict)
            return
        roleuser = crudmixin.RoleUser()
        roleids = roleuser.getRoleIds(id)
        if roleids:
            # deluserrole = "".join(item.name for item in roleids)
            self.send_fail_json(msg=u"请先解除用户角色关系", code=500)
            return
        user = crudmixin.User()
        code, msg = user.delUserById(id)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg="")


@route("/rbac/user/pagedlist")
class UserPagesListHandler(MixinRequestHandler):

    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def get(self):

        form = userPageListForm(self)
        if form.is_valid():
            pageIndex = form.value_dict["pageIndex"]
            pageSize = form.value_dict["pageSize"]
            sortBy = form.value_dict["sortBy"]
            descending = form.value_dict["descending"]
            rules = form.value_dict["filter"]
            if rules:
                rules = json.loads(rules)
            else:
                rules = {}
        else:
            LOG.error("req_path: %s, req_data: %s", self.request.path,
                      self.from_data())
            self.send_fail_json(msg=form.error_dict)
            return
        user = crudmixin.User()
        code, totalCount, userList = user.getUserPagedList(
            pageIndex, pageSize, rules)
        data = buildUserPagesList(totalCount, userList, sortBy, rules,
                                  descending)
        return self.send_ok_json(data=data)


@route("/rbac/user/editrole/")
class EdidUserRoleInfoHandler(MixinRequestHandler):

    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def post(self):
        form = userEditRoleUserForm(self)
        if form.is_valid():
            action = form.value_dict["action"]
            roleId = form.value_dict["roleId"]
            userId = form.value_dict["userId"]
        else:
            LOG.error("req_path: %s, req_data: %s", self.request.path,
                      self.from_data())
            self.send_fail_json(msg=form.error_dict)
            return
        roleuser = crudmixin.RoleUser()
        code, msg = roleuser.saveRoleUser(action, roleId, userId)
        if code:
            self.send_ok_json(data="")
        else:
            self.send_fail_json(msg="未知错误")
        return


@route(
    "/rbac/user/(?P<uid>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})"
)
class userGetHandler(MixinRequestHandler):

    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def get(self, uid):
        user = crudmixin.User()
        userdb = user.getUserById(uid)
        if userdb:
            data = {
                "name": userdb.name,
                "trueName": userdb.realName,
                "id": userdb.id,
                "phone": userdb.phone,
                "email": userdb.email
            }
            return self.send_ok_json(data=data)
        return self.send_fail_json(msg=u"用户不存在")


@route("/rbac/user/changepassword")
class userChangePassHandler(MixinRequestHandler):
    '''
    @description:  用户自行修改密码
    @param {type}
    @return:
    '''
    @auth_middleware()
    # @PermissionCheck
    @gen.coroutine
    def post(self):
        userId = self.user_id
        form = RetPassForm(self)
        if form.is_valid():
            oldpassword = form.value_dict["oldpassword"]
            newpassword = form.value_dict["newpassword"]
            repassword = form.value_dict["repassword"]
            name = form.value_dict["name"]
        else:
            form_error(self, form)
        user = crudmixin.User()
        userDB = user.getById(userId)
        if userDB.realName != name.encode("utf-8"):
            LOG.error("db_username: %s, req_username: %s", userDB.realName,
                      name)
            self.send_fail_json("未知错误")
            return
        checkpassword = md5_password(userDB.name, oldpassword)
        if userDB.password != checkpassword:
            self.send_fail_json("旧密码错误")
            return
        if newpassword != repassword:
            self.send_fail_json("两次密码输入不一样")
            return
        if newpassword == oldpassword:
            self.send_fail_json("新密码和旧密码不能一样")
            return
        save_password = md5_password(userDB.name, newpassword)
        try:
            userDB.password = save_password
            user.session.commit()
        except Exception:
            pass
        self.send_ok_json(data="修改成功")
        return


@route("/rbac/user/adminchangepassword")
class adminResetPassHandler(MixinRequestHandler):
    '''
    @description:  管理员修改用户密码
    @param {type}
    @return:
    '''
    @auth_middleware()
    @PermissionCheck
    @gen.coroutine
    def post(self):
        # userId = self.user_id
        req_data = self.from_data()
        userId = req_data.get("name", "")
        if not userId:
            self.send_fail(msg="参数有误")
        newpassword = req_data.get("newpassword")
        repassword = req_data.get("repassword")
        if repassword != newpassword:
            self.send_fail_json(msg="两次密码不一样")
            return
        user = crudmixin.User()
        userDB = user.getById(userId)
        if userDB:
            save_password = md5_password(userDB.name, repassword)
            userDB.password = save_password
            user.session.commit()
            user.session.close()
            self.send_ok_json(data="修改成功")
            return
        else:
            self.send_fail_json("修改失败")
            return


@route("/rbac/user/batchdel")
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
        roleuser = crudmixin.RoleUser()
        user = crudmixin.User()
        ret = []
        for id in ids:
            roleids = roleuser.getRoleIds(id)
            if roleids:
                name = user.getById(id).name
                ret.append(name)
            else:
                LOG.info("删除用户: {}".format(id))
                user.delById(id)
        # if ret:
        #     data = ",".join(ret)
        if ret:
            data = {"清先删除以下用户角色绑定": ret}
            self.send_fail(msg=data)
        else:
            data = ""
            self.send_ok(data=data)
        return
