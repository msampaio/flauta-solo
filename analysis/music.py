#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music21
import _utils


def getScore(idCode, movement=None):
    """Return a Music21 score from a given idCode."""

    base = _utils.getCfgInfo('Scores', 'path')
    filename = 'IF' + idCode

    if movement:
        path = filename + '_' + movement
    path = os.path.join(base, path + '.xml')

    mScore = music21.converter.parse(path)

    return mScore
