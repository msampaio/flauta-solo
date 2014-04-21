# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Composition.composition_type'
        db.alter_column(u'analysis_composition', 'composition_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.CompositionType'], null=True))

    def backwards(self, orm):

        # Changing field 'Composition.composition_type'
        db.alter_column(u'analysis_composition', 'composition_type_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['analysis.CompositionType']))

    models = {
        u'analysis.collection': {
            'Meta': {'object_name': 'Collection'},
            'compositions': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Composition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imslp_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'analysis.composer': {
            'Meta': {'object_name': 'Composer'},
            'date_birth': ('django.db.models.fields.DateField', [], {}),
            'date_death': ('django.db.models.fields.DateField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'place_birth': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'place_death': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time_period': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'analysis.composition': {
            'Meta': {'object_name': 'Composition'},
            'composer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.Composer']"}),
            'composition_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.CompositionType']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'misc_notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'music_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.MusicData']"}),
            'pagecount': ('django.db.models.fields.IntegerField', [], {}),
            'publisher_information': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'raw_pagecount': ('django.db.models.fields.IntegerField', [], {}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'uploader': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'analysis.compositiontype': {
            'Meta': {'object_name': 'CompositionType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'analysis.musicdata': {
            'Meta': {'object_name': 'MusicData'},
            'ambitus': ('django.db.models.fields.IntegerField', [], {}),
            'contour': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'durations': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'float'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervals': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'varchar'", 'null': 'True', 'blank': 'True'}),
            'intervals_midi': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'intervals_with_direction': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'varchar'", 'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'key_midi': ('django.db.models.fields.IntegerField', [], {}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'notes_midi': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'preview': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'score': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.MusicXMLScore']"}),
            'time_signature': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'total_duration': ('django.db.models.fields.FloatField', [], {})
        },
        u'analysis.musicxmlscore': {
            'Meta': {'object_name': 'MusicXMLScore'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['analysis']