#!/usr/bin/env python
# encoding: utf-8
"""
views.py

Created by Maximillian Dornseif on 2010-11-20.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import config
config.imported = True

from gaetk import webapp2
from gaetk.handler import BasicHandler
from sanctions.models import Entity, Name
import logging
import metaphone


class TechnikHandler(BasicHandler):
    def get(self):
        self.render({}, 'how.html')


class HintergrundHandler(BasicHandler):
    def get(self):
        self.render({}, 'hintergrund.html')


class EntityHandler(BasicHandler):
    def get(self, eid, name):
        entity = Entity.all().filter('id = ', eid).get()
        entity.unpickle()
        self.render(dict(entity=entity), 'entity.html')


class SearchHandler(BasicHandler):
    """
    * If the user enters a Single name check if there is any match of their name with
    - "WHOLENAME"
    - "LASTNAME, FIRSTNAME"
    - "FIRSTNAME LASTNAME"
    - "FIRSTNAME MIDDLENAME LASTNAME"
    * No match on Gender, address, Title etc.
    * If there is a match display all information th the matched <ENTITY>,
      current timestamp, input name and version of the XML-File used.
      else display "no match"
    * In addition allow the user to enter several lines in a <textarea> or upload
      a file and check line by line if there is a match to the Embargo list.
      Display the information required above and a summary ("n entries checked,
      m matches", etc.)
    """

    def match(self, query):
        """Query database for entities that have names that match 'data'."""
        query = query.strip().lower()
        if not query:
            return [], []
        logging.info(query)
        names = Name.all().filter('searchterms =', query).fetch(25)
        entities = dict([(x.sanc_entity.id, x.sanc_entity) for x in names])
        mph = []
        for mp in metaphone.dm(query):
            mph.extend(Name.all().filter('metaphones =', mp).fetch(25))
        fuzzyentities = dict([(x.sanc_entity.id, x.sanc_entity) for x in mph if x.id not in entities])
        return entities.values(), fuzzyentities.values()

    def get(self):
        context = {}
        names = self.request.get('name', '').strip().split('\r\n')
        names = set(names)
        matches = set()
        for name in names:
            logging.info(name)
            entities, fuzzyentities = self.match(name.strip())
            matched = set(entities)
            matches = matches.union(matched)

        for match in matches:
            match.unpickle()
        context['names'] = names
        context['results'] = matches
        #context['number_of_entries'] = Name.objects.count()
        self.render(context, 'search.html')


class DownloadHandler(BasicHandler):
    """Update the embargo entries from the global.xml file."""
    def get(self):
        """Read the global.xml file and import each data entry."""
        import sanctions.importer
        row_cnt = sanctions.importer.read_chunks()
        self.response.headers['content-type'] = 'text/plain; charset=utf-8'
        self.response.out.write('read %d entries from global.xml' % row_cnt)


class MainHandler(BasicHandler):
    def get(self):
        self.render({}, 'homepage.html')


def main():
    application = webapp2.WSGIApplication(
    [
     ('/entity/(\d+)/(.+)/', EntityHandler),
     ('/technik-des-santionslistenscreenings/', TechnikHandler),
     ('/hintergrund-der-embargolisten/', HintergrundHandler),
     ('/pruefung/', SearchHandler),
     ('/download/', DownloadHandler),
     ('/', MainHandler),
    ],
    debug=True)
    application.run()


if __name__ == '__main__':
    main()
