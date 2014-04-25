from django.db import models
from djorm_pgarray.fields import ArrayField


class MusicXMLScore(models.Model):
    filename = models.CharField(max_length=300)
    code = models.CharField(max_length=300)
    score = models.TextField()

    def __str__(self):
        return "<{}>".format(self.code)


class MusicData(models.Model):
    # in MusicXML format
    score = models.ForeignKey(MusicXMLScore)

    notes_midi = ArrayField(dbtype="int")
    # notes are represented in base40
    notes = ArrayField(dbtype="int")
    intervals = ArrayField(dbtype="varchar")
    intervals_midi = ArrayField(dbtype="int")
    intervals_with_direction = ArrayField(dbtype="varchar")
    durations = ArrayField(dbtype="float")
    contour = ArrayField(dbtype="int")

    mode = models.CharField(max_length=100)
    key = models.CharField(max_length=10)
    key_midi = models.IntegerField()
    time_signature = models.CharField(max_length=20)
    # we get it with quarterLength
    total_duration = models.FloatField()
    # as a MIDI interval
    ambitus = models.IntegerField()

    preview = models.ImageField(upload_to='preview', null=True)

    def __str__(self):
        size = len(self.notes)
        last = size - 1 if size < 10 else 10
        return "<{}...>".format(self.notes[0:last])


class Composer(models.Model):
    imslp_id = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)
    date_birth = models.DateField(blank=True, null=True)
    date_death = models.DateField(blank=True, null=True)
    # TODO: confirm if IMSLP provides birth and death places
    place_birth = models.CharField(max_length=200, blank=True, null=True)
    place_death = models.CharField(max_length=200, blank=True, null=True)
    nationality = models.CharField(max_length=200, blank=True, null=True)
    time_period = models.CharField(max_length=200)

    def __str__(self):
        return "<{}, {}>".format(self.last_name, self.first_name)

class CompositionType(models.Model):
    """Things like Symphony, Etude, etc"""
    name = models.CharField(max_length=200)


class Composition(models.Model):
    music_data = models.ForeignKey(MusicData)

    composer = models.ForeignKey(Composer)
    composition_type = models.ForeignKey(CompositionType, blank=True, null=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)

    editor = models.CharField(max_length=200)
    publisher_information = models.CharField(max_length=200)
    misc_notes = models.TextField(max_length=200)
    description = models.TextField()
    uploader = models.CharField(max_length=200)
    pagecount = models.CharField(max_length=200)
    raw_pagecount = models.CharField(max_length=200)
    rating = models.CharField(max_length=200)
    imslp_filename = models.CharField(max_length=200)

    def __str__(self):
        return "<{}>".format(self.title)

class Collection(models.Model):
    imslp_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    compositions = models.ForeignKey(Composition)
