#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import music
import _utils
import imslp


class Piece(object):
    """Class for Piece objects."""

    def __init__(self):

        self.title = None
        self.composer = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Piece: {0}, {1}>".format(self.title, self.composer.normalName)


class Score(object):
    """Class for Score objects. Scores are sources segments."""

    def __init__(self):

        self.source = None
        self.piece = None
        self.idCode = None
        self.composer = None
        self.mscore = None

        self.timeSignature = None
        self.meter = None
        self.key = None
        self.mode = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        if self.idCode:
            idCode = self.idCode
        else:
            idCode = None
        return "<Score: {0}, {1}>".format(self.piece.title, idCode)


def makePiece(title, composer):
    """Return a Piece object with the given attributes. The dates must
    be in a string with the format YYYYMMDD."""

    piece = Piece()

    piece.title = title
    piece.composer = composer

    return piece


def makeScore(sourceObj, pieceObj, idCode, composer, mscore=None):
    """Return a Score object with the given attributes."""

    score = Score()

    score.source = sourceObj
    score.piece = pieceObj
    score.idCode = idCode
    score.composer = composer
    score.mscore = mscore

    if mscore:
        dic = music.getInfoAboutMScore(mscore)

        score.timeSignature = dic['timeSignature']
        score.meter = dic['meter']
        score.key = dic['key']
        score.mode = dic['mode']
        score.notes = dic['notes']
        score.pitches = dic['pitches']
        score.durations = dic['durations']
        score.pitchContour = dic['pitchContour']
        score.durationContour = dic['durationContour']
        score.ambitus = dic['ambitus']

    return score


# FIXME: how to handle with song number and movement number?
def makeCompleteScore(idNumber, song=None, movement=None):
    """Return a complete Score object, with data retrieved from IMSLP
    and xml score.

    >>> makeCompleteScore('34491', '01')
    """

    print 'Processing score id {0}, song {1}, movement {2}'.format(idNumber, song, movement)

    imslpSource = imslp.makeImslpSource(idNumber)
    title = imslpSource.parent.split(' (')[0]
    composer = imslpSource.getComposer()
    editor = imslpSource.editor

    piece = makePiece(title, composer)
    mscore = music.getScore(idNumber, song, movement)
    score = makeScore(imslpSource, piece, idNumber, composer, mscore)

    return score


def makeScoresFromPath(path=None):
    """Return a list of Score objects from a given path with xml
    files."""

    if not path:
        path = _utils.getCfgInfo('Scores', 'path')
    files = _utils.getXmlFiles(path)

    return [makeCompleteScore(*_utils.splitFileName(f)) for f in files]
