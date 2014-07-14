# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AccessStandard'
        db.delete_table('access_standard')


    def backwards(self, orm):
        # Adding model 'AccessStandard'
        db.create_table('access_standard', (
            ('DVM', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
            ('emission_standard', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('standard_details', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('access_standards', ['AccessStandard'])


    models = {
        
    }

    complete_apps = ['access_standards']