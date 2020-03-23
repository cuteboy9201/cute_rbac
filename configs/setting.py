#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-10-11 11:24:53
@LastEditors: YouShumin
@LastEditTime: 2020-03-23 17:15:58
@Description: 
'''

import os

debug = os.environ.get("RUN_ENV")

if debug == "prod":
    from configs.cfg import RBAC_NAME, RBAC_DB, RBAC_DB_ECHO, ADMIN_LIST
else:
    from configs.dev_cfg import RBAC_NAME, RBAC_DB, RBAC_DB_ECHO, ADMIN_LIST

PATH_APP_ROOT = os.path.abspath(
    os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))))

COOKIE_SECRET = "0wEE^@!TKGwbC0p@nyY4*Cm*8ojzulHC48HT620YJl^zE6qE"
PROJECT_NAME = "CuTeeyes"
ALLOW_HOST = ["http://192.168.2.108:4445", "http://192.168.2.108:8080"]
LOGFILE = "/Users/youshumin/logs/dev_rbac.log"
HOST = "0.0.0.0"
PORT = 3001