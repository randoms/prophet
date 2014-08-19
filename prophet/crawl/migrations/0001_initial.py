# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table(u'crawl_news', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('time', self.gf('django.db.models.fields.IntegerField')()),
            ('link', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'crawl', ['News'])

        # Adding model 'Keywords'
        db.create_table(u'crawl_keywords', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news', self.gf('django.db.models.fields.related.ForeignKey')(related_name='keywords', to=orm['crawl.News'])),
            ('words', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'crawl', ['Keywords'])

        # Adding model 'Refers'
        db.create_table(u'crawl_refers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news', self.gf('django.db.models.fields.related.ForeignKey')(related_name='refer_news', to=orm['crawl.News'])),
            ('refer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'crawl', ['Refers'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table(u'crawl_news')

        # Deleting model 'Keywords'
        db.delete_table(u'crawl_keywords')

        # Deleting model 'Refers'
        db.delete_table(u'crawl_refers')


    models = {
        u'crawl.keywords': {
            'Meta': {'object_name': 'Keywords'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'keywords'", 'to': u"orm['crawl.News']"}),
            'words': ('django.db.models.fields.TextField', [], {})
        },
        u'crawl.news': {
            'Meta': {'object_name': 'News'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'time': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'crawl.refers': {
            'Meta': {'object_name': 'Refers'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'refer_news'", 'to': u"orm['crawl.News']"}),
            'refer': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['crawl']