# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.section'
        db.add_column(u'news_article', 'section',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Article.section'
        db.delete_column(u'news_article', 'section')


    models = {
        u'news.article': {
            'Meta': {'ordering': "('-is_featured', '-created')", 'object_name': 'Article'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'section': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['news']