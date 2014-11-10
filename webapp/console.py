# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

__author__ = 'hendro'

from tornado.web import RequestHandler

from library.AutoVivification import AutoVivification
from library.helpers import send_request, is_engine_activated, load_engine_db
from config import USERNAME, PASSWORD, APP_NAME, DB_PATH

import requests

class BaseHandler(RequestHandler):
    scrapyd_api_url = "http://engine.lintas.me:6800"
    
    def set_default_headers(self):
        self.set_header("Server", "LintasEngineServer/0.1")

    def get_current_user(self):
        return self.get_secure_cookie("username")

class LoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect('/engine/console/home')
            return
        self.render('views/page_login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username == USERNAME and password == PASSWORD:
            self.set_secure_cookie("username", USERNAME, expires_days=5)
            self.redirect("/engine/console/home")

class LogoutHandler(BaseHandler):
    def get(self):
        if not self.get_current_user():
            self.redirect('/engine/console/login')
            return

        self.clear_cookie("username")
        self.redirect('/engine/console/login')

class HomeHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            self.redirect("/engine/console/login")
            return

        engine_config = load_engine_db(DB_PATH)
        engines = engine_config['engine']
        try:
            post_to_lintas = engine_config['post_to_lintas']
        except KeyError:
            post_to_lintas = "No"
        engine_count = len(engines)
        engine_list = AutoVivification()
        for engine in engines:
            engine_list[engine]['status'] = "ACTIVE" if is_engine_activated(engine.lower()) else "INACTIVE"
            engine_list[engine]['cmd'] = engines[engine]['cmd']
            engine_list[engine]['minute_run_at'] = engines[engine]['run_at'][0]
            engine_list[engine]['hour_run_at'] = engines[engine]['run_at'][1]
        try:
            running_project = "text-primary|" + send_request("%s/listprojects.json" % self.scrapyd_api_url)['projects'][0]
            running_spider = "text-primary|" + send_request("%s/listspiders.json?project=%s" % (self.scrapyd_api_url, running_project.split('|')[1]))['spiders'][0]
            project_version = "text-primary|" + send_request("%s/listversions.json?project=%s" % (self.scrapyd_api_url, running_project.split('|')[1]))['versions'][0]
        except requests.ConnectionError:
            running_project = "text-danger|CRAWLER SERVER IS DOWN"
            running_spider = "text-danger|CRAWLER SERVER IS DOWN"
            project_version = "text-danger|CRAWLER SERVER IS DOWN"
        except IndexError:
            running_project = "text-danger|NO CRAWLER PROJECT RUNNING"
            running_spider = "text-danger|NO CRAWLER PROJECT RUNNING"
            project_version = "text-danger|NO CRAWLER PROJECT RUNNING"

        self.render('views/main.html', title=APP_NAME, name=user, \
                    running_project=running_project, running_spider=running_spider, \
                    project_version=project_version, engine_count=engine_count, \
                    engines=engine_list, post_to_lintas=post_to_lintas)

class InformationHandler(BaseHandler):

    def get(self):
        user = self.get_current_user()
        if not user:
            self.redirect("/engine/console/login")
            return

        engine_count = len(load_engine_db(DB_PATH)['engine'])
        try:
            running_project = "text-primary|" + send_request("%s/listprojects.json" % \
                            (self.scrapyd_api_url))['projects'][0]
            running_spider = "text-primary|" + send_request("%s/listspiders.json?project=%s" % \
                            (self.scrapyd_api_url, running_project.split('|')[1]))['spiders'][0]
            project_version = "text-primary|" + send_request("%s/listversions.json?project=%s" % \
                            (self.scrapyd_api_url, running_project.split('|')[1]))['versions'][0]
        except requests.ConnectionError:
            running_project = "text-danger|CRAWLER SERVER IS DOWN"
            running_spider = "text-danger|CRAWLER SERVER IS DOWN"
            project_version = "text-danger|CRAWLER SERVER IS DOWN"
        except IndexError:
            running_project = "text-danger|NO CRAWLER PROJECT RUNNING"
            running_spider = "text-danger|NO CRAWLER PROJECT RUNNING"
            project_version = "text-danger|NO CRAWLER PROJECT RUNNING"

        self.render('views/informations.html', title=APP_NAME, name=user, \
                    running_project=running_project, running_spider=running_spider, \
                    project_version=project_version, engine_count=engine_count)