#!/usr/bin/env python
# encoding: utf-8
"""
views.py

Created by Maximillian Dornseif on 2010-11-20.
Copyright (c) 2010, 2016 HUDORA. All rights reserved.
"""

import config
config.imported = True

import logging
import metaphone

from cs.gaetk_common import make_app
from cs.gaetk_common import wwwHandler
from gaetk import webapp2
from google.appengine.ext import ndb

from sanctions.models import seEntity
from sanctions.models import seName


class TechnikHandler(wwwHandler):
    def get(self):
        self.render({}, 'how.html')


class HintergrundHandler(wwwHandler):
    def get(self):
        self.render({}, 'hintergrund.html')


class EntityHandler(wwwHandler):
    def get(self, eid, name):
        entity = seEntity.get_by_id(eid)
        self.render(dict(entity=entity), 'entity.html')


class SearchHandler(wwwHandler):
    """
    * If the user enters a Single name check if there is any match of their NAME with
    - "WHOLENAME"
    - "LASTNAME, FIRSTNAME"
    - "FIRSTNAME LASTNAME"
    - "FIRSTNAME MIDDLENAME LASTNAME"
    * No match on Gender, address, Title etc.
    * If there is a match display all information th the matched <seEntity>,
      current timestamp, input name and version of the XML-File used.
      else display "no match"
    * In addition allow the user to enter several lines in a <textarea> or upload
      a file and check line by line if there is a match to the Embargo list.
      Display the information required above and a summary ("n entries checked,
      m matches", etc.)
    """

    def match(self, querystring):
        """Query database for entities that have name that match 'data'."""
        querystring = querystring.strip().lower()
        if not querystring:
            return [], []
        logging.info(querystring)
        names = seName.query().filter(seName.searchterms==querystring).fetch(25)
        list_of_entities = ndb.get_multi([x.sanc_entity for x in names])
        entities = dict([(x.key, x) for x in list_of_entities])
        mph = []
        for mp in metaphone.dm(querystring):
            mph.extend(seName.query().filter(seName.metaphones==mp).fetch(25))
        list_of_entities = ndb.get_multi([x.sanc_entity for x in mph])
        fuzzyentities = dict([(x.key, x) for x in list_of_entities if x.key not in entities])
        return entities, fuzzyentities

    def get(self):
        context = {}
        names = self.request.get('name', '').strip().split('\r\n')
        names = set(names)
        matches = dict()
        fuzzymatches = dict()
        for name in names:
            entities, fuzzyentities = self.match(name.strip())
            matches.update(entities)
            fuzzymatches.update(fuzzyentities)
            logging.info("search %s %s %s", name, entities, fuzzyentities)

        context['names'] = names
        context['results'] = matches.values()
        context['fuzzyresults'] = matches.values()
        self.render(context, 'search.html')


class DownloadHandler(wwwHandler):
    """Update the embargo entries from the global.xml file."""
    def get(self):
        """Read the global.xml file and import each data entry."""
        import sanctions.importer
        row_cnt = sanctions.importer.read_chunks()
        self.response.headers['content-type'] = 'text/plain; charset=utf-8'
        self.response.out.write('read %d entries from global.xml' % row_cnt)


class MainHandler(wwwHandler):
    def get(self):
        self.render({}, 'homepage.html')


application = make_app([
     (r'/entity/(\d+)/(.+)/', EntityHandler),
     (r'/technik-des-santionslistenscreenings/', TechnikHandler),
     (r'/hintergrund-der-embargolisten/', HintergrundHandler),
     (r'/pruefung/', SearchHandler),
     (r'/download/', DownloadHandler),
     (r'/', MainHandler),
])
