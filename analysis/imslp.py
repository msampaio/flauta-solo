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

    def getComposer(self):
        """Return the source composer. Retrieves from IMSLP
        database."""

        return makeImslpComposer(self.parentComposer)


class ImslpComposer(object):
    """Class for IMSLP Composer info."""

    def __init__(self):

        self.normalName = None

    def __eq__(self, other):
        return _utils.equalityComparisons(self, other)

    def __ne__(self, other):
        return _utils.equalityComparisons(self, other, True)

    def __repr__(self):
        return "<ImslpComposer: {0}>".format(unicode(self.normalName).encode('utf-8'))


def makeURL(dic):
    initURL = 'http://imslp.org/imslpscripts/API.ISCR.php?'
    data = []
    for k, v in dic.items():
        data.append('{0}={1}'.format(k, v))

    return initURL + '/'.join(data)


def makeDic(idNumber, iType='3', retformat='json'):
    dic = {}
    dic['account'] = _utils.getCfgInfo('Imslp', 'user')
    dic['type'] = iType
    if iType == '1':
        idNumber = 'Category:' + idNumber

    dic['id'] = base64.b64encode(idNumber)
    dic['disclaimer'] = 'accepted'
    dic['retformat'] = retformat

    return dic


def download(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return html


def getInfo(idNumber, iType='3', retformat='json'):
    """Return a dictionary with data retrieved from IMSLP."""

    dic = makeDic(idNumber, iType, retformat)
    url = makeURL(dic)
    string = download(url)

    return json.loads(string)


def makeImslpSource(idNumber):
    """Return an object of ImslpSource class."""

    imslpSource = ImslpSource()
    dic = getInfo(idNumber, '3')['0']

    extvals = dic['extvals']
    intvals = dic['intvals']

    extSeq = (
        ('editor', 'Editor'),
        ('publisherInformation', 'Publisher Information'),
        ('miscNotes', 'Misc. Notes')
        )

    scoreInfoSeq = (
        ('description', 'description'),
        ('uploader', 'uploader'),
        ('id', 'index'),
        ('timestamp', 'timestamp'),
        ('pagecount', 'pagecount'),
        ('rawpagecount', 'rawpagecount'),
        ('rating', 'rating')
        )

    parent = dic['parent']
    # extract composer from parent
    parentComposer = parent[parent.find("(")+1:parent.find(")")]

    setattr(imslpSource, 'parent', parent)
    setattr(imslpSource, 'parentComposer', parentComposer)

    for extPair in extSeq:
        _utils.dicAddAttrib(imslpSource, extvals, extPair)

    for k in intvals.keys():
        if k.isdigit:
            if 'index' in intvals[k]:
                if intvals[k]['index'] == idNumber:
                    scoreInfo = intvals[k]
                    for scoreInfoPair in scoreInfoSeq:
                        _utils.dicAddAttrib(imslpSource, scoreInfo, scoreInfoPair)

    return imslpSource


def makeImslpComposer(idNumber):
    """Return an object of ImslpComposer class."""

    imslpComposer = ImslpComposer()
    dic = getInfo(unicode(idNumber).encode('utf-8'), '1')['0']

    parent = dic['parent']
    extvals = dic['extvals']
    intvals = dic['intvals']

    extSeq = (('birthDate', 'Birth Date'),
              ('bornDay', 'Born Day'),
              ('bornMonth', 'Born Month'),
              ('bornYear', 'Born Year'),
              ('deathDate', 'Death Date'),
              ('diedDay', 'Died Day'),
              ('diedMonth', 'Died Month'),
              ('diedYear', 'Died Year'),
              ('pictureCaption', 'Picture Caption'),
              ('timePeriod', 'Time Period'),
              ('nationality', 'Nationality'))

    intSeq = (('firstName', 'firstname'),
              ('lastName', 'lastname'),
              ('normalName', 'normalname'),
              ('pictureLinkRaw', 'picturelinkraw'),
              ('rawCats', 'rawcats'),
              ('totalDate', 'totaldate'))

    setattr(imslpComposer, 'parent', parent)

    for extPair in extSeq:
        _utils.dicAddAttrib(imslpComposer, extvals, extPair)

    for intPair in intSeq:
        _utils.dicAddAttrib(imslpComposer, intvals, intPair)

    return imslpComposer
