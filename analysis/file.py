#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    middle = prefix[7:]
    idCodeDic['sourceExpansion'] = False

    if middle:
        if middle[-1] == 'E':
            idCodeDic['sourceExpansion'] = True
        if middle[0] == '_':
            idCodeDic['sourceSongNumber'] =  middle[1:3]
            if idCodeDic['sourceExpansion']:
                idCodeDic['sourceMovement'] = middle[3:-1]
            else:
                idCodeDic['sourceMovement'] = middle[3:]
        
    return idCodeDic
