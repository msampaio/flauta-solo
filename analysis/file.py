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

    if len(splitted) > 1:
        suffix = splitted[1:]

    idCodeDic = {}
    idCodeDic['sourceOrigin'] = prefix[0]
    idCodeDic['sourceType'] = prefix[1]
    idCodeDic['sourceId'] = prefix[2:7]

    middle = prefix[7:]

    if middle:
        if middle[-1] == 'E':
            idCodeDic['sourceExpansion'] = True
        if middle[0] == '_':
            idCodeDic['sourceSongNumber'] =  middle[1:2]
            if idCodeDic['sourceExpansion']:
                idCodeDic['sourceMovement'] = middle[3:-1]
            else:
                idCodeDic['sourceMovement'] = middle[3:]
        
    return idCodeDic
