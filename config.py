#!/usr/bin/env python
# encoding: utf-8
"""
config.py - general configuration sample for gaetk

Created by Maximillian Dornseif on 2010-09-28.
Copyright (c) 2010, 2016 HUDORA. All rights reserved.
"""

import os
import os.path
import sys

# ----8<-----------------------------------------
# common setup in all our apps
DEBUG = False
if os.environ.get('SERVER_NAME', '').startswith('dev-'):
    DEBUG = True
if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
    DEBUG = True

BASEDIR = os.path.dirname(__file__)
template_dirs = [
    os.path.join(BASEDIR, 'templates'),
    os.path.join(BASEDIR, 'lib', 'appengine-toolkit', 'templates'),
    os.path.join(BASEDIR, 'lib', 'CentralServices', 'templates')]
# ----8<-----------------------------------------

SENTRY_URL = ('https://5210fba32bd84f2f958ca1becd7dbb24:5fda0dc29292459fb75fd7577186cd5e'
              '@app.getsentry.com/94020')


def main():
    """show path for usage in scripts"""
    from . import lib
    lib.this_updated_paths = True
    print ':'.join(sys.path)

if __name__ == '__main__':
    main()
