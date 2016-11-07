#!/usr/bin/env python
# encoding: utf-8
"""
views.py

Created by Maximillian Dornseif on 2010-11-20.
Copyright (c) 2010, 2016 HUDORA. All rights reserved.
"""
import logging
import metaphone

from cs.gaetk_common import make_app
from cs.gaetk_common import wwwHandler
from google.appengine.ext import ndb

import modules.sanctions.importer

from modules.sanctions.models import seEntity
from modules.sanctions.models import seName


class TechnikHandler(wwwHandler):
    """Wie funktioniert das ganze?"""
    def get(self):
        self.render({}, 'how.html')


class HintergrundHandler(wwwHandler):
    """Informationen über die Sanktionsliste."""
    def get(self):
        self.render({}, 'hintergrund.html')


class EntityHandler(wwwHandler):
    """Einen Eintrag der Sanktionsliste darstellen."""
    def get(self, eid, _name):
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
        """Query database for entities that have name that match the query"""

        querystring = querystring.lower().strip()
        if not querystring:
            return [], []
        logging.info(u'Searching for %s', querystring)

        query = seName.query().filter(seName.searchterms == querystring)
        keys = [name.sanc_entity for name in query.iter(batch_size=100)]
        matches = dict((entity.key, entity) for entity in ndb.get_multi(keys))

        query = seName.query().filter(
            seName.metaphones.IN([mp for mp in metaphone.dm(querystring) if mp]))
        keys = [name.sanc_entity for name in query.iter(batch_size=100) if name.sanc_entity not in matches]
        fuzzy_matches = dict((entity.key, entity) for entity in ndb.get_multi(keys))

        return matches, fuzzy_matches

    def get(self, fmt='html'):
        names = set(self.request.get('name', u'').strip().splitlines())
        matches = dict()
        fuzzymatches = dict()
        for name in names:
            entities, fuzzyentities = self.match(name)
            matches.update(entities)
            fuzzymatches.update(fuzzyentities)
            logging.info("search %s %s %s", name, entities, fuzzyentities)

        values = dict(names=sorted(names), results=matches.values(), fuzzyresults=fuzzymatches.values())
        self.multirender(fmt, values, html_template='search.html')


class DownloadHandler(wwwHandler):
    """Update the embargo entries from the global.xml file."""
    def get(self):
        """Read the global.xml file and import each data entry."""
        row_cnt = modules.sanctions.importer.start_import()
        self.response.headers['content-type'] = 'text/plain; charset=utf-8'
        self.response.out.write('read %d entries from global.xml' % row_cnt)


class MainHandler(wwwHandler):
    """Homepage darstellen."""
    def get(self):
        # neuster Eintrag von entity.reg_date
        self.render({}, 'homepage.html')


application = make_app([
    (r'/entity/(\d+)/(.+)/', EntityHandler),
    (r'/technik-des-santionslistenscreenings/', TechnikHandler),
    (r'/hintergrund-der-embargolisten/', HintergrundHandler),
    (r'/pruefung\.(json|html)', SearchHandler),
    (r'/download/', DownloadHandler),
    (r'/', MainHandler),
])
