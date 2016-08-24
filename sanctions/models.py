#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Maximillian Dornseif on 2010-11-21.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import config
config.imported = True

import pickle

from google.appengine.ext import ndb


class seEntity(ndb.Model):
    typ = ndb.StringProperty(required=False, indexed=True)
    legal_basis = ndb.StringProperty(required=False, indexed=True)
    reg_date = ndb.StringProperty(required=False, indexed=False)
    pdf_link = ndb.StringProperty(required=False, indexed=False)
    programme = ndb.StringProperty(required=False, indexed=True)
    lastname = ndb.TextProperty(required=False, indexed=True)
    addon_data = ndb.JsonProperty(required=False, indexed=False, compressed=True)
    remark = ndb.TextProperty(required=False, indexed=False)
    updated_at = ndb.DateTimeProperty(auto_now=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    def get_url(self):
        return "/entity/%s/%s/" % (self.key.id(), self.names[0].searchterms[0].replace(' ', '_'))

    @property
    def addresses(self):
        return self.addon_data.get('addresses', {})
    
    @property
    def births(self):
        return self.addon_data.get('births', {})
    
    @property
    def passports(self):
        return self.addon_data.get('passports', {})
    
    @property
    def citizenship(self):
        return self.addon_data.get('citizenship', {})
    
    @property
    def names(self):
        return seName.query().filter(seName.sanc_entity==self.key).fetch(25)
    

class seName(ndb.Expando):
    sanc_entity = ndb.KeyProperty(kind=seEntity)
    firstname = ndb.StringProperty(required=False)
    middlename = ndb.StringProperty(required=False)
    lastname = ndb.StringProperty(required=False)
    wholename = ndb.StringProperty()
    function = ndb.StringProperty(required=False)
    language = ndb.StringProperty(required=False)
    title = ndb.StringProperty(required=False)
    gender = ndb.StringProperty(required=False)
    legal_basis = ndb.StringProperty(required=False)
    reg_date = ndb.StringProperty(required=False)
    pdf_link = ndb.StringProperty(required=False)
    programme = ndb.StringProperty(required=False)
    searchterms = ndb.StringProperty(repeated=True)
    metaphones = ndb.StringProperty(repeated=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    def __unicode__(self):
        return self.wholename or u'%s %s' % (self.firstname, self.lastname)
