#!/usr/bin/env python
# encoding: utf-8
"""
importer.py - import data into sanctex

Created by Maximillian Dornseif on 2010-11-21.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import config
config.imported = True

import metaphone
import pickle

from google.appengine.ext import db
from google.appengine.ext import deferred
from sanctions.models import Entity
from sanctions.models import Name
from xml.etree import cElementTree as ET


class mem:
    pass

mem.file_pos = 0
START_MARKER = '<ENTITY'
END_MARKER = '</ENTITY>'


def import_sanktion(xml):
    entity = ET.fromstring(xml)
    e = Entity(key_name=entity.get('Id'),
               id=entity.get('Id'),
               type=entity.get('Type'),
               legal_basis=entity.get('legal_basis'),
               reg_date=entity.get('reg_date'),
               pdf_link=entity.get('pdf_link'),
               programme=entity.get('programme'),
               remark=entity.get('remark'))
    putlist = [e]
    addon_data = {}
    for name in entity.findall('NAME'):
        searchterms = [name.findtext('WHOLENAME'),
            '%s %s' % (name.findtext('FIRSTNAME'), name.findtext('LASTNAME')),
            '%s, %s' % (name.findtext('LASTNAME'), name.findtext('FIRSTNAME')),
            ]
        if name.findtext('MIDDLENAME'):
            searchterms.append('%s %s %s' % (name.findtext('FIRSTNAME'), name.findtext('MIDDLENAME'),
                                             name.findtext('LASTNAME')))

        searchterms = list(set([x.strip(' ,').lower() for x in searchterms if x.strip(' ,')]))
        metaphones = []
        for searchterm in searchterms:
            metaphones.extend([x for x in metaphone.dm(unicode(searchterm)) if x])
        n = Name(key_name=name.get('Id'),
                 id=name.get('Id'),
                 legal_basis=name.get('legal_basis'),
                 pdf_link=name.get('pdf_link'),
                 programme=name.get('programme'),
                 lastname=name.findtext('LASTNAME'),
                 firstname=name.findtext('FIRSTNAME'),
                 middlename=name.findtext('MIDDLENAME'),
                 wholename=name.findtext('WHOLENAME'),
                 gender=name.findtext('GENDER'),
                 title=name.findtext('TITLE'),
                 function=name.findtext('FUNCTION'),
                 language=name.findtext('LANGUAGE'),
                 searchterms=searchterms,
                 metaphones=metaphones)
        n.reg_date = name.get('reg_date')
        n.sanc_entity = e
        putlist.append(n)
    for address in entity.findall('ADDRESS'):
        d = dict(legal_basis=address.get('legal_basis'),
                 reg_date=address.get('reg_date') or None,
                 pdf_link=address.get('pdf_link'),
                 programme=address.get('programme'),
                 number=address.findtext('NUMBER'),
                 street=address.findtext('STREET'),
                 city=address.findtext('CITY'),
                 zipcode=address.findtext('ZIPCODE'),
                 country=address.findtext('COUNTRY'),
                 other=address.findtext('OTHER'))
        addon_data.setdefault('addresses', []).append(d)
    for birth in entity.findall('BIRTH'):
        d = dict(id=birth.get('Id'),
                 legal_basis=birth.get('legal_basis'),
                 reg_date=birth.get('reg_date') or None,
                 pdf_link=birth.get('pdf_link'),
                 programme=birth.get('programme'),
                 date=birth.findtext('DATE'),
                 place=birth.findtext('PLACE'),
                 country=birth.findtext('COUNTRY'))
        addon_data.setdefault('births', []).append(d)
    for passport in entity.findall('PASSPORT'):
        d = dict(id=passport.get('Id'),
                 legal_basis=passport.get('legal_basis'),
                 reg_date=passport.get('reg_date') or None,
                 pdf_link=passport.get('pdf_link'),
                 programme=passport.get('programme'),
                 number=passport.findtext('NUMBER'),
                 country=passport.findtext('COUNTRY'))
        addon_data.setdefault('passports', []).append(d)
    for citizen in entity.findall('CITIZEN'):
        d = dict(id=citizen.get('Id'),
                 legal_basis=citizen.get('legal_basis'),
                 reg_date=citizen.get('reg_date') or None,
                 pdf_link=citizen.get('pdf_link'),
                 programme=citizen.get('programme'),
                 country=citizen.findtext('COUNTRY'))
        addon_data.setdefault('citizenship', []).append(d)
    e.addon_data = pickle.dumps(addon_data, 2)
    db.put(putlist)


def read_chunks(file_pos=0):
    row_cnt = 0
    file_read_size = 100000
    content = ''
    f = open('./global.xml')
    #if mem.file_pos:
    #    f.seek(mem.file_pos)
    while True:
        chunk = f.read(file_read_size)
        if not chunk:
            break
        content += chunk
        entity_start_pos = 0
        entity_end_pos = 0
        while True:
            try:
                entity_start_pos = content.index(START_MARKER, entity_end_pos)
                entity_end_pos = content.index('</ENTITY>', entity_start_pos) + len(END_MARKER)
            except ValueError:
                break
            data = content[entity_start_pos:entity_end_pos]
            #import_sanktion(data)
            deferred.defer(import_sanktion, data)
            row_cnt += 1

        mem.file_pos += entity_end_pos
        content = content[entity_end_pos:]
    return row_cnt
