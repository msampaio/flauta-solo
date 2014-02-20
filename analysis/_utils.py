#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import ConfigParser
import idcode

def dateParser(dateString):
    """Return a datetime object from a dateString argument in
    format YYYYMMDD."""

    y, m, d = [int(s) for s in dateString[:4], dateString[4:6], dateString[6:]]
    return datetime.date(y, m, d)


def nameParser(completeNameStr):
    """Return prename and name in two separate strings."""

    names = completeNameStr.split()
    return ' '.join(names[:-1]), names[-1:][0]


def equalityComparisons(objectOne, objectTwo, inequality=False):
    attribList = objectOne.__dict__.keys()
    if attribList != objectTwo.__dict__.keys():
        return False
    else:
        comparisons = []
        if objectOne and objectTwo:
            for method in ['__class__', '__dict__']:
                methodOne = getattr(objectOne, method)
                methodTwo = getattr(objectTwo, method)
                comparisons.append(methodOne == methodTwo)
            for atrb in attribList:
                atrbOne = objectOne.__getattribute__(atrb)
                atrbTwo = objectTwo.__getattribute__(atrb)
                comparisons.append(atrbOne == atrbTwo)
        else:
            comparisons.append(False)
        if inequality:
            return not all(comparisons)
        else:
            return all(comparisons)


def getCfgInfo(section, item, cfgFile='.musiAnalysis.cfg'):
    """Return a given item from a section in config file."""

    basename = os.path.expanduser('~')
    path = os.path.join(basename, cfgFile)
    config = ConfigParser.ConfigParser()
    config.read(path)

    return config.get(section, item)


def dicAddAttrib(outputDic, inputDic, pair):
    """Set an attribute from a input dictionary in a output one. The
    pair is the key in both dictionaries."""

    if pair[1] in inputDic:
        setattr(outputDic, pair[0], inputDic[pair[1]])


def splitFileName(absFilename):
    """Return id and song number from a given absolute path
    filename.

    >>> splitFileName('Flauta Solo/Partituras')
    """

    basename = os.path.basename(absFilename)

    idCode = idcode.idCodeParser(basename.strip('.xml'))
    idNumber = idCode['sourceId']

    if 'sourceSongNumber' in idCode:
        songNumber = idCode['sourceSongNumber']
    else:
        songNumber = None

    if 'sourceMovement' in idCode:
        movement = idCode['sourceMovement']
    else:
        movement = None

    return idNumber, songNumber, movement


def getXmlFiles(path):
    """Return a list of xml files from a given path."""

    return [f for f in os.listdir(path) if f.endswith('.xml') and f.startswith('IF')]
