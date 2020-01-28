"""
bokehadauth.py, when hooked into Bokeh server, will require Active Directory login by users.
Currently, it expects the environment variables AD_SERVER and AD_DOMAIN to be set correctly.

This module is meant to be specified as argument to a bokeh server.
bokeh serve --auth-module=bokehadauth.py --cookie-secret YOURSECRETHERE [...]
"""
import os

import easyad
from tornado.escape import json_decode, url_escape, json_encode
from tornado.web import RequestHandler


def get_user(request_handler):
    user_json = request_handler.get_secure_cookie("user")
    if user_json:
        return json_decode(user_json)
    else:
        return None


login_url = "/login"


class LoginHandler(RequestHandler):
    """
    The handler for logins. Bokeh promises to include a route to this handler
    """

    def get(self):
        self.render("login.html", next=self.get_argument("next", "/"))

    def post(self):
        self.ad = easyad.EasyAD({'AD_SERVER': os.environ.get('AD_SERVER', None),
                                 'AD_DOMAIN': os.environ.get('AD_DOMAIN', None)})
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        is_authorised = self.ad.authenticate_user(username, password, json_safe=True)
        if is_authorised and username:
            self.set_secure_cookie("user", json_encode(username))
            self.redirect(self.get_argument("next", "/"))
        else:
            error = "?error=" + url_escape("Login incorrect.")
            self.redirect("/login" + error)
            self.clear_cookie("user")
