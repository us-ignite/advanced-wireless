# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Pitch.email_text'
        db.delete_column(u'smart_gigabit_communities_pitch', 'email_text')

        # Adding field 'Pitch.link'
        db.add_column(u'smart_gigabit_communities_pitch', 'link',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Pitch.link_text'
        db.add_column(u'smart_gigabit_communities_pitch', 'link_text',
                      self.gf('django.db.models.fields.CharField')(default='LEARN MORE', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Pitch.email_text'
        db.add_column(u'smart_gigabit_communities_pitch', 'email_text',
                      self.gf('django.db.models.fields.CharField')(default='Email Them', max_length=50),
                      keep_default=False)

        # Deleting field 'Pitch.link'
        db.delete_column(u'smart_gigabit_communities_pitch', 'link')

        # Deleting field 'Pitch.link_text'
        db.delete_column(u'smart_gigabit_communities_pitch', 'link_text')


    models = {
        u'smart_gigabit_communities.pitch': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Pitch'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'google': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_text': ('django.db.models.fields.CharField', [], {'default': "'LEARN MORE'", 'max_length': '50'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pitch_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'pitch_video': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'youtube': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['smart_gigabit_communities']