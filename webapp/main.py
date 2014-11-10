#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

__author__ = 'hendro'

from os import getcwd

from tornado.web import Application, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options

from summarizer import SummarizeContent
# from prediction import Prediction
from console import HomeHandler, InformationHandler, LoginHandler, LogoutHandler
from config import SECRET

import unittest

define("port", default=1421)
define("debug", default=True)
define("secret", default=SECRET)

routes = [
    # Routes definition for RESTFUL API
    (r"/rest/summarize", SummarizeContent),
    #(r"/rest/prediction", Prediction),

    # Routes definition for Engine Console/Web Interface
    (r"/", HomeHandler),
    (r"/engine/console", HomeHandler),
    (r"/engine/console/login", LoginHandler),
    (r"/engine/console/logout", LogoutHandler),
    (r"/engine/console/home", HomeHandler),
    (r"/engine/console/informations", InformationHandler),
    (r'/assets/(.*)', StaticFileHandler, {'path': "{}/theme/".format(getcwd())})
]

if __name__ == "__main__":
    opts = {
        "debug": options.debug,
        "cookie_secret": options.secret
    }

    application = Application(handlers=routes, **opts)
    application.listen(options.port)

    IOLoop.instance().start()