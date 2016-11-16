#!/usr/bin/env python
# encoding: utf-8
"""
importer.py - import data into sanctex

Created by Maximillian Dornseif on 2010-11-21.
Copyright (c) 2010, 2016 HUDORA. All rights reserved.
"""

import logging

from xml.etree import cElementTree as ET

import huTools.http
import metaphone

from google.appengine.ext import deferred
from google.appengine.ext import ndb
from modules.sanctions.models import seEntity
from modules.sanctions.models import seName


START_MARKER = '<ENTITY'
END_MARKER = '</ENTITY>'


def import_sanktion(xml):
    """Eine einzelne Sanktion mit ihrem XML-Fragment importieren."""
    logging.debug("xml: %s", xml)
    entity = ET.fromstring(xml)
    e = seEntity(
        id=entity.get('Id'),
        typ=entity.get('Type'),
        legal_basis=entity.get('legal_basis'),
        reg_date=entity.get('reg_date'),
        pdf_link=entity.get('pdf_link'),
        programme=entity.get('programme'),
        remark=entity.get('remark'))
    e.put()
    putlist = [e]
    addon_data = {}
    for name in entity.findall('NAME'):
        searchterms = [
            name.findtext('WHOLENAME'),
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
        n = seName(
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
        n.sanc_entity = e.key
        n.put()
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
    logging.info("%s addon: %r", n.wholename, addon_data)
    e.addon_data = addon_data
    e.put()
    ndb.put_multi(putlist)


def start_import():
    """Sanktionsliste herunterladen, Tasks starten."""
    # from http://eeas.europa.eu/cfsp/sanctions/consol-list/index_en.htm
    _status, _headers, content = huTools.http.fetch2xx(
        'http://ec.europa.eu/external_relations/cfsp/sanctions/list/version4/global/global.xml',
    )
    logging.info("downloaded %d bytes", len(content))
    row_cnt = 0
    content = content[:]
    entity_start_pos = 0
    entity_end_pos = 0
    while True:
        try:
            entity_start_pos = content.index(START_MARKER, entity_end_pos)
            entity_end_pos = content.index(END_MARKER, entity_start_pos) + len(END_MARKER)
        except ValueError:
            break
        data = content[entity_start_pos:entity_end_pos]
        deferred.defer(import_sanktion, data)
        row_cnt += 1
    # shorten content
    content = content[entity_end_pos:]
    return row_cnt
