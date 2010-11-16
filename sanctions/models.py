#!/usr/bin/env python
# encoding: utf-8

# created november 2009 by danielroseman for Hudora GmbH

from django.db import models
from django.utils.encoding import smart_unicode

from djangotoolbox.fields import ListField

import metaphone


class Download(models.Model):
    version_date = models.DateField()
    download_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-download_time']


class Entity(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=1)
    legal_basis = models.CharField(max_length=50, blank=True)
    reg_date = models.DateField(null=True, blank=True)
    pdf_link = models.URLField(blank=True, verify_exists=False)
    programme = models.CharField(max_length=10, blank=True)
    remark = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "entities"

    def __unicode__(self):
        return u"Entity %s" % self.id

    def get_absolute_url(self):
        return "/entity/%d/" % self.id


class Name(models.Model):
    id = models.IntegerField(primary_key=True)
    entity = models.ForeignKey(Entity)
    lastname = models.CharField(blank=True, max_length=100)
    firstname = models.CharField(blank=True, max_length=100)
    middlename = models.CharField(blank=True, max_length=100)
    wholename = models.CharField(blank=True, max_length=100)
    gender = models.CharField(blank=True, max_length=5)
    title = models.CharField(blank=True, max_length=50)
    function = models.TextField(blank=True)
    language = models.CharField(blank=True, max_length=10)
    legal_basis = models.CharField(max_length=50, blank=True)
    reg_date = models.DateField(null=True, blank=True)
    pdf_link = models.URLField(blank=True, verify_exists=False)
    programme = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return self.wholename or u'%s %s' % (self.firstname, self.lastname)


class NameIndex(models.Model):
    id = models.CharField(primary_key=True, max_length=300)
    entity = models.ForeignKey(Entity)
    name_variant = models.CharField(max_length=300)
    metaphones = ListField(models.CharField(max_length=100))

    def save(self, *args, **kwargs):
        self.id = self.entity.id + '_' + self.name_variant

        m1, m2 = metaphone.dm(smart_unicode(self.name_variant, strings_only=True))
        if m1:
            self.metaphones.append(m1)
        if m2:
            self.metaphones.append(m2)

        super(NameIndex, self).save(*args, **kwargs)


class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    entity = models.ForeignKey(Entity)
    number = models.CharField(blank=True, max_length=100)
    street = models.CharField(blank=True, max_length=100)
    zipcode = models.CharField(blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=100)
    country = models.CharField(blank=True, max_length=10)
    other = models.TextField(blank=True)
    legal_basis = models.CharField(max_length=50, blank=True)
    reg_date = models.DateField(null=True, blank=True)
    pdf_link = models.URLField(blank=True, verify_exists=False)
    programme = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name_plural = "addresses"

    def __unicode__(self):
        return u"Address for %s" % self.entity


class Birth(models.Model):
    id = models.IntegerField(primary_key=True)
    entity = models.ForeignKey(Entity)
    # date sometimes contains non-date text
    date = models.CharField(blank=True, max_length=100)
    place = models.CharField(blank=True, max_length=100)
    country = models.CharField(blank=True, max_length=10)
    legal_basis = models.CharField(max_length=50, blank=True)
    reg_date = models.DateField(null=True, blank=True)
    pdf_link = models.URLField(blank=True, verify_exists=False)
    programme = models.CharField(max_length=10, blank=True)


class Passport(models.Model):
    id = models.IntegerField(primary_key=True)
    entity = models.ForeignKey(Entity)
    # number is a whole chunk of text
    number = models.CharField(blank=True, max_length=500)
    country = models.CharField(blank=True, max_length=10)
    legal_basis = models.CharField(max_length=50, blank=True)
    reg_date = models.DateField(null=True, blank=True)
    pdf_link = models.URLField(blank=True, verify_exists=False)
    programme = models.CharField(max_length=10, blank=True)


class Citizen(models.Model):
    id = models.IntegerField(primary_key=True)
    entity = models.ForeignKey(Entity)
    country = models.CharField(blank=True, max_length=10)
    legal_basis = models.CharField(max_length=50, blank=True)
    reg_date = models.DateField(null=True, blank=True)
    pdf_link = models.URLField(blank=True, verify_exists=False)
    programme = models.CharField(max_length=10, blank=True)


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Name)
def create_name_index(sender, instance=None, created=None, **kwargs):
    if not created:
        return

    firstname = instance.firstname.lower()
    middlename = instance.middlename.lower()
    lastname = instance.lastname.lower()
    wholename = instance.wholename.lower()

    names = [firstname,
             middlename,
             lastname,
             wholename,
             ' '.join([firstname, lastname]),
             ' '.join([lastname, firstname]),
             ' '.join([firstname, middlename, lastname])]

    for name in names:
        name = name.strip()
        if not name: continue

        NameIndex.objects.create(entity=instance.entity, name_variant=name)