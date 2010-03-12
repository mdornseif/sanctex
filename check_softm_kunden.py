#!/usr/bin/env python
# encoding: utf-8
"""
transfer_bdp.py -- Transfer Kundendatten to CouchDB to allof faster access.

Created by Maximillian Dornseif, Tobias Nockher on 2008-03-13.
Copyright (c) 2008 HUDORA GmbH. All rights reserved.
"""

__revision__ = "$Revision: 7410 $"


from django.core.management import setup_environ
import settings
setup_environ(settings)

import sys
import couchdb.client
from optparse import OptionParser
from husoftm.kunden import get_kundennummern, get_kunde

from sanctions.views import match
from sanctions.models import Name, Download

def parse_commandline(): 
    """Return options found in the commandline.""" 
    parser = OptionParser(version=True) 
    parser.version = "%%prog %s" % (__revision__.strip('$Revision: '))
    parser.description = ('Speichert Kundendaten in CouchDB')
    parser.set_usage('usage: %prog [options]')
    parser.add_option('--couch', action='store', default='http://couchdb.local.hudora.biz:5984',
                       help='Address of CouchDB server. [default: %default]')
    parser.add_option('--db', action='store', default='cs_address',
                      help='Database name [default: %default]')
    parser.add_option('--debug', action='store_true')
     
    options, args = parser.parse_args() 
    if args: 
        parser.error("incorrect number of arguments") 
    return options 


def get_kundennumemrs():
    """Holt eine Liste der Kundennummern, die uebertragen werden sollen."""
    return reversed(get_kundennummern())
    

def collect_names():
    kunden = {}
    for kdnnr in sorted(get_kundennumemrs()):
        kunden["SC%d" % kdnnr] = []
        data = vars(get_kunde(kdnnr))
        #kdnnr = str(kdnnr)
        if 'xxxx' in data.get('name1', ''):
            # unused entry
            continue
        doc = {'name1': data.get('name1', ''), 'name2': data.get('name2', ''), 'name3': data.get('name3', ''), 
               'strasse': data.get('strasse', ''),
               'land': data.get('land', ''), 'plz': data.get('plz', ''), 'ort': data.get('ort', ''),
               'tel': data.get('tel', ''), 'softmid': data.get('kundennr', ''),
                }
        kunden["SC%d" % kdnnr].append(doc['name1'])
        kunden["SC%d" % kdnnr].append(doc['name2'])
        kunden["SC%d" % kdnnr].append(doc['name3'])
        kunden["SC%d" % kdnnr].append(''.join([doc['name1'], doc['name2']]))
        kunden["SC%d" % kdnnr].append(''.join([doc['name1'], doc['name2'], doc['name3']]))
        kunden["SC%d" % kdnnr].append(' '.join([doc['name1'], doc['name2']]))
        kunden["SC%d" % kdnnr].append(' '.join([doc['name1'], doc['name2'], doc['name3']]))
        if len(kunden) > 30:
            break
    return kunden

def main():
    """Run the Datatransfer."""
    options = parse_commandline()
    download = Download.objects.latest('download_time')
    print "SanctEx - http://sanktionen.hudoracybernetics.com/"
    print "Aktuelle Liste zuletzt am", download.download_time, "geladen."
    print "(Versionsdatum:", download.version_date, ",",
    print Name.objects.count(), "Eintraege)."

    kunden = collect_names()
    varianten = set()
    for namen in kunden.values():
        for name in namen:
            if name.strip():
                varianten.add(name.strip())
    # varianten.add("Robert Mugabe")
    
    print "Datenquelle: Kundenstamm"
    print len(kunden), "Namens-Datensätze mit", len(varianten), "Schreibweisen geladen"
    print "* Matches:"
    for name in sorted(varianten):
        name = name.strip()
        entries = match(name)
        if entries:
            print name.encode('utf-8'), [x.id for x in entries]
    print "* Lauf beendet"

if __name__ == "__main__":
    main()
