# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Challenge'
        db.create_table(u'challenges_challenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('start_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('is_external', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('event_dates', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('acknowledgments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizations.Organization'], null=True, blank=True)),
            ('hide_entries', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'challenges', ['Challenge'])

        # Adding model 'Question'
        db.create_table(u'challenges_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Challenge'])),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'challenges', ['Question'])

        # Adding model 'Entry'
        db.create_table(u'challenges_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Challenge'])),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.Application'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'challenges', ['Entry'])

        # Adding unique constraint on 'Entry', fields ['challenge', 'application']
        db.create_unique(u'challenges_entry', ['challenge_id', 'application_id'])

        # Adding model 'EntryAnswer'
        db.create_table(u'challenges_entryanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Entry'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenges.Question'])),
            ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'challenges', ['EntryAnswer'])

        # Adding unique constraint on 'EntryAnswer', fields ['entry', 'question']
        db.create_unique(u'challenges_entryanswer', ['entry_id', 'question_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'EntryAnswer', fields ['entry', 'question']
        db.delete_unique(u'challenges_entryanswer', ['entry_id', 'question_id'])

        # Removing unique constraint on 'Entry', fields ['challenge', 'application']
        db.delete_unique(u'challenges_entry', ['challenge_id', 'application_id'])

        # Deleting model 'Challenge'
        db.delete_table(u'challenges_challenge')

        # Deleting model 'Question'
        db.delete_table(u'challenges_question')

        # Deleting model 'Entry'
        db.delete_table(u'challenges_entry')

        # Deleting model 'EntryAnswer'
        db.delete_table(u'challenges_entryanswer')


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
        u'apps.applicationmembership': {
            'Meta': {'unique_together': "(('user', 'application'),)", 'object_name': 'ApplicationMembership'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.Application']"}),
            'can_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
        u'challenges.challenge': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Challenge'},
            'acknowledgments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'event_dates': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hide_entries': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organizations.Organization']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'challenges.entry': {
            'Meta': {'unique_together': "(('challenge', 'application'),)", 'object_name': 'Entry'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.Application']"}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        u'challenges.entryanswer': {
            'Meta': {'ordering': "('question__order',)", 'unique_together': "(('entry', 'question'),)", 'object_name': 'EntryAnswer'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Entry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Question']"})
        },
        u'challenges.question': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Question'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenges.Challenge']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'organizations.organization': {
            'Meta': {'object_name': 'Organization'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'interest_ignite': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['profiles.Interest']", 'symmetrical': 'False', 'blank': 'True'}),
            'interests_other': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False', 'through': u"orm['organizations.OrganizationMember']", 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'position': ('geoposition.fields.GeopositionField', [], {'default': "'0,0'", 'max_length': '42', 'blank': 'True'}),
            'resources_available': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'organizations.organizationmember': {
            'Meta': {'unique_together': "(('user', 'organization'),)", 'object_name': 'OrganizationMember'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organizations.Organization']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'profiles.interest': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Interest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
        }
    }

    complete_apps = ['challenges']