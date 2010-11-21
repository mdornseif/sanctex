#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Maximillian Dornseif on 2010-11-21.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import config
config.imported = True

from google.appengine.ext import db
import pickle


class Entity(db.Model):
    id = db.StringProperty()
    type = db.StringProperty(required=False)
    legal_basis = db.StringProperty(required=False)
    reg_date = db.StringProperty(required=False)
    pdf_link = db.LinkProperty(required=False)
    programme = db.StringProperty(required=False)
    lastname = db.TextProperty(required=False)
    addon_data = db.BlobProperty(required=False)
    remark = db.TextProperty(required=False)

    def get_url(self):
        return "/entity/%s/%s/" % (self.id, self.name_set.get().searchterms[0].replace(' ', '_'))

    def unpickle(self):
        d = pickle.loads(self.addon_data)
        self.addresses = d.get('addresses', {})
        self.births = d.get('births', {})
        self.passports = d.get('passports', {})
        self.citizenship = d.get('citizenship', {})
        self.names = self.name_set.fetch(25)


class Name(db.Expando):
    sanc_entity = db.ReferenceProperty(Entity)
    firstname = db.StringProperty(required=False)
    middlename = db.StringProperty(required=False)
    lastname = db.StringProperty(required=False)
    wholename = db.StringProperty()
    function = db.StringProperty(required=False)
    language = db.StringProperty(required=False)
    title = db.StringProperty(required=False)
    gender = db.StringProperty(required=False)
    legal_basis = db.StringProperty(required=False)
    reg_date = db.StringProperty(required=False)
    pdf_link = db.StringProperty(required=False)
    programme = db.StringProperty(required=False)
    searchterms = db.StringListProperty()
    metaphones = db.StringListProperty()

    def __unicode__(self):
        return self.wholename or u'%s %s' % (self.firstname, self.lastname)
