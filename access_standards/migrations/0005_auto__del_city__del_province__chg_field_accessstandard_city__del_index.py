# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'City'
        db.delete_table('city')

        # Deleting model 'Province'
        db.delete_table('province')


        # Changing field 'AccessStandard.city'
        db.alter_column('access_standard', 'city', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40))
        # Removing index on 'AccessStandard', fields ['city']
        db.delete_index('access_standard', ['city'])

        # Adding unique constraint on 'AccessStandard', fields ['city']
        db.create_unique('access_standard', ['city'])


    def backwards(self, orm):
        # Removing unique constraint on 'AccessStandard', fields ['city']
        db.delete_unique('access_standard', ['city'])

        # Adding index on 'AccessStandard', fields ['city']
        db.create_index('access_standard', ['city'])

        # Adding model 'City'
        db.create_table('city', (
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['access_standards.Province'])),
            ('pinyin', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
        ))
        db.send_create_signal('access_standards', ['City'])

        # Adding model 'Province'
        db.create_table('province', (
            ('pinyin', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('access_standards', ['Province'])


        # Changing field 'AccessStandard.city'
        db.alter_column('access_standard', 'city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['access_standards.City'], to_field='name', db_column='city'))

    models = {
        'access_standards.accessstandard': {
            'DVM': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'Meta': {'object_name': 'AccessStandard', 'db_table': "'access_standard'"},
            'city': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'emission_standard': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standard_details': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['access_standards']