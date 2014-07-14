# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'City.province_id'
        #db.delete_column('city', 'province_id_id')

        # Adding field 'City.province'
        db.add_column('city', 'province',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['access_standards.Province']),
                      keep_default=False)

        # Deleting field 'AccessStandard.city_id'
        db.delete_column('access_standard', 'city_id_id')

        # Adding field 'AccessStandard.city'
        db.add_column('access_standard', 'city',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['access_standards.City']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'City.province_id'
        db.add_column('city', 'province_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['access_standards.Province']),
                      keep_default=False)

        # Deleting field 'City.province'
        db.delete_column('city', 'province_id')

        # Adding field 'AccessStandard.city_id'
        db.add_column('access_standard', 'city_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['access_standards.City']),
                      keep_default=False)

        # Deleting field 'AccessStandard.city'
        db.delete_column('access_standard', 'city_id')


    models = {
        'access_standards.accessstandard': {
            'DVM': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Meta': {'object_name': 'AccessStandard', 'db_table': "'access_standard'"},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['access_standards.City']"}),
            'emission_standard': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standard_details': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'access_standards.city': {
            'Meta': {'object_name': 'City', 'db_table': "'city'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'pinyin': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['access_standards.Province']"})
        },
        'access_standards.province': {
            'Meta': {'object_name': 'Province', 'db_table': "'province'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pinyin': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['access_standards']
