#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by Maximillian Dornseif on 2009-11-15.
Copyright (c) 2009 HUDORA. All rights reserved.
"""

from django.conf.urls.defaults import *
from piston.authentication import HttpBasicAuthentication
from piston.doc import documentation_view
from piston.resource import Resource
from api.handlers import EntryHandler

entry_handler = Resource(EntryHandler)

urlpatterns = patterns('',
   url(r'^entry/', entry_handler, name='api_entry_handler'),
   # automated documentation
   url(r'^$', documentation_view),
)