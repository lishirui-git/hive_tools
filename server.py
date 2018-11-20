#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-11-17
# @Author  : 殷帅

import os

import tornado.autoreload
import tornado.ioloop
import tornado.web
from tornado.options import define

settings = {'debug': True}

# open debug mode
define("debug", default=True, help="debug mode", type=bool)
settings = {'debug': True}

settings = dict(
    blog_title=u"dw hive tools ",
    debug=True
)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class TransHandler(tornado.web.RequestHandler):
    def get(self):
        select_sql = self.get_argument("select_sql", "")
        self.write(select_sql+"ddddd")
        # hc = HiveSchemaCreate()
        # hc.hive_sql_to_hive_schema()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/date_shell_trans/", TransHandler)
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8895)
    tornado.ioloop.IOLoop.current().start()
