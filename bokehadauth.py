"""
bokehadauth.py, when hooked into Bokeh server, will require Active Directory login by users.

This module is meant to be specified as argument to a bokeh server.
bokeh serve --auth-module=bokehadauth.py [...]
"""

import easyad
from tornado.escape import json_decode, url_escape, json_encode
from tornado.web import RequestHandler


def get_user(request_handler):
    user_json = request_handler.get_secure_cookie("user")
    if user_json:
        return json_decode(user_json)
    else:
        return None


def get_login_url(request_handler):
    return u"/login"


class LoginHandler(RequestHandler):
    """
    The handler for logins. Bokeh promises to include a route to this handler
    """

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

