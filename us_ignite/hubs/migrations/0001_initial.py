# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("apps", "0001_initial"),
        ("organizations", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'HubRequest'
        db.create_table(u'hubs_hubrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('hub', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hubs.Hub'], null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'hubs', ['HubRequest'])

        # Adding model 'NetworkSpeed'
        db.create_table(u'hubs_networkspeed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
        ))
        db.send_create_signal(u'hubs', ['NetworkSpeed'])

        # Adding model 'Hub'
        db.create_table(u'hubs_hub', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('connections', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizations.Organization'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('network_speed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hubs.NetworkSpeed'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('is_advanced', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('experimentation', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('estimated_passes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=500, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('position', self.gf('geoposition.fields.GeopositionField')(default='0,0', max_length=42, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'hubs', ['Hub'])

        # Adding M2M table for field applications on 'Hub'
        m2m_table_name = db.shorten_name(u'hubs_hub_applications')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hub', models.ForeignKey(orm[u'hubs.hub'], null=False)),
            ('application', models.ForeignKey(orm[u'apps.application'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hub_id', 'application_id'])

        # Adding M2M table for field features on 'Hub'
        m2m_table_name = db.shorten_name(u'hubs_hub_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hub', models.ForeignKey(orm[u'hubs.hub'], null=False)),
            ('feature', models.ForeignKey(orm[u'apps.feature'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hub_id', 'feature_id'])

        # Adding model 'HubActivity'
        db.create_table(u'hubs_hubactivity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hub', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hubs.Hub'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'hubs', ['HubActivity'])

        # Adding model 'HubMembership'
        db.create_table(u'hubs_hubmembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hub', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hubs.Hub'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'hubs', ['HubMembership'])

        # Adding model 'HubAppMembership'
        db.create_table(u'hubs_hubappmembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hub', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hubs.Hub'])),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.Application'])),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'hubs', ['HubAppMembership'])


    def backwards(self, orm):
        # Deleting model 'HubRequest'
        db.delete_table(u'hubs_hubrequest')

        # Deleting model 'NetworkSpeed'
        db.delete_table(u'hubs_networkspeed')

        # Deleting model 'Hub'
        db.delete_table(u'hubs_hub')

        # Removing M2M table for field applications on 'Hub'
        db.delete_table(db.shorten_name(u'hubs_hub_applications'))

        # Removing M2M table for field features on 'Hub'
        db.delete_table(db.shorten_name(u'hubs_hub_features'))

        # Deleting model 'HubActivity'
        db.delete_table(u'hubs_hubactivity')

        # Deleting model 'HubMembership'
        db.delete_table(u'hubs_hubmembership')

        # Deleting model 'HubAppMembership'
        db.delete_table(u'hubs_hubappmembership')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hubs.hub': {
            'Meta': {'ordering': "('-is_featured', 'created')", 'object_name': 'Hub'},
            'applications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['apps.Application']", 'symmetrical': 'False', 'blank': 'True'}),
            'connections': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'estimated_passes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'experimentation': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['apps.Feature']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'blank': 'True'}),
            'is_advanced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network_speed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hubs.NetworkSpeed']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organizations.Organization']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'position': ('geoposition.fields.GeopositionField', [], {'default': "'0,0'", 'max_length': '42', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'hubs.hubactivity': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'HubActivity'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hubs.Hub']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'hubs.hubappmembership': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'HubAppMembership'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['apps.Application']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hubs.Hub']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'hubs.hubmembership': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'HubMembership'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hubs.Hub']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'hubs.hubrequest': {
            'Meta': {'ordering': "('created',)", 'object_name': 'HubRequest'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hubs.Hub']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'hubs.networkspeed': {
            'Meta': {'object_name': 'NetworkSpeed'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
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

    complete_apps = ['hubs']
