#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music21
import _utils


def getContour(numberSequence):
    """Return a flatten contour."""

    transition = {}
    for new, old in enumerate(sorted(list(set(numberSequence)))):
        transition[old] = new

    return [transition[new] for new in numberSequence]


def getChromaticAmbitus(pitches):
    """Return an integer with ambitus chromatic semitones."""

    return max(pitches) - min(pitches)

def getScore(idCode, song=None, movement=None):
    """Return a Music21 score from a given idCode."""

    base = _utils.getCfgInfo('Scores', 'path')
    filename = 'IF' + idCode

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


def getInfoAboutMScore(mscore):
    """Insert Music information such as Time Signature in Source
    object."""

    filename = os.path.basename(mscore.filePath)
    print '. Getting info from source {0}'.format(filename)

    part = mscore.getElementsByClass('Part')[0]
    measures = part.getElementsByClass('Measure')
    m1 = measures[0]
    timeSignatureObj = m1.getElementsByClass('TimeSignature')[0]
    timeSignature = '/'.join([str(i) for i in timeSignatureObj.numerator, timeSignatureObj.denominator])
    meter = timeSignatureObj.beatCountName
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
    dic['timeSignature'] = timeSignature
    dic['meter'] = meter
    dic['mode'] = mode
    dic['key'] = key
    dic['notes'] = notes
    dic['pitches'] = pitches
    dic['durations'] = durations
    dic['pitchContour'] = getContour(pitches)
    dic['durationContour'] = getContour(durations)
    dic['ambitus'] = getChromaticAmbitus(pitches)

    return dic
