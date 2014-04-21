from django.db import models
from djorm_pgarray.fields import ArrayField


class Composer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_birth = models.DateField()
    date_death = models.DateField()
    place_birth = models.CharField(max_length=200)
    place_death = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    time_period = models.CharField(max_length=200)


class CompositionType(models.Model):
    """Things like Symphony, Etude, etc"""
    name = models.CharField(max_length=200)


class Composition(models.Model):
    composer = models.ForeignKey(Composer)
    composition_type = models.ForeignKey(CompositionType)

    imslp_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    editor = models.CharField(max_length=200)
    publisher_information = models.CharField(max_length=200)
    misc_notes = models.CharField(max_length=200)
    description = models.TextField()
    uploader = models.CharField(max_length=200)
    #timestamp = models.CharField(max_length=200)
    pagecount = models.IntegerField()
    raw_pagecount = models.IntegerField()
    rating = models.IntegerField()

    notes_midi = ArrayField(dbtype="int")
    # notes are represented in base40
    notes = ArrayField(dbtype="int")
    intervals = ArrayField(dbtype="int")
    intervals_with_direction = ArrayField(dbtype="int")
    durations = ArrayField(dbtype="float")


class Collection(models.Model):
    name = models.CharField(max_length=200)
    compositions = models.ForeignKey(Composition)
