"""Configuration for each AppEngine Instance"""

# pylint: skip-file

# monkeypatch from
import logging
import webob.exc

def _new_WSGIHTTPException__call__(self, environ, start_response):
    "webob.exc.HTTPException with decent logging"

    detail = getattr(self, 'detail', '')
    if getattr(self, 'location', None):
        text = 'redirect to %r' % getattr(self, 'location', None)
        if not detail:
            detail = text
        else:
            detail = "%s (%s)" % (detail, text)
    if detail:
        if getattr(self, 'code', 400) < 400:
            logging.info("HTTP%s: %s", getattr(self, 'code', '???'), detail)
        else:
            logging.warning("HTTP%s: %s", getattr(self, 'code', '???'), detail)
    if getattr(self, 'comment', None):
        logging.info("%s", self.comment)
    return webob.exc.WSGIHTTPException.__oldcall__(self, environ, start_response)

webob.exc.WSGIHTTPException.__oldcall__ = webob.exc.WSGIHTTPException.__call__
webob.exc.WSGIHTTPException.__call__ = _new_WSGIHTTPException__call__


# Libraries einbinden
from google.appengine.ext import vendor
from site import addsitedir
vendor.add('lib/site-packages')
addsitedir('lib')

import cs.gaetk_common

from cs.gaetk_common import gae_mini_profiler_should_profile_production  # pylint: disable=W0611
from cs.gaetk_common import webapp_add_wsgi_middleware  # pylint: disable=W0611

import config  # pylint: disable=W0611

cs.gaetk_common.init_appengine_config()
