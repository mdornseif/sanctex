#!/usr/bin/env python
# encoding: utf-8
"""
embargolist.client - client for the embargolist.api

Created by Maximillian Dornseif on 2009-11-22.
Copyright (c) 2009 HUDORA. All rights reserved.
"""

import httplib2
import simplejson as json

def name_ok(name):
    """Checks if a Name is on the Embargolist. Returns False in Match and True on miss."""
    h = httplib2.Http()
    resp, content = h.request("http://api.local.hudora.biz/embargolist/api/entry/",
                              "POST", body=name,
                              headers={'content-type':'text/plain'})
    assert resp.status != '200'
    if json.loads(content) == []:
        return True
    return False

# print name_ok("Maximillian Dornseif")
# print name_ok("Robert Mugabe")