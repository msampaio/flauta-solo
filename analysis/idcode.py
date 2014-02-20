#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class IdCodeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def idCodeChecker(idCodeDic):

    n = [str(x) for x in range(100)]
    n.append(None)
    w = list('abcdefghijklmnopqrstuvwxyz')
    w.append(None)

    conditionsOne = [
        idCodeDic['sourceOrigin'] in list('EI'),
        idCodeDic['sourceType'] in list('FT'),
        len(idCodeDic['sourceId']) == 5
        ]

    conditionsTwo = [
        not 'sourceSongNumber' in idCodeDic or idCodeDic['sourceSongNumber'] in n,
        not 'sourceMovement' in idCodeDic or idCodeDic['sourceMovement'] in w,
        idCodeDic['sourceExpansion'] in (True, False)
        ]

    if not all(conditionsOne) and all(conditionsTwo):
        raise IdCodeError('The given idCode is wrong.')


def idCodeParser(idCode):
    """Return a dictionary with idCode parsed.

    >>> idCodeParser('ET00001_12aE')
    {'sourceExpansion': True,
    'sourceId': '00001',
    'sourceMovement': 'a',
    'sourceOrigin': 'E',
    'sourceSongNumber': '1',
    'sourceType': 'T'}
    """

    splitted = idCode.split('-')
    prefix = splitted[0]

    idCodeDic = {}

    if len(splitted) > 1:
        idCodeDic['sourceSuffix'] = ' '.join(splitted[1:])

    idCodeDic['sourceOrigin'] = prefix[0]
    idCodeDic['sourceType'] = prefix[1]
    idCodeDic['sourceId'] = prefix[2:7]

    if prefix[-1] == 'E':
        idCodeDic['sourceExpansion'] = True
        prefix = prefix.rstrip('E')
    else:
        idCodeDic['sourceExpansion'] = False

    if '_' in prefix:
        middle = prefix.split('_')[1]

        sourceSongNumber, sourceMovement = re.match(r"([0-9]*)([a-z]*)", middle).groups()

        if sourceSongNumber != None:
            idCodeDic['sourceSongNumber'] = sourceSongNumber

        if sourceMovement != None:
            idCodeDic['sourceMovement'] = sourceMovement

    try:
        idCodeChecker(idCodeDic)
        return idCodeDic
    except IdCodeError():
        print 'IdCode Error'


def idCodeMaker(sourceOrigin, sourceType, sourceId, sourceSongNumber=None, sourceMovement=None, sourceExpansion=False, sourceSuffix=None):
    """Return an idCode in a string.

    >>> idCodeMaker('E', 'T', '00001', '23', 'a', True, 'Foobar')
    'ET00001_23aE-Foobar'
    """

    prefix = ''.join([sourceOrigin, sourceType, sourceId])

    optionals = []

    if sourceSongNumber:
        optionals.append('_' + sourceSongNumber)
    if sourceMovement:
        optionals.append(sourceMovement)
    if sourceExpansion:
        optionals.append('E')
    if sourceSuffix:
        optionals.append('-' + sourceSuffix)

    suffix = ''.join(optionals)

    return prefix + suffix
