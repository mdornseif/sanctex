#!/usr/bin/env python
# encoding: utf-8
"""
Tests for Sanctex

Based on resttets.py by Benjamin Köppchen.
Created by Christian Klein on 2011-10-06.
Copyright (c) 2011 HUDORA GmbH. All rights reserved.
"""

import sys
from resttest_dsl import get_app_version, create_testclient_from_cli


def main():
    """Main Entry Point"""

    client = create_testclient_from_cli(default_hostname='%s.sanktex.appspot.com' % get_app_version())

    client.GET('/').responds_http_status(200)
    client.GET('/pruefung/').responds_http_status(200)
    client.GET('/pruefung/?name=Robert+Mugabe').responds_http_status(200)
    client.GET('/entity/1/robert_mugabe/').responds_http_status(200)

    client.GET('/technik-des-santionslistenscreenings/').responds_http_status(200)
    client.GET('/hintergrund-der-embargolisten/').responds_http_status(200)

    client.GET('/nonexistent/').responds_http_status(404)

    print "Errors: %s" % client.errors
    sys.exit(client.errors)


if __name__ == "__main__":
    main()
