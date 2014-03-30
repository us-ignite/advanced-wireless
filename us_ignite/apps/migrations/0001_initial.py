# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feature'
        db.create_table(u'apps_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
        ))
        db.send_create_signal(u'apps', ['Feature'])

        # Adding model 'Domain'
        db.create_table(u'apps_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
        ))
        db.send_create_signal(u'apps', ['Domain'])

        # Adding model 'Application'
        db.create_table(u'apps_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('stage', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=500, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('impact_statement', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('assistance', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('team_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('team_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('acknowledgments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('slug', self.gf('us_ignite.common.fields.AutoUUIDField')(unique=True, max_length=50, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ownership_set', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('features_other', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.Domain'], null=True, blank=True)),
            ('awards', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'apps', ['Application'])

        # Adding M2M table for field features on 'Application'
        m2m_table_name = db.shorten_name(u'apps_application_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('application', models.ForeignKey(orm[u'apps.application'], null=False)),
            ('feature', models.ForeignKey(orm[u'apps.feature'], null=False))
        ))
        db.create_unique(m2m_table_name, ['application_id', 'feature_id'])

        # Adding model 'ApplicationMembership'
        db.create_table(u'apps_applicationmembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.Application'])),
            ('can_edit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'apps', ['ApplicationMembership'])

        # Adding unique constraint on 'ApplicationMembership', fields ['user', 'application']
        db.create_unique(u'apps_applicationmembership', ['user_id', 'application_id'])

        # Adding model 'ApplicationURL'
        db.create_table(u'apps_applicationurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.Application'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500)),
        ))
        db.send_create_signal(u'apps', ['ApplicationURL'])

        # Adding model 'ApplicationMedia'
        db.create_table(u'apps_applicationmedia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.Application'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=500, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'apps', ['ApplicationMedia'])

        # Adding model 'ApplicationVersion'
        db.create_table(u'apps_applicationversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('stage', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=500, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('impact_statement', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('assistance', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('team_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('team_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('acknowledgments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.Application'])),
            ('slug', self.gf('us_ignite.common.fields.AutoUUIDField')(unique=True, max_length=50, blank=True)),
        ))
        db.send_create_signal(u'apps', ['ApplicationVersion'])

        # Adding model 'Page'
        db.create_table(u'apps_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='name', overwrite=False)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'apps', ['Page'])

        # Adding model 'PageApplication'
        db.create_table(u'apps_pageapplication', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.Page'])),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.Application'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'apps', ['PageApplication'])


    def backwards(self, orm):
        # Removing unique constraint on 'ApplicationMembership', fields ['user', 'application']
        db.delete_unique(u'apps_applicationmembership', ['user_id', 'application_id'])

        # Deleting model 'Feature'
        db.delete_table(u'apps_feature')

        # Deleting model 'Domain'
        db.delete_table(u'apps_domain')

        # Deleting model 'Application'
        db.delete_table(u'apps_application')

        # Removing M2M table for field features on 'Application'
        db.delete_table(db.shorten_name(u'apps_application_features'))

        # Deleting model 'ApplicationMembership'
        db.delete_table(u'apps_applicationmembership')

        # Deleting model 'ApplicationURL'
        db.delete_table(u'apps_applicationurl')

        # Deleting model 'ApplicationMedia'
        db.delete_table(u'apps_applicationmedia')

        # Deleting model 'ApplicationVersion'
        db.delete_table(u'apps_applicationversion')

        # Deleting model 'Page'
        db.delete_table(u'apps_page')

        # Deleting model 'PageApplication'
        db.delete_table(u'apps_pageapplication')


    models = {
        u'apps.application': {
            'Meta': {'ordering': "('-is_featured', 'created')", 'object_name': 'Application'},
            'acknowledgments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'assistance': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'awards': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.Domain']", 'null': 'True', 'blank': 'True'}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['apps.Feature']", 'symmetrical': 'False', 'blank': 'True'}),
            'features_other': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'blank': 'True'}),
            'impact_statement': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'membership_set'", 'symmetrical': 'False', 'through': u"orm['apps.ApplicationMembership']", 'to': u"orm['auth.User']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ownership_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'slug': ('us_ignite.common.fields.AutoUUIDField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'stage': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'team_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'apps.applicationmedia': {
            'Meta': {'ordering': "('created',)", 'object_name': 'ApplicationMedia'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.Application']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'apps.applicationmembership': {
            'Meta': {'unique_together': "(('user', 'application'),)", 'object_name': 'ApplicationMembership'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.Application']"}),
            'can_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'apps.applicationurl': {
            'Meta': {'object_name': 'ApplicationURL'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        u'apps.applicationversion': {
            'Meta': {'object_name': 'ApplicationVersion'},
            'acknowledgments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.Application']"}),
            'assistance': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'blank': 'True'}),
            'impact_statement': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('us_ignite.common.fields.AutoUUIDField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'stage': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'team_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'apps.domain': {
            'Meta': {'object_name': 'Domain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
        },
        u'apps.feature': {
            'Meta': {'object_name': 'Feature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
        },
        u'apps.page': {
            'Meta': {'object_name': 'Page'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        u'apps.pageapplication': {
            'Meta': {'ordering': "('order',)", 'object_name': 'PageApplication'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.Page']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['apps']