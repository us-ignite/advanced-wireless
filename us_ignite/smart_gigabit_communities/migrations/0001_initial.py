# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pitch'
        db.create_table(u'smart_gigabit_communities_pitch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('subtitle', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=500, null=True, blank=True)),
            ('pitch_video', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('pitch_image', self.gf('django.db.models.fields.files.ImageField')(max_length=500, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'smart_gigabit_communities', ['Pitch'])


    def backwards(self, orm):
        # Deleting model 'Pitch'
        db.delete_table(u'smart_gigabit_communities_pitch')


    models = {
        u'smart_gigabit_communities.pitch': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Pitch'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pitch_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'pitch_video': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['smart_gigabit_communities']