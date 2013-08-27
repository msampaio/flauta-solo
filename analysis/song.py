#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _utils


class Country(object):
    """Class for Country objects."""
    
    def __init__(self):

        self.name = None
        self.continent = None

    def __repr__(self):
        return "<Country: {0}, {1}>".format(self.name, self.continent)


class City(Country):
    """Class for City objects."""
    
    def __init__(self):

        self.name = None
        self.province = None
        self.country = None

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
        self.commonStyle = None

    def __repr__(self):
        if self.bornDate:
            bornDate = self.bornDate.year
        else:
            borndDate = None

        if self.deathDate:
            deathDate = self.deathDate.year
        else:
            deathDate = None

        return "<Composer: {0}, {1}, {2}--{3}>".format(self.name, self.bornCity.country.name, bornDate, deathDate)

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

    def __repr__(self):
        return "<Piece: {0}, {1}>".format(self.title, self.composer)


class Movement(object):
    """Class for Movement objects."""

    def __init__(self):

        self.title = None
        self.subtitle = None
        self.tempo = None
        self.tonality = None

    def __repr__(self):
        return "<Movement: {0}>".format(self.title)


class Source(object):
    """Class for Source objects."""

    def __init__(self):

        self.piece = None
        self.info = None
        self.editor = None
        self.idCode = None

    def __repr__(self):
        return "<Source: {0}, {1}>".format(self.piece, self.info)


def makeCountry(name, continent):
    """Return a Country object with given attributes."""

    country = Country()
    country.name = name
    country.continent = continent

    return country


def makeCity(name, countryObj, province=None):
    """Return a City object with given attributes."""

    city = City()
    city.name = name
    city.country = countryObj
    city.province = province

    return city


def makeComposer(completeName, gender='M', bornCityObj=None, bornDate=None, deathCityObj=None, deathDate=None, mainInstrument=None, commonStyle=None):
    """Return a Composer object with given attributes. The dates must
    be in a string with the format YYYYMMDD."""

    composer = Composer()
    composer.prename, composer.name = _utils.nameParser(completeName)
    composer.gender = gender
    composer.bornCity = bornCityObj
    composer.deathCity = deathCityObj
    composer.mainInstrument = mainInstrument
    composer.commonStyle = commonStyle

    if bornDate:
        composer.bornDate = _utils.dateParser(bornDate)
    if deathDate:
        composer.deathDate = _utils.dateParser(deathDate)

    return composer
