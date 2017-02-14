# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Pitch.email_text'
        db.add_column(u'smart_gigabit_communities_pitch', 'email_text',
                      self.gf('django.db.models.fields.CharField')(default='EMAIL THEM', max_length=50),
                      keep_default=False)


        # Changing field 'Pitch.google'
        db.alter_column(u'smart_gigabit_communities_pitch', 'google', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))
        # Removing index on 'Pitch', fields ['google']
        db.delete_index(u'smart_gigabit_communities_pitch', ['google'])


        # Changing field 'Pitch.twitter'
        db.alter_column(u'smart_gigabit_communities_pitch', 'twitter', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))
        # Removing index on 'Pitch', fields ['twitter']
        db.delete_index(u'smart_gigabit_communities_pitch', ['twitter'])


        # Changing field 'Pitch.youtube'
        db.alter_column(u'smart_gigabit_communities_pitch', 'youtube', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))
        # Removing index on 'Pitch', fields ['youtube']
        db.delete_index(u'smart_gigabit_communities_pitch', ['youtube'])


        # Changing field 'Pitch.facebook'
        db.alter_column(u'smart_gigabit_communities_pitch', 'facebook', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))
        # Removing index on 'Pitch', fields ['facebook']
        db.delete_index(u'smart_gigabit_communities_pitch', ['facebook'])


    def backwards(self, orm):
        # Adding index on 'Pitch', fields ['facebook']
        db.create_index(u'smart_gigabit_communities_pitch', ['facebook'])

        # Adding index on 'Pitch', fields ['youtube']
        db.create_index(u'smart_gigabit_communities_pitch', ['youtube'])

        # Adding index on 'Pitch', fields ['twitter']
        db.create_index(u'smart_gigabit_communities_pitch', ['twitter'])

        # Adding index on 'Pitch', fields ['google']
        db.create_index(u'smart_gigabit_communities_pitch', ['google'])

        # Deleting field 'Pitch.email_text'
        db.delete_column(u'smart_gigabit_communities_pitch', 'email_text')


        # Changing field 'Pitch.google'
        db.alter_column(u'smart_gigabit_communities_pitch', 'google', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True))

        # Changing field 'Pitch.twitter'
        db.alter_column(u'smart_gigabit_communities_pitch', 'twitter', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True))

        # Changing field 'Pitch.youtube'
        db.alter_column(u'smart_gigabit_communities_pitch', 'youtube', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True))

        # Changing field 'Pitch.facebook'
        db.alter_column(u'smart_gigabit_communities_pitch', 'facebook', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True))

    models = {
        u'smart_gigabit_communities.pitch': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Pitch'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'email_text': ('django.db.models.fields.CharField', [], {'default': "'Email Them'", 'max_length': '50'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'google': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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