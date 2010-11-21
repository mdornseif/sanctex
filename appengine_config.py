"""Configuration for each AppEngine Instance"""

import config
config.imported = True

from gaetk.gaesessions import SessionMiddleware
COOKIE_KEY = '8614122a4ea8147ffa336bbe5d733f79-5a17'


def webapp_add_wsgi_middleware(app):
    """Called with each WSGI handler initialisation """
    app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
    # For profiling:
    # from google.appengine.ext.appstats import recording
    # app = recording.appstats_wsgi_middleware(app)
    return app
