#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import urllib2
import json
import _utils


class ImslpSource(object):
    """Class for IMSLP Source info."""

    def __init__(self):

        self.id = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<ImslpSource: {0}>".format(self.id)


def makeURL(dic):
    initURL = 'http://imslp.org/imslpscripts/API.ISCR.php?'
    data = []
    for k, v in dic.items():
        data.append('{0}={1}'.format(k, v))

    return initURL + '/'.join(data)


def makeDic(idNumber, retformat='json'):
    dic = {}
    dic['account'] = _utils.getCfgInfo('Imslp', 'user')
    dic['type'] = '3'
    dic['id'] = base64.b64encode(idNumber)
    dic['disclaimer'] = 'accepted'
    dic['retformat'] = retformat

    return dic


def download(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return html


def getInfo(idNumber, retformat='json'):
    """Return a dictionary with data retrieved from IMSLP."""
    dic = makeDic(idNumber, retformat)
    url = makeURL(dic)
    string = download(url)

    return json.loads(string)


def makeImslpSource(idNumber):
    """Return an object of ImslpSource class."""


    imslpSource = ImslpSource()
    dic = getInfo(idNumber)['0']

    setattr(imslpSource, 'parent', dic['parent'])

    extvals = dic['extvals']
    setattr(imslpSource, 'editor', extvals['Editor'])
    setattr(imslpSource, 'publisherInformation', extvals['Publisher Information'])
    setattr(imslpSource, 'miscNotes', extvals['Misc. Notes'])

    intvals = dic['intvals']

    for k in intvals.keys():
        if k.isdigit:
            if 'index' in intvals[k]:
                if intvals[k]['index'] == idNumber:
                    scoreInfo = intvals[k]
                    setattr(imslpSource, 'description', scoreInfo['description'])
                    setattr(imslpSource, 'uploader', scoreInfo['uploader'])
                    setattr(imslpSource, 'id', scoreInfo['index'])
                    setattr(imslpSource, 'timestamp', scoreInfo['timestamp'])
                    setattr(imslpSource, 'pagecount', scoreInfo['pagecount'])
                    setattr(imslpSource, 'rawpagecount', scoreInfo['rawpagecount'])
                    setattr(imslpSource, 'rating', scoreInfo['rating'])

    return imslpSource
