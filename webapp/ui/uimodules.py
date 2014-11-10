# -*- coding: utf-8 -*-

__author__ = 'hendro'

from tornado.web import UIModule

class Entry(UIModule):
    def render(self, entry, **kwargs):
        return self.render_string(
            "views/_layout/layout.html", entry=entry, **kwargs)