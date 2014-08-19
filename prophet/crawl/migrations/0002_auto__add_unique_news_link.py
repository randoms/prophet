# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'News', fields ['link']
        db.create_unique(u'crawl_news', ['link'])


    def backwards(self, orm):
        # Removing unique constraint on 'News', fields ['link']
        db.delete_unique(u'crawl_news', ['link'])


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
            'link': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
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