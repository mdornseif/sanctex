#!/usr/bin/env python
# encoding: utf-8

# created november 2009 by danielroseman for Hudora GmbH

import datetime
import logging
import urllib
import random
from xml.etree import cElementTree as ET

from django.db import connection
from django.http import HttpResponse
from django import forms
from django.shortcuts import render_to_response

from sanctions.models import Download, Entity, Name, Address, Birth, Passport, Citizen
#o.wozniak
from django.contrib.auth import authenticate, login


def download(request):
    """
    View to trigger download function and show response to user.
    """
    Entity.objects.all().delete()
    try:
        return HttpResponse(import_sanctions())
    except Exception, e:
        msg= 'Error found: %s<br><a href="/">Return to search</a>' % e
        return HttpResponse(msg)

def get_data():
    """
    Get data from server and return an ElementTree object.
    
    Separated for easier testing.
    """
    url = "http://ec.europa.eu/external_relations/cfsp/sanctions/list/version4/global/global.xml"
    #url = "global.xml"
    response = urllib.urlopen(url)
    return ET.parse(response).getroot()

def import_sanctions():
    """
    Download, parse and import XML file.
    
    Uses `yield` to stream data to response, giving user an idea that things
    are still happening.
    """
    
    yield "Downloading ..."
    data = get_data()
    
    # import pdb;pdb.set_trace()
    version_date = datetime.datetime.strptime(data.get('Date'), '%d/%m/%Y').date()
    Download.objects.create(version_date=version_date)
    for entity in data.findall('ENTITY'):
        e = Entity.objects.create(
            id=entity.get('Id'),
            type=entity.get('Type'),
            legal_basis=entity.get('legal_basis'),
            reg_date=entity.get('reg_date') or None,
            pdf_link=entity.get('pdf_link'),
            programme=entity.get('programme'),
            remark=entity.get('remark'),
        )
        for name in entity.findall('NAME'):
            n = Name.objects.create(
                id=name.get('Id'),
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
                language=name.findtext('LANGUAGE'),
            )

        for address in entity.findall('ADDRESS'):
            a = Address.objects.create(
                id=address.get('Id'),
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
                other=address.findtext('OTHER'),
            )
        for birth in entity.findall('BIRTH'):
            b = Birth.objects.create(
                id=birth.get('Id'),
                entity=e,
                legal_basis=birth.get('legal_basis'),
                reg_date=birth.get('reg_date') or None,
                pdf_link=birth.get('pdf_link'),
                programme=birth.get('programme'),
                date=birth.findtext('DATE'),
                place=birth.findtext('PLACE'),
                country=birth.findtext('COUNTRY'),
            )
        for passport in entity.findall('PASSPORT'):
            p = Passport.objects.create(
                id=passport.get('Id'),
                entity=e,
                legal_basis=passport.get('legal_basis'),
                reg_date=passport.get('reg_date') or None,
                pdf_link=passport.get('pdf_link'),
                programme=passport.get('programme'),
                number=passport.findtext('NUMBER'),
                country=passport.findtext('COUNTRY'),
            )
        for citizen in entity.findall('CITIZEN'):
            c = Citizen.objects.create(
                id=citizen.get('Id'),
                entity=e,
                legal_basis=citizen.get('legal_basis'),
                reg_date=citizen.get('reg_date') or None,
                pdf_link=citizen.get('pdf_link'),
                programme=citizen.get('programme'),
                country=citizen.findtext('COUNTRY'),
            )
        yield "Entity %s created ..." % e.id
       
    yield '<a href="/">Return to search</a>'


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
    data = data.lower()
    cursor = connection.cursor()
    cursor.execute("SELECT entity_id FROM sanctions_name WHERE "
                   "wholename LIKE %s"
                   " OR lastname||', '||firstname like %s"
                   " OR firstname||' '||lastname like %s"
                   " OR firstname||' '||middlename||' '||lastname like %s",
                   params=['%%%s%%' % data] * 4
    )
    name_ids = [r[0] for r in cursor.fetchall()]
    entities = Entity.objects.filter(id__in=name_ids)
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
    try:
        context['version'] = Download.objects.latest('download_time')
        context['number_of_entries'] = Name.objects.count()
    except Download.DoesNotExist:
        pass
    return render_to_response('sanctions/search.html', context)
