#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _utils


class Country(object):
    """Class for Country objects."""

    def __init__(self):

        self.name = None
        self.continent = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Country: {0}, {1}>".format(self.name, self.continent)


class City(Country):
    """Class for City objects."""

    def __init__(self):

        self.name = None
        self.province = None
        self.country = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<City: {0}, {1}>".format(self.name, self.country.name)


class Composer(object):
    """Class for Composer objects."""

    def __init__(self):

        self.name = None
        self.prename = None
        self.gender = None
        self.bornCity = None
        self.bornDate = None
        self.deathCity = None
        self.deathDate = None
        self.mainInstrument = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        if self.bornDate:
            bornDate = self.bornDate.year
        else:
            bornDate = None

        if self.deathDate:
            deathDate = self.deathDate.year
        else:
            deathDate = None

        if self.bornCity:
            bornCity = self.bornCity.country.name
        else:
            bornCity = None

        return "<Composer: {0}, {1}, {2}--{3}>".format(self.name, bornCity, bornDate, deathDate)

    def completeName(self):
        return ' '.join([self.prename, self.name])


class Editor(object):
    """Class for Editor objects."""

    def __init__(self):

        self.name = None
        self.prename = None
        self.gender = None
        self.bornCity = None
        self.bornDate = None
        self.deathCity = None
        self.deathDate = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        if self.bornDate:
            bornDate = self.bornDate.year
        else:
            borndDate = None

        if self.deathDate:
            deathDate = self.deathDate.year
        else:
            deathDate = None

        return "<Editor: {0}, {1}, {2}--{3}>".format(self.name, self.bornCity.country.name, bornDate, deathDate)

    def completeName(self):
        return ' '.join([self.prename, self.name])


class Piece(object):
    """Class for Piece objects."""

    def __init__(self):

        self.title = None
        self.subtitle = None
        self.composer = None
        self.city = None
        self.date = None
        self.premierCity = None
        self.premierDate = None
        self.opus = None
        self.classificationCode = None
        self.movements = None
        self.structure = None
        self.tonality = None
        self.instrument = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Piece: {0}, {1}>".format(self.title, self.composer.completeName())


class Movement(object):
    """Class for Movement objects."""

    def __init__(self):

        self.title = None
        self.subtitle = None
        self.tempo = None
        self.tonality = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<Movement: {0}>".format(self.title)


class Source(object):
    """Class for Source objects."""

    def __init__(self):

        self.title = None
        self.editor = None
        self.idCode = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        if self.idCode:
            idCode = self.idCode
        else:
            idCode = None
        return "<Source: {0}, {1}>".format(self.title, idCode)


class Score(object):
    """Class for Score objects. Scores are sources segments."""

    def __init__(self):

        self.source = None
        self.piece = None
        self.idCode = None
        self.mscore = None
        self.formAnalysis = None

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


def makeCountry(name, continent):
    """Return a Country object with the given attributes."""

    country = Country()
    country.name = name
    country.continent = continent

    return country


def makeCity(name, countryObj, province=None):
    """Return a City object with the given attributes."""

    city = City()
    city.name = name
    city.country = countryObj
    city.province = province

    return city


def makeComposer(completeName, gender='M', bornCityObj=None, bornDate=None, deathCityObj=None, deathDate=None, mainInstrument=None):
    """Return a Composer object with the given attributes. The dates
    must be in a string with the format YYYYMMDD."""

    composer = Composer()
    composer.prename, composer.name = _utils.nameParser(completeName)
    composer.gender = gender
    composer.bornCity = bornCityObj
    composer.deathCity = deathCityObj
    composer.mainInstrument = mainInstrument

    if bornDate:
        composer.bornDate = _utils.dateParser(bornDate)
    if deathDate:
        composer.deathDate = _utils.dateParser(deathDate)

    return composer


def makeEditor(completeName, gender='M', bornCityObj=None, bornDate=None, deathCityObj=None, deathDate=None):
    """Return an Editor object with the given attributes. The dates
    must be in a string with the format YYYYMMDD."""

    editor = Editor()
    editor.prename, editor.name = _utils.nameParser(completeName)
    editor.gender = gender
    editor.bornCity = bornCityObj
    editor.deathCity = deathCityObj

    if bornDate:
        editor.bornDate = _utils.dateParser(bornDate)
    if deathDate:
        editor.deathDate = _utils.dateParser(deathDate)

    return editor


def makePiece(title, composer, tonality=None, date=None, subtitle=None, city=None, premierCity=None, premierDate=None, opus=None, classificationCode=None, movements=None, structure=None, instrument=None):
    """Return a Piece object with the given attributes. The dates must
    be in a string with the format YYYYMMDD."""

    piece = Piece()

    piece.title = title
    piece.subtitle = subtitle
    piece.composer = composer
    piece.city = city
    piece.premierCity = premierCity
    piece.opus = opus
    piece.classificationCode = classificationCode
    piece.movements = movements
    piece.structure = structure
    piece.tonality = tonality
    piece.instrument = instrument

    if date:
        piece.date = _utils.dateParser(date)
    if premierDate:
        piece.premierDate = _utils.dateParser(premierDate)

    return piece


def makeMovement(title, tempo, tonality, subtitle=None):
    """Return a Movement object with the given attributes."""

    movement = Movement()

    movement.title = title
    movement.subtitle = subtitle
    movement.tempo = tempo
    movement.tonality = tonality

    return movement


def makeSource(idCode, title, editorObj):
    """Return a Source object with the given attributes."""

    source = Source()

    source.idCode = idCode
    source.title = title
    source.editor = editorObj

    return source


def makeScore(sourceObj, pieceObj, idCode, mscore=None, formAnalysis=None):
    """Return a Score object with the given attributes."""

    score = Score()

    score.source = sourceObj
    score.piece = pieceObj
    score.idCode = idCode
    score.mscore = mscore
    score.formAnalysis = formAnalysis

    # FIXME: use music21 to get these
    # score.timeSignature = timeSignature
    # score.meter = meter
    # score.key = key
    # score.mode = mode

    return score
