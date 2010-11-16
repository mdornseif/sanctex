#!/usr/bin/env python
# encoding: utf-8

# created november 2009 by danielroseman for Hudora GmbH
from __future__ import with_statement

import os
import datetime
import logging
import urllib
import random
from xml.etree import cElementTree as ET

from django.db import connection
from django import http
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django import forms
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.utils.encoding import smart_unicode, smart_str

from sanctions.models import Download, Entity, Name, Address, Birth, Passport, Citizen, NameIndex, XmlPart

from google.appengine.api import urlfetch
from google.appengine.api.labs import taskqueue
from google.appengine.runtime import DeadlineExceededError

import metaphone


class mem: pass
mem.file_pos = 0

START_MARKER = '<ENTITY'
END_MARKER = '</ENTITY>'

def download(request):
    """
    View to trigger download function and show response to user.
    """
    try:
        mem.file_pos = int(request.GET['pos'])
    except KeyError:
        pass

    try:
        read_chunks()
    except DeadlineExceededError:
        taskqueue.add(url=reverse('download'),
                      method='GET',
                      params={'pos': mem.file_pos})

    return http.HttpResponse()


def read_chunks(file_pos=0):
    file_read_size = 100000
    content = ''

    with open(settings.SANCTIONS_PATH) as f:
        if mem.file_pos:
            f.seek(mem.file_pos)

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

                part = XmlPart.objects.create(data=data)
                taskqueue.add(url=reverse('import-sanctions'),
                              method='GET',
                              params={'part_pk': part.pk},
                              queue_name='sanctions-import')

            mem.file_pos += entity_end_pos
            content = content[entity_end_pos:]


def get_data():
    """
    Get data from server and return an ElementTree object.

    Separated for easier testing.
    """
    url = "http://ec.europa.eu/external_relations/cfsp/sanctions/list/version4/global/global.xml"
    response = urlfetch.fetch(url, deadline=10)
    return ET.fromstring(response.content)


def import_sanctions(request):
    """
    Download, parse and import XML file.

    Uses `yield` to stream data to response, giving user an idea that things
    are still happening.
    """

    try:
        pk = request.GET['part_pk']
    except KeyError:
        return http.HttpResponseBadRequest()

    entity = ET.fromstring(smart_str(XmlPart.objects.get(pk=pk).data, strings_only=True))

    e = Entity.objects.create(id=entity.get('Id'),
                              type=entity.get('Type'),
                              legal_basis=entity.get('legal_basis'),
                              reg_date=entity.get('reg_date') or None,
                              pdf_link=entity.get('pdf_link'),
                              programme=entity.get('programme'),
                              remark=entity.get('remark'),)

    for name in entity.findall('NAME'):
        n = Name.objects.create(id=name.get('Id'),
                                entity=e,
                                legal_basis=name.get('legal_basis'),
                                reg_date=name.get('reg_date') or None,
                                pdf_link=name.get('pdf_link'),
                                programme=name.get('programme'),
                                lastname=name.findtext('LASTNAME'),
                                firstname=name.findtext('FIRSTNAME'),
                                middlename=name.findtext('MIDDLENAME'),
                                wholename=name.findtext('WHOLENAME'),
                                gender=name.findtext('GENDER'),
                                title=name.findtext('TITLE'),
                                function=name.findtext('FUNCTION'),
                                language=name.findtext('LANGUAGE'),)

    for address in entity.findall('ADDRESS'):
        a = Address.objects.create(id=address.get('Id'),
                                   entity=e,
                                   legal_basis=address.get('legal_basis'),
                                   reg_date=address.get('reg_date') or None,
                                   pdf_link=address.get('pdf_link'),
                                   programme=address.get('programme'),
                                   number=address.findtext('NUMBER'),
                                   street=address.findtext('STREET'),
                                   city=address.findtext('CITY'),
                                   zipcode=address.findtext('ZIPCODE'),
                                   country=address.findtext('COUNTRY'),
                                   other=address.findtext('OTHER'),)

    for birth in entity.findall('BIRTH'):
        b = Birth.objects.create(id=birth.get('Id'),
                                 entity=e,
                                 legal_basis=birth.get('legal_basis'),
                                 reg_date=birth.get('reg_date') or None,
                                 pdf_link=birth.get('pdf_link'),
                                 programme=birth.get('programme'),
                                 date=birth.findtext('DATE'),
                                 place=birth.findtext('PLACE'),
                                 country=birth.findtext('COUNTRY'),)

    for passport in entity.findall('PASSPORT'):
        p = Passport.objects.create(id=passport.get('Id'),
                                    entity=e,
                                    legal_basis=passport.get('legal_basis'),
                                    reg_date=passport.get('reg_date') or None,
                                    pdf_link=passport.get('pdf_link'),
                                    programme=passport.get('programme'),
                                    number=passport.findtext('NUMBER'),
                                    country=passport.findtext('COUNTRY'),)

    for citizen in entity.findall('CITIZEN'):
        c = Citizen.objects.create(id=citizen.get('Id'),
                                   entity=e,
                                   legal_basis=citizen.get('legal_basis'),
                                   reg_date=citizen.get('reg_date') or None,
                                   pdf_link=citizen.get('pdf_link'),
                                   programme=citizen.get('programme'),
                                   country=citizen.findtext('COUNTRY'),)

    return http.HttpResponse()


class SearchForm(forms.Form):
    """
    Form containing search fields.
    """
    name = forms.CharField(required=False)
    mehrere_Namen = forms.CharField(widget=forms.Textarea, required=False)
    datei_Hochladen = forms.FileField(required=False)


def match(data):
    """
    Query database for entities that have names that match 'data'.
    """
    if not data:
        return []

    data = smart_unicode(data, strings_only=True).lower()

    metaphones = []
    m1, m2 = metaphone.dm(data)
    if m1:
        metaphones.append(m1)
    if m2:
        metaphones.append(m2)

    names = NameIndex.objects.filter(name_variant__gte=data, name_variant__lt=data+u"\ufffd")
    ids = [name.entity_id for name in names]

    names = NameIndex.objects.filter(metaphones__in=metaphones)
    ids.extend([name.entity_id for name in names])

    entities = Entity.objects.filter(id__in=ids)

    return entities


def search(request):

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

    context = {}

    if request.GET:
        form = SearchForm(request.GET, request.FILES)

        if form.is_valid():
            names = []
            if form.cleaned_data.get('name'):
                names.append(form.cleaned_data['name'])
            if form.cleaned_data.get('mehrere_Namen'):
                names.extend(form.cleaned_data['mehrere_Namen'].split('\r\n'))
            if form.cleaned_data.get('datei_Hochladen'):
                names.extend(form.cleaned_data['datei_Hochladen'].readlines())
            names = set(names)
            matches = set()
            for name in names:
                matched = set(match(name.strip()))
                matches = matches.union(matched)

            context['names'] = names
            context['results'] = matches
    else:
        form = SearchForm()
    context['form'] = form
    context['number_of_entries'] = Name.objects.count()
    return render_to_response('sanctions/search.html', context)
