# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'City'
        db.delete_table('city')

        # Deleting model 'AccessStandard'
        db.delete_table('access_standard')

        # Deleting model 'Province'
        db.delete_table('province')


    def backwards(self, orm):
        # Adding model 'City'
        db.create_table('city', (
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['access_standards.Province'])),
            ('pinyin', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('access_standards', ['City'])

        # Adding model 'AccessStandard'
        db.create_table('access_standard', (
            ('DVM', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['access_standards.City'])),
            ('emission_standard', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('standard_details', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('access_standards', ['AccessStandard'])

        # Adding model 'Province'
        db.create_table('province', (
            ('pinyin', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('access_standards', ['Province'])


    models = {
        
    }

    complete_apps = ['access_standards']