# bokeh-active-directory
Active Directory authentication for Bokeh servers

``bokehadauth.py``, when hooked into Bokeh server, will require Active Directory login by users.
Currently, it expects the environment variables ``AD_SERVER`` and ``AD_DOMAIN`` to be set correctly.
This module is meant to be specified as argument to a bokeh server.
``bokeh serve --auth-module=bokehadauth.py --cookie-secret YOURSECRETHERE [...]``

# Resources
+ https://docs.bokeh.org/en/latest/docs/user_guide/server.html#authentication
+ https://stackoverflow.com/questions/6514783/tornado-login-examples-tutorials
+ https://www.tornadoweb.org/en/stable/guide/security.html
+ https://codepen.io/miroot/pen/qwIgC
