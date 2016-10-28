#!/usr/bin/env python
# encoding: utf-8
"""
importer.py - import data into sanctex

Created by Maximillian Dornseif on 2010-11-21.
Copyright (c) 2010, 2016 HUDORA. All rights reserved.
"""
import logging
import metaphone

from lxml import etree

from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from sanctions.models import seEntity
from sanctions.models import seName


def get_data(elem):
    data = dict(elem.attrib)
    data['id'] = data.pop('Id')
    del data['Entity_id']

    data.update((child.tag.lower(), child.text or u'') for child in elem.iterchildren())
    return data


def parse_entity(entity):

    addon_data = dict(
        addresses=[get_data(address) for address in entity.iterfind('ADDRESS')],
        births=[get_data(birth) for birth in entity.iterfind('BIRTH')],
        passports=[get_data(passport) for passport in entity.iterfind('PASSPORT')],
        citizenship=[get_data(citizen) for citizen in entity.iterfind('CITIZEN')]
    )

    key = ndb.Key(seEntity, entity.get('Id'))

    yield seEntity(
        key=key,
        typ=entity.get('Type'),
        legal_basis=entity.get('legal_basis'),
        reg_date=entity.get('reg_date'),
        pdf_link=entity.get('pdf_link'),
        programme=entity.get('programme'),
        remark=entity.get('remark'),
        addon_data=addon_data)

    for name in entity.iterfind('NAME'):
        firstname = name.findtext('FIRSTNAME')
        lastname = name.findtext('LASTNAME')
        middlename = name.findtext('MIDDLENAME')

        searchterms = set((
            unicode(name.findtext('WHOLENAME', '').lower()),
            (u'%s %s' % (firstname, lastname)).strip(' ,').lower(),
            (u'%s, %s' % (lastname, firstname)).strip(' ,').lower(),
            (u'%s %s %s' % (firstname, middlename, lastname)).strip(', ').lower(),
        ))

        metaphones = set()
        for searchterm in searchterms:
            metaphones.update((x for x in metaphone.dm(searchterm) if x))

        yield seName(
            id=name.get('Id'),
            reg_date=name.get('reg_date'),
            sanc_entity=key,
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


def get_root():
    """Return parsed XML document"""

    url = 'http://ec.europa.eu/external_relations/cfsp/sanctions/list/version4/global/global.xml'
    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    result = urlfetch.fetch(url)
    return etree.fromstring(result.content, parser=parser)


def parse():
    """Parse data from XML tree"""

    batch_size = 700

    root = get_root()
    row_cnt = 0
    writelist = []
    for element in root:
        row_cnt += 1
        if row_cnt % 100 == 0:
            logging.debug(u'rows: %s', row_cnt)

        writelist.extend(parse_entity(element))
        if len(writelist) > batch_size:
            ndb.put_multi(writelist)
            writelist = []

    ndb.put_multi(writelist)
    return row_cnt
