# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feature'
        db.create_table(u'actionclusters_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
        ))
        db.send_create_signal(u'actionclusters', ['Feature'])

        # Adding model 'Domain'
        db.create_table(u'actionclusters_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
        ))
        db.send_create_signal(u'actionclusters', ['Domain'])

        # Adding model 'ActionCluster'
        db.create_table(u'actionclusters_actioncluster', (
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
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ownership_set_for_actioncluster', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('features_other', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actionclusters.Domain'], null=True, blank=True)),
            ('awards', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('position', self.gf('geoposition.fields.GeopositionField')(default='0,0', max_length=42, blank=True)),
            ('is_homepage', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'actionclusters', ['ActionCluster'])

        # Adding M2M table for field features on 'ActionCluster'
        m2m_table_name = db.shorten_name(u'actionclusters_actioncluster_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('actioncluster', models.ForeignKey(orm[u'actionclusters.actioncluster'], null=False)),
            ('feature', models.ForeignKey(orm[u'actionclusters.feature'], null=False))
        ))
        db.create_unique(m2m_table_name, ['actioncluster_id', 'feature_id'])

        # Adding model 'ActionClusterMembership'
        db.create_table(u'actionclusters_actionclustermembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('actioncluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actionclusters.ActionCluster'])),
            ('can_edit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'actionclusters', ['ActionClusterMembership'])

        # Adding unique constraint on 'ActionClusterMembership', fields ['user', 'actioncluster']
        db.create_unique(u'actionclusters_actionclustermembership', ['user_id', 'actioncluster_id'])

        # Adding model 'ActionClusterURL'
        db.create_table(u'actionclusters_actionclusterurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('actioncluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actionclusters.ActionCluster'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500)),
        ))
        db.send_create_signal(u'actionclusters', ['ActionClusterURL'])

        # Adding model 'ActionClusterMedia'
        db.create_table(u'actionclusters_actionclustermedia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('actioncluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actionclusters.ActionCluster'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=500, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'actionclusters', ['ActionClusterMedia'])

        # Adding model 'ActionClusterVersion'
        db.create_table(u'actionclusters_actionclusterversion', (
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
            ('actioncluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actionclusters.ActionCluster'])),
            ('slug', self.gf('us_ignite.common.fields.AutoUUIDField')(unique=True, max_length=50, blank=True)),
        ))
        db.send_create_signal(u'actionclusters', ['ActionClusterVersion'])

        # Adding model 'Page'
        db.create_table(u'actionclusters_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='name', overwrite=False)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'actionclusters', ['Page'])

        # Adding model 'PageActionCluster'
        db.create_table(u'actionclusters_pageactioncluster', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actionclusters.Page'])),
            ('actioncluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actionclusters.ActionCluster'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'actionclusters', ['PageActionCluster'])


    def backwards(self, orm):
        # Removing unique constraint on 'ActionClusterMembership', fields ['user', 'actioncluster']
        db.delete_unique(u'actionclusters_actionclustermembership', ['user_id', 'actioncluster_id'])

        # Deleting model 'Feature'
        db.delete_table(u'actionclusters_feature')

        # Deleting model 'Domain'
        db.delete_table(u'actionclusters_domain')

        # Deleting model 'ActionCluster'
        db.delete_table(u'actionclusters_actioncluster')

        # Removing M2M table for field features on 'ActionCluster'
        db.delete_table(db.shorten_name(u'actionclusters_actioncluster_features'))

        # Deleting model 'ActionClusterMembership'
        db.delete_table(u'actionclusters_actionclustermembership')

        # Deleting model 'ActionClusterURL'
        db.delete_table(u'actionclusters_actionclusterurl')

        # Deleting model 'ActionClusterMedia'
        db.delete_table(u'actionclusters_actionclustermedia')

        # Deleting model 'ActionClusterVersion'
        db.delete_table(u'actionclusters_actionclusterversion')

        # Deleting model 'Page'
        db.delete_table(u'actionclusters_page')

        # Deleting model 'PageActionCluster'
        db.delete_table(u'actionclusters_pageactioncluster')


    models = {
        u'actionclusters.actioncluster': {
            'Meta': {'ordering': "('-is_featured', 'created')", 'object_name': 'ActionCluster'},
            'acknowledgments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'assistance': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'awards': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actionclusters.Domain']", 'null': 'True', 'blank': 'True'}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['actionclusters.Feature']", 'symmetrical': 'False', 'blank': 'True'}),
            'features_other': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'blank': 'True'}),
            'impact_statement': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_homepage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'membership_set_for_actioncluster'", 'symmetrical': 'False', 'through': u"orm['actionclusters.ActionClusterMembership']", 'to': u"orm['auth.User']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ownership_set_for_actioncluster'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'position': ('geoposition.fields.GeopositionField', [], {'default': "'0,0'", 'max_length': '42', 'blank': 'True'}),
            'slug': ('us_ignite.common.fields.AutoUUIDField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'stage': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'team_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'actionclusters.actionclustermedia': {
            'Meta': {'ordering': "('created',)", 'object_name': 'ActionClusterMedia'},
            'actioncluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actionclusters.ActionCluster']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'actionclusters.actionclustermembership': {
            'Meta': {'unique_together': "(('user', 'actioncluster'),)", 'object_name': 'ActionClusterMembership'},
            'actioncluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actionclusters.ActionCluster']"}),
            'can_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'actionclusters.actionclusterurl': {
            'Meta': {'object_name': 'ActionClusterURL'},
            'actioncluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actionclusters.ActionCluster']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        u'actionclusters.actionclusterversion': {
            'Meta': {'object_name': 'ActionClusterVersion'},
            'acknowledgments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'actioncluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actionclusters.ActionCluster']"}),
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
        u'actionclusters.domain': {
            'Meta': {'object_name': 'Domain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
        },
        u'actionclusters.feature': {
            'Meta': {'object_name': 'Feature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
        },
        u'actionclusters.page': {
            'Meta': {'object_name': 'Page'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        u'actionclusters.pageactioncluster': {
            'Meta': {'ordering': "('order',)", 'object_name': 'PageActionCluster'},
            'actioncluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actionclusters.ActionCluster']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['actionclusters.Page']"})
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

    complete_apps = ['actionclusters']