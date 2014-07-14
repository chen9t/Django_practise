# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'City'
        db.create_table('city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['access_standards.Province'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('pinyin', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('access_standards', ['City'])

        # Adding model 'AccessStandard'
        db.create_table('access_standard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['access_standards.City'], to_field='name', db_column='city')),
            ('emission_standard', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('standard_details', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('DVM', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
        ))
        db.send_create_signal('access_standards', ['AccessStandard'])

        # Adding model 'Province'
        db.create_table('province', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('pinyin', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('access_standards', ['Province'])


    def backwards(self, orm):
        # Deleting model 'City'
        db.delete_table('city')

        # Deleting model 'AccessStandard'
        db.delete_table('access_standard')

        # Deleting model 'Province'
        db.delete_table('province')


    models = {
        'access_standards.accessstandard': {
            'DVM': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'Meta': {'object_name': 'AccessStandard', 'db_table': "'access_standard'"},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['access_standards.City']", 'to_field': "'name'", 'db_column': "'city'"}),
            'emission_standard': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standard_details': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'access_standards.city': {
            'Meta': {'object_name': 'City', 'db_table': "'city'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'pinyin': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['access_standards.Province']"})
        },
        'access_standards.province': {
            'Meta': {'object_name': 'Province', 'db_table': "'province'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pinyin': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['access_standards']