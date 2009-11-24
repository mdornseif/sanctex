#!/usr/bin/env python
# encoding: utf-8
"""
handlers.py - API handling methods

Created by Maximillian Dornseif on 2009-11-15.
Copyright (c) 2009 HUDORA. All rights reserved.
"""

from piston.handler import BaseHandler
import sanctions.views
from sanctions.models import Download

class EntryHandler(BaseHandler):
    """Check for a single Name if it's on one of the lists.
    
    Returns a empy JSON lsit if there are no matches:
    
    $ curl -X POST -d 'Peter Hacker' http://127.0.0.1:8000/api/entry/
    []
    
    If thete are matches a list of dicts is returned listing the reasons this Address matches:
    
    
    curl -X POST -d 'Robert Mugabe' http://127.0.0.1:8000/api/entry/y/
    [
        {
            "passports": [
                {
                    "entity_id": 1, 
                    "country": "", 
                    "legal_basis": "77/2009 (OJ L 23)", 
                    "number": "AD001095", 
                    "reg_date": "2009-01-27", 
                    "pdf_link": "http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF", 
                    "id": 315, 
                    "programme": "ZWE"
                }
            ], 
            "remark": "Date of designation referred to in Article 7 (2): 21.2.2002. Head of Government and as such responsible for activities that seriously undermine democracy, respect for human rights and the rule of law.", 
            "birthdays": [
                {
                    "entity_id": 1, 
                    "country": "", 
                    "legal_basis": "898/2005 (OJ L 153)", 
                    "reg_date": "2005-06-16", 
                    "place": "", 
                    "pdf_link": "http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf", 
                    "date": "1924-02-21", 
                    "id": 1, 
                    "programme": "ZWE"
                }
            ], 
            "names": [
                {
                    "function": "President", 
                    "entity_id": 1, 
                    "language": "", 
                    "firstname": "Robert", 
                    "title": "", 
                    "middlename": "Gabriel", 
                    "lastname": "Mugabe", 
                    "legal_basis": "898/2005 (OJ L 153)", 
                    "reg_date": "2005-06-16", 
                    "pdf_link": "http://eur-lex.europa.eu/lex/LexUriServ/site/en/oj/2005/l_153/l_15320050616en00090014.pdf", 
                    "gender": "M", 
                    "wholename": "", 
                    "id": 1, 
                    "programme": "ZWE"
                }
            ], 
            "addresses": [], 
            "legal_basis": "77/2009 (OJ L 23)", 
            "citizenships": [], 
            "reg_date": "2009-01-27", 
            "pdf_link": "http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2009:023:0005:0024:EN:PDF", 
            "type": "P", 
            "id": 1, 
            "programme": "ZWE"
        }
    ]
    
    See embargoliste.client for a simple client for this.
    
    """
    allowed_methods = ('POST',)
    
    def create(self, request):
        "Prüfe, ob ein einzelner Name auf der Embargoliste steht."
        name = request.raw_post_data.strip()
        matches = sanctions.views.match(name)
        ret = []
        for match in matches:
            match.addresses = list(match.address_set.all())
            match.birthdays = list(match.birth_set.all())
            match.citizenships = list(match.citizen_set.all())
            match.names = list(match.name_set.all())
            match.passports = list(match.passport_set.all())
            ret.append(match)
        #download =  Download.objects.latest('download_time')
        #ret = {'file_version': download.version_date}
        return ret
    
    @staticmethod
    def resource_uri():
        return ('api_entry_handler')

