# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'maps_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'maps', ['Category'])

        # Adding model 'Location'
        db.create_table(u'maps_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('position', self.gf('geoposition.fields.GeopositionField')(default='0,0', max_length=42)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.Category'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'maps', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'maps_category')

        # Deleting model 'Location'
        db.delete_table(u'maps_location')


    models = {
        u'maps.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'maps.location': {
            'Meta': {'object_name': 'Location'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'position': ('geoposition.fields.GeopositionField', [], {'default': "'0,0'", 'max_length': '42'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        }
    }

    complete_apps = ['maps']