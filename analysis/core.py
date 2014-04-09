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
        return _utils.equality_comparisons(self, other)

    def __ne__(self, other):
        return _utils.equality_comparisons(self, other, True)

    def __repr__(self):
        return "<Piece: {0}, {1}>".format(self.title, self.composer.normal_name)


class Score(object):
    """Class for Score objects. Scores are sources segments."""

    def __init__(self):

        self.source = None
        self.piece = None
        self.id_code = None
        self.composer = None
        self.mscore = None

        self.time_signature = None
        self.meter = None
        self.key = None
        self.mode = None

    def __eq__(self, other):
        return _utils.equality_comparisons(self, other)

    def __ne__(self, other):
        return _utils.equality_comparisons(self, other, True)

    def __repr__(self):
        if self.id_code:
            id_code = self.id_code
        else:
            id_code = None
        return "<Score: {0}, {1}>".format(self.piece.title, id_code)


def make_piece(title, composer):
    """Return a Piece object with the given attributes. The dates must
    be in a string with the format YYYYMMDD."""

    piece = Piece()

    piece.title = title
    piece.composer = composer

    return piece


def makeScore(source_obj, piece_obj, id_code, composer, mscore=None):
    """Return a Score object with the given attributes."""

    score = Score()

    score.source = source_obj
    score.piece = piece_obj
    score.id_code = id_code
    score.composer = composer
    score.mscore = mscore

    if mscore:
        dic = music.get_info_about_mscore(mscore)

        score.time_signature = dic['time_signature']
        score.meter = dic['meter']
        score.key = dic['key']
        score.mode = dic['mode']
        score.notes = dic['notes']
        score.pitches = dic['pitches']
        score.durations = dic['durations']
        score.pitch_contour = dic['pitch_contour']
        score.duration_contour = dic['duration_contour']
        score.ambitus = dic['ambitus']

    return score


# FIXME: how to handle with song number and movement number?
def make_complete_score(id_number, song=None, movement=None):
    """Return a complete Score object, with data retrieved from IMSLP
    and xml score.

    >>> make_complete_score('34491', '01')
    """

    print 'Processing score id {0}, song {1}, movement {2}'.format(id_number, song, movement)

    imslp_source = imslp.make_imslp_source(id_number)
    title = imslp_source.parent.split(' (')[0]
    composer = imslp_source.get_composer()
    editor = imslp_source.editor

    piece = make_piece(title, composer)
    mscore = music.get_score(id_number, song, movement)
    score = makeScore(imslp_source, piece, id_number, composer, mscore)

    return score


def make_scores_from_path(path=None):
    """Return a list of Score objects from a given path with xml
    files."""

    if not path:
        path = _utils.get_cfg_info('Scores', 'path')
    files = _utils.get_xml_files(path)

    return [make_complete_score(*_utils.split_filename(f)) for f in files]
