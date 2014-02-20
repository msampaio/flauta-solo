#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music21
import _utils


def getScore(idCode, song=None, movement=None):
    """Return a Music21 score from a given idCode."""

    base = _utils.getCfgInfo('Scores', 'path')
    filename = 'IF' + idCode

    # Song test
    if song != None:
        filename = filename + '_' + song

        # Movement test
        if movement:
            filename = filename + movement

    path = os.path.join(base, filename + '.xml')

    # Xml file existence test
    if os.path.exists(path):
        mScore = music21.converter.parse(path)
    else:
        mScore = None

    return mScore


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

    return timeSignature, meter, mode, key
