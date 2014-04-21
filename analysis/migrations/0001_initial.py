# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Composer'
        db.create_table('analysis_composer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date_birth', self.gf('django.db.models.fields.DateField')()),
            ('date_death', self.gf('django.db.models.fields.DateField')()),
            ('place_birth', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('place_death', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nationality', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('time_period', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('analysis', ['Composer'])

        # Adding model 'CompositionType'
        db.create_table('analysis_compositiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('analysis', ['CompositionType'])

        # Adding model 'Composition'
        db.create_table('analysis_composition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('composer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.Composer'])),
            ('composition_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.CompositionType'])),
            ('imslp_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
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
            ('notes_midi', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True)),
            ('notes', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True)),
            ('intervals', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True)),
            ('intervals_with_direction', self.gf('djorm_pgarray.fields.ArrayField')(null=True, default=None, blank=True)),
            ('durations', self.gf('djorm_pgarray.fields.ArrayField')(null=True, dbtype='float', blank=True, default=None)),
        ))
        db.send_create_signal('analysis', ['Composition'])

        # Adding model 'Collection'
        db.create_table('analysis_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('compositions', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.Composition'])),
        ))
        db.send_create_signal('analysis', ['Collection'])


    def backwards(self, orm):
        # Deleting model 'Composer'
        db.delete_table('analysis_composer')

        # Deleting model 'CompositionType'
        db.delete_table('analysis_compositiontype')

        # Deleting model 'Composition'
        db.delete_table('analysis_composition')

        # Deleting model 'Collection'
        db.delete_table('analysis_collection')


    models = {
        'analysis.collection': {
            'Meta': {'object_name': 'Collection'},
            'compositions': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.Composition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.composer': {
            'Meta': {'object_name': 'Composer'},
            'date_birth': ('django.db.models.fields.DateField', [], {}),
            'date_death': ('django.db.models.fields.DateField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'place_birth': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'place_death': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time_period': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.composition': {
            'Meta': {'object_name': 'Composition'},
            'composer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.Composer']"}),
            'composition_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.CompositionType']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'durations': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'dbtype': "'float'", 'blank': 'True', 'default': 'None'}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imslp_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'intervals': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'intervals_with_direction': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'misc_notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'notes_midi': ('djorm_pgarray.fields.ArrayField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'pagecount': ('django.db.models.fields.IntegerField', [], {}),
            'publisher_information': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'raw_pagecount': ('django.db.models.fields.IntegerField', [], {}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'uploader': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'analysis.compositiontype': {
            'Meta': {'object_name': 'CompositionType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['analysis']