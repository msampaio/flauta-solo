#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


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


def makeComposer(completeName, gender='M', bornCity=None, bornDate=None, deathCity=None, deathDate=None):
    """Return a Composer object with given attributes. The dates must
    be in a string with the format YYYYMMDD."""

    def dateParser(dateString):
        """Return a datetime object from a dateString argument in
        format YYYYMMDD."""

        y, m, d = [int(s) for s in dateString[:4], dateString[5:6], dateString[6:]]
        return datetime.date(y, m, d)

    def nameParser(completeName):
        """Return prename and name in two separate strings."""
        
        names = completeName.split()
        return ' '.join(names[:-1]), names[-1:][0]

    composer = Composer()
    composer.prename, composer.name = nameParser(completeName)
    composer.gender = gender
    composer.bornCity = bornCity
    composer.deathCity = deathCity

    if bornDate:
        composer.bornDate = dateParser(bornDate)
    if deathDate:
        composer.deathDate = dateParser(deathDate)

    return composer
