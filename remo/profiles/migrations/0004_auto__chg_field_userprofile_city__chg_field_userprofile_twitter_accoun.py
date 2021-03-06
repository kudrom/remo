# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'UserProfile.city'
        db.alter_column('profiles_userprofile', 'city', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'UserProfile.twitter_account'
        db.alter_column('profiles_userprofile', 'twitter_account', self.gf('django.db.models.fields.CharField')(max_length=16))

        # Changing field 'UserProfile.display_name'
        db.alter_column('profiles_userprofile', 'display_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15))

        # Changing field 'UserProfile.irc_name'
        db.alter_column('profiles_userprofile', 'irc_name', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'UserProfile.gpg_key'
        db.alter_column('profiles_userprofile', 'gpg_key', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Changing field 'UserProfile.country'
        db.alter_column('profiles_userprofile', 'country', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'UserProfile.region'
        db.alter_column('profiles_userprofile', 'region', self.gf('django.db.models.fields.CharField')(max_length=30))


    def backwards(self, orm):
        
        # Changing field 'UserProfile.city'
        db.alter_column('profiles_userprofile', 'city', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'UserProfile.twitter_account'
        db.alter_column('profiles_userprofile', 'twitter_account', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'UserProfile.display_name'
        db.alter_column('profiles_userprofile', 'display_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15, null=True))

        # Changing field 'UserProfile.irc_name'
        db.alter_column('profiles_userprofile', 'irc_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'UserProfile.gpg_key'
        db.alter_column('profiles_userprofile', 'gpg_key', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

        # Changing field 'UserProfile.country'
        db.alter_column('profiles_userprofile', 'country', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'UserProfile.region'
        db.alter_column('profiles_userprofile', 'region', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.ircchannel': {
            'Meta': {'object_name': 'IRCChannel'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'profiles.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'users_added'", 'null': 'True', 'to': "orm['auth.User']"}),
            'bio': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'diaspora_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '15', 'blank': 'True'}),
            'facebook_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'gpg_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irc_channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['profiles.IRCChannel']", 'symmetrical': 'False'}),
            'irc_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'linkedin_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mozillians_profile_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'personal_blog_feed': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'personal_website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'private_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'private_email_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'twitter_account': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['profiles']
