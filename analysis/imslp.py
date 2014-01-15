#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import urllib2
import json
import _utils


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
