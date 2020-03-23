#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-08-21 11:13:46
@LastEditors  : YouShumin
@LastEditTime : 2020-01-19 16:48:06
'''
import logging
import logging.config
import os
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.options
import tornado.web
from configs.setting import (ALLOW_HOST, COOKIE_SECRET, HOST, LOGFILE, PORT,
                             PROJECT_NAME)
from oslo.db.module import mysqlHanlder
from tornado.log import enable_pretty_logging
from tornado.options import define, options

debug = os.environ.get("RUN_ENV")
if debug == "prod":
    options.log_file_prefix = LOGFILE
    options.log_rotate_mode = "time"
    options.log_rotate_when = "D"
    options.log_rotate_interval = 1
    options.log_file_num_backups = 30
    options.log_to_stderr = False
LOG = logging.getLogger(__name__)


class LogHandler(tornado.log.LogFormatter):
    """
        设置tornado 日志信息 当设置RUN_ENV为prod的时候进行文件输出,否则控制台
        python3 会有问题... 不是大问题, 不在细化研究...使用supervisor管理python
    """
    def __init__(self):
        super(LogHandler, self).__init__(
            fmt=
            '%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')


p_version = sys.version_info.major
if p_version == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')


class RouteHandler(object):
    """注册路由"""
    def __init__(self):
        """
        需要配置这里实现注册路由...
            自动注册路由的方式可以继承 application实现
            我这边是想实现像flask蓝本一样实现注册...所以暂时设置为这样
        """

        from handlers import auth
        from handlers import interface
        from handlers import menu
        from handlers import user
        from handlers import role
        from handlers import route
        from handlers import api

        from oslo.web.route import route
        self.route = route
        super(RouteHandler, self).__init__()


class DB(object):
    """初始化数据库"""
    def __init__(self):
        self.db = mysqlHanlder()

    def rbac_init(self):
        """初始化rbac数据库"""
        from configs.setting import RBAC_DB, RBAC_DB_ECHO, RBAC_NAME
        self.db.init(dbname=RBAC_NAME, dburl=RBAC_DB, dbecho=RBAC_DB_ECHO)


class Application(tornado.web.Application, RouteHandler):
    """初始化application"""
    def __init__(self):
        configs = dict(
            # emplate_path=os.path.join(PATH_APP_ROOT, "templates"),
            debug=options.debug,
            cookie_secret=COOKIE_SECRET,
            autoescape=None,
        )
        DB().rbac_init()
        RouteHandler.__init__(self)
        tornado.web.Application.__init__(self, self.route.get_urls(),
                                         **configs)


class WebApp():
    """应用启动唯一入口"""
    def __init__(self):
        """
            初始化启动信息
                运行环境 debug
                运行ip host
                启动端口 port
        """
        if debug != "prod":
            define("debug", default=True, help="enable debug mode")
            define("allow_host", default=[], help="allow host")
        else:
            define("debug", default=False, help="enable debug mode")
            define("allow_host", default=ALLOW_HOST, help="allow host")
        define("host", default=HOST, help="run on this host", type=str)
        define("port", default=PORT, help="run on this port", type=int)

        LOG.info(options.allow_host)

    def run(self):
        [i.setFormatter(LogHandler()) for i in logging.getLogger().handlers]
        enable_pretty_logging()
        http_server = tornado.httpserver.HTTPServer(Application(),
                                                    xheaders=True)
        if options.debug:
            logging.getLogger().setLevel(logging.DEBUG)
            http_server.listen(options.port, address=options.host)
            LOG.info("start app [%s] for %s:%s", PROJECT_NAME, options.host,
                     options.port)
        else:
            http_server.listen(options.port, address=options.host)
            LOG.info("start app [%s] for %s:%s", PROJECT_NAME, options.host,
                     options.port)
        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            tornado.ioloop.IOLoop.instance().stop()

    def stop(self):
        tornado.ioloop.IOLoop.instance().stop()


def web_app():
    return WebApp()
