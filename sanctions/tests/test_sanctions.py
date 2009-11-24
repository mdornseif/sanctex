#!/usr/bin/env python
# encoding: utf-8

# created november 2009 by danielroseman for Hudora GmbH

from django import test

from sanctions.models import Download, Entity, Name, Address, Birth, Passport, Citizen
from sanctions import views
from sanctions.tests import test_data

class DownloadTests(test.TestCase):
    def setUp(self):
        self.import_data()
    
    def import_data(self):
        # replace default get_data function with mocked version
        def get_data():
            return test_data.xml
        old_get_data = views.get_data
        views.get_data = get_data
        
        for _ in views.import_sanctions():
            pass
            
        # put it back how we found it
        views.get_data = old_get_data


    def test_download(self):
        """Parse sample XML and ensure that all data has been imported."""
        
        self.assertEquals(Entity.objects.count(), 13)
        self.assertEquals(Name.objects.count(), 21)
        self.assertEquals(Address.objects.count(), 1)
        self.assertEquals(Birth.objects.count(), 14)
        self.assertEquals(Passport.objects.count(), 2)
        self.assertEquals(Citizen.objects.count(), 1)
        
    def test_simple_match(self):
        matches = views.match('mugabe')
        self.assertEquals(len(matches), 1)
        
    def test_match_surname_firstname(self):
        matches = views.match('Buka, Flora')
        self.assertEquals(len(matches), 1)


    def test_match_wholename(self):
        matches = views.match('Testy Testname')
        self.assertEquals(len(matches), 1)


    def test_search_view(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'Results')

    def test_search_single_name(self):
        response = self.client.post('/', {'name': 'mugabe'})
        self.assertContains(response, 'Results: 1 name checked, 1 match found')

    def test_search_multiple_names(self):
        response = self.client.post('/', {'multiple_names': 'mugabe\r\nflora'})
        self.assertContains(response, 'Results: 2 names checked, 2 matches found')

    def test_file_search(self):
        f = open('sanctions/tests/names.txt')
        # need an empty non-file field here so client recognises the POST
        response = self.client.post('/', {'name': '', 'uploaded': f})
        self.assertContains(response, 'Results: 3 names checked, 2 matches found')
