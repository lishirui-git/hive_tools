#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-11-17
# @Author  : 殷帅

import os

import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado.escape
from tornado.options import define
from hive_schema_create import HiveSchemaCreate
from date_shell_trans import  DateShellTrans
# open debug mode
define("debug", default=True, help="debug mode", type=bool)

settings = {
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'template_path': os.path.join(os.path.dirname(__file__), "template"),
}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html')


class TransHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        sql = self.get_argument("sql", "")
        oper = self.get_argument("oper", "")
        # sql = tornado.escape.utf8(sql)  # uicode to utf8  escape 和 encode公用会出问题,后面看看原因
        dtrans = DateShellTrans(sql)
        if oper == 'shell_to_date':
            ret = dtrans.replace_sql_shell_flag()
        elif oper == 'date_to_shell':
            ret = dtrans.replace_sql_pt_2_shell()
        self.write({"ret": ret.encode('utf-8')})

    def get(self):
        sql = self.get_argument("sql", "")
        oper = self.get_argument("oper", "date_to_shell")
        # sql = tornado.escape.utf8(sql)  # uicode to utf8  escape 和 en                                                                                 code公用会出问题,后面看看原因
        dtrans = DateShellTrans(sql)
        if oper == 'shell_to_date':
            ret = dtrans.replace_sql_shell_flag()
        elif oper == 'date_to_shell':
            ret = dtrans.replace_sql_pt_2_shell()
        self.finish(str({"ret": ret}))

class CreateSchemaHandler(tornado.web.RequestHandler):
    def post(self):
        sql = self.get_argument("sql", "")
        action = self.get_argument("action", "")
        sql = sql.encode('utf-8')
        hive_util = HiveSchemaCreate(sql)
        # print hive_util.hive_sql_to_mysql_scheme()
        if action == 'get_hive':
            schema = hive_util.hive_sql_to_hive_schema()
        elif action == 'get_mysql':
            schema = hive_util.hive_sql_to_mysql_scheme()
        self.write({"ret": schema})


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/date_shell_trans", TransHandler),
        (r"/create_schema", CreateSchemaHandler)


    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8902)
    tornado.ioloop.IOLoop.current().start()
