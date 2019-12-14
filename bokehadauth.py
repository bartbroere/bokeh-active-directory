from typing import Optional, Awaitable
from urllib.request import BaseHandler

import easyad
from bokeh.server.auth_provider import AuthProvider
from tornado.escape import json_decode, url_escape, json_encode
from tornado.web import RequestHandler


class ActiveDirectoryAuthProvider(AuthProvider):

    def __init__(self):
        super().__init__()

    def get_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return json_decode(user_json)
        else:
            return None

    def get_login_url(self):
        return u"/login"


class LoginHandler(RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.render("login.html", next=self.get_argument("next", "/"))

    def post(self):
        self.ad = easyad.EasyAD()
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        is_authorised = self.ad.authenticate_user(username, password, json_safe=True)
        if is_authorised and username:
            self.set_secure_cookie("user", json_encode(username))
            self.redirect(self.get_argument("next", u"/"))
        else:
            error = u"?error=" + url_escape("Login incorrect.")
            self.redirect(u"/login" + error)
            self.clear_cookie("user")

# Code below needs to be handled by something in bokeh
# application = tornado.web.Application([
#     (r"/", MainHandler),
#     (r"/login", LoginHandler),
# ], cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")
