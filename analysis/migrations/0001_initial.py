# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MusicXMLScore'
        db.create_table(u'analysis_musicxmlscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('score', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'analysis', ['MusicXMLScore'])

        # Adding model 'MusicData'
        db.create_table(u'analysis_musicdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.MusicXMLScore'])),
            ('notes_midi', self.gf('djorm_pgarray.fields.ArrayField')(default=None, null=True, blank=True)),
            ('notes', self.gf('djorm_pgarray.fields.ArrayField')(default=None, null=True, blank=True)),
            ('intervals', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='varchar', null=True, blank=True)),
            ('intervals_midi', self.gf('djorm_pgarray.fields.ArrayField')(default=None, null=True, blank=True)),
            ('intervals_with_direction', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='varchar', null=True, blank=True)),
            ('durations', self.gf('djorm_pgarray.fields.ArrayField')(default=None, dbtype='float', null=True, blank=True)),
            ('contour', self.gf('djorm_pgarray.fields.ArrayField')(default=None, null=True, blank=True)),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('key_midi', self.gf('django.db.models.fields.IntegerField')()),
            ('time_signature', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('total_duration', self.gf('django.db.models.fields.FloatField')()),
            ('ambitus', self.gf('django.db.models.fields.IntegerField')()),
            ('preview', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'analysis', ['MusicData'])

        # Adding model 'Composer'
        db.create_table(u'analysis_composer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date_birth', self.gf('django.db.models.fields.DateField')()),
            ('date_death', self.gf('django.db.models.fields.DateField')()),
            ('place_birth', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('place_death', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nationality', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('time_period', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'analysis', ['Composer'])

        # Adding model 'CompositionType'
        db.create_table(u'analysis_compositiontype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'analysis', ['CompositionType'])

        # Adding model 'Composition'
        db.create_table(u'analysis_composition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('music_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.MusicData'])),
            ('composer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.Composer'])),
            ('composition_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.CompositionType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('editor', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('publisher_information', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('misc_notes', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('uploader', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pagecount', self.gf('django.db.models.fields.IntegerField')()),
            ('raw_pagecount', self.gf('django.db.models.fields.IntegerField')()),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'analysis', ['Composition'])

        # Adding model 'Collection'
        db.create_table(u'analysis_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imslp_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('compositions', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.Composition'])),
        ))
        db.send_create_signal(u'analysis', ['Collection'])


    def backwards(self, orm):
        # Deleting model 'MusicXMLScore'
        db.delete_table(u'analysis_musicxmlscore')

        # Deleting model 'MusicData'
        db.delete_table(u'analysis_musicdata')

        # Deleting model 'Composer'
        db.delete_table(u'analysis_composer')

        # Deleting model 'CompositionType'
        db.delete_table(u'analysis_compositiontype')

        # Deleting model 'Composition'
        db.delete_table(u'analysis_composition')

        # Deleting model 'Collection'
        db.delete_table(u'analysis_collection')


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
            'composition_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analysis.CompositionType']"}),
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