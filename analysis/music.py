#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music21
import _utils


def get_contour(number_sequence):
    """Return a flatten contour."""

    transition = {}
    for new, old in enumerate(sorted(list(set(number_sequence)))):
        transition[old] = new

    return [transition[new] for new in number_sequence]


def get_chromatic_ambitus(pitches):
    """Return an integer with ambitus chromatic semitones."""

    return max(pitches) - min(pitches)

def get_score(id_code, song=None, movement=None):
    """Return a Music21 score from a given id_code."""

    base = _utils.get_cfg_info('Scores', 'path')
    filename = 'IF' + id_code

    # Song test
    if song is not None:
        filename = filename + '_' + song

        # Movement test
        if movement:
            filename = filename + movement

    path = os.path.join(base, filename + '.xml')

    # expand the path in case it's in the format ~/myfile
    expanded_path = os.path.expanduser(path)

    return music21.converter.parse(expanded_path) if os.path.exists(expanded_path) else None


def get_info_about_mscore(mscore):
    """Insert Music information such as Time Signature in Source
    object."""

    filename = os.path.basename(mscore.filePath)
    print '. Getting info from source {0}'.format(filename)

    part = mscore.getElementsByClass('Part')[0]
    measures = part.getElementsByClass('Measure')
    m1 = measures[0]
    time_signature_obj = m1.getElementsByClass('TimeSignature')[0]
    time_signature = '/'.join([str(i) for i in time_signature_obj.numerator, time_signature_obj.denominator])
    meter = time_signature_obj.beatCountName
    keyObj, mode = m1.getElementsByClass('KeySignature')[0].pitchAndMode
    key = keyObj.fullName

    flatten = mscore.flat
    notesObj = flatten.getElementsByClass('Note')

    notes = []
    pitches = []
    durations = []

    for note in notesObj:
        notes.append(note.nameWithOctave)
        pitches.append(note.midi)
        durations.append(note.duration.quarterLength)

    dic = {}
    dic['time_signature'] = time_signature
    dic['meter'] = meter
    dic['mode'] = mode
    dic['key'] = key
    dic['notes'] = notes
    dic['pitches'] = pitches
    dic['durations'] = durations
    dic['pitch_contour'] = get_contour(pitches)
    dic['duration_contour'] = get_contour(durations)
    dic['ambitus'] = get_chromatic_ambitus(pitches)

    return dic
