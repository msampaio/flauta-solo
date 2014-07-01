# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MusicXMLScore'
        db.create_table('analysis_musicxmlscore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('score', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('analysis', ['MusicXMLScore'])

        # Adding model 'MusicData'
        db.create_table('analysis_musicdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.MusicXMLScore'])),
            ('notes_midi', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True)),
            ('notes', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True)),
            ('intervals', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True, dbtype='varchar')),
            ('intervals_midi', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True)),
            ('intervals_with_direction', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True, dbtype='varchar')),
            ('durations', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True, dbtype='float')),
            ('contour', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True)),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('key_midi', self.gf('django.db.models.fields.IntegerField')()),
            ('time_signature', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('total_duration', self.gf('django.db.models.fields.FloatField')()),
            ('ambitus', self.gf('django.db.models.fields.IntegerField')()),
            ('preview', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal('analysis', ['MusicData'])

        # Adding model 'Composer'
        db.create_table('analysis_composer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imslp_id', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_death', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('place_birth', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('place_death', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('nationality', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('time_period', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('analysis', ['Composer'])

        # Adding model 'CompositionType'
        db.create_table('analysis_compositiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('analysis', ['CompositionType'])

        # Adding model 'Collection'
        db.create_table('analysis_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imslp_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('analysis', ['Collection'])

        # Adding model 'Composition'
        db.create_table('analysis_composition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('music_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.MusicData'])),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.Collection'])),
            ('composer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.Composer'])),
            ('composition_type', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['analysis.CompositionType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('editor', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('publisher_information', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('misc_notes', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('uploader', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pagecount', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('raw_pagecount', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('rating', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('imslp_filename', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('analysis', ['Composition'])


    def backwards(self, orm):
        # Deleting model 'MusicXMLScore'
        db.delete_table('analysis_musicxmlscore')

        # Deleting model 'MusicData'
        db.delete_table('analysis_musicdata')

        # Deleting model 'Composer'
        db.delete_table('analysis_composer')

        # Deleting model 'CompositionType'
        db.delete_table('analysis_compositiontype')

        # Deleting model 'Collection'
        db.delete_table('analysis_collection')

        # Deleting model 'Composition'
        db.delete_table('analysis_composition')


    models = {
        'analysis.collection': {
            'Meta': {'object_name': 'Collection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imslp_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.composer': {
            'Meta': {'object_name': 'Composer'},
            'date_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_death': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imslp_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'place_birth': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'place_death': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'time_period': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.composition': {
            'Meta': {'object_name': 'Composition'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.Collection']"}),
            'composer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.Composer']"}),
            'composition_type': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.CompositionType']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imslp_filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'misc_notes': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'music_data': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.MusicData']"}),
            'pagecount': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publisher_information': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rating': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'raw_pagecount': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'uploader': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.compositiontype': {
            'Meta': {'object_name': 'CompositionType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.musicdata': {
            'Meta': {'object_name': 'MusicData'},
            'ambitus': ('django.db.models.fields.IntegerField', [], {}),
            'contour': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'durations': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True', 'dbtype': "'float'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervals': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True', 'dbtype': "'varchar'"}),
            'intervals_midi': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'intervals_with_direction': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True', 'dbtype': "'varchar'"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'key_midi': ('django.db.models.fields.IntegerField', [], {}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'notes_midi': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'preview': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'score': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.MusicXMLScore']"}),
            'time_signature': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'total_duration': ('django.db.models.fields.FloatField', [], {})
        },
        'analysis.musicxmlscore': {
            'Meta': {'object_name': 'MusicXMLScore'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['analysis']