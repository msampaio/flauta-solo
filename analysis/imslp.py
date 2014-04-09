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
        return _utils.equality_comparisons(self, other)

    def __ne__(self, other):
        return _utils.equality_comparisons(self, other, True)

    def __repr__(self):
        return "<ImslpSource: {0}>".format(self.id)

    def get_composer(self):
        """Return the source composer. Retrieves from IMSLP
        database."""

        return make_imslp_composer(self.parent_composer)


class ImslpComposer(object):
    """Class for IMSLP Composer info."""

    def __init__(self):

        self.normal_name = None

    def __eq__(self, other):
        return _utils.equality_comparisons(self, other)

    def __ne__(self, other):
        return _utils.equality_comparisons(self, other, True)

    def __repr__(self):
        return "<ImslpComposer: {0}>".format(unicode(self.normal_name).encode('utf-8'))


def make_url(dic):
    initURL = 'http://imslp.org/imslpscripts/API.ISCR.php?'
    data = []
    for k, v in dic.items():
        data.append('{0}={1}'.format(k, v))

    return initURL + '/'.join(data)


def make_dic(id_number, i_type='3', retformat='json'):
    dic = {}
    dic['account'] = _utils.get_cfg_info('Imslp', 'user')
    dic['type'] = i_type
    if i_type == '1':
        id_number = 'Category:' + id_number

    dic['id'] = base64.b64encode(id_number)
    dic['disclaimer'] = 'accepted'
    dic['retformat'] = retformat

    return dic


def download(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return html


def get_info(id_number, i_type='3', retformat='json'):
    """Return a dictionary with data retrieved from IMSLP."""

    dic = make_dic(id_number.lstrip('0'), i_type, retformat)
    url = make_url(dic)
    string = download(url)

    return json.loads(string)


def make_imslp_source(id_number):
    """Return an object of ImslpSource class."""

    imslp_source = ImslpSource()
    dic = get_info(id_number, '3')['0']

    extvals = dic['extvals']
    intvals = dic['intvals']

    ext_seq = (
        ('editor', 'Editor'),
        ('publisherInformation', 'Publisher Information'),
        ('miscNotes', 'Misc. Notes')
        )

    score_info_seq = (
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
    parent_composer = parent[parent.find("(")+1:parent.find(")")]

    setattr(imslp_source, 'parent', parent)
    setattr(imslp_source, 'parent_composer', parent_composer)

    for ext_pair in ext_seq:
        _utils.dic_add_attrib(imslp_source, extvals, ext_pair)

    for k in intvals.keys():
        if k.isdigit:
            if 'index' in intvals[k]:
                if intvals[k]['index'] == id_number:
                    score_info = intvals[k]
                    for score_info_pair in score_info_seq:
                        _utils.dic_add_attrib(imslp_source, score_info, score_info_pair)

    return imslp_source


def make_imslp_composer(id_number):
    """Return an object of ImslpComposer class."""

    imslp_composer = ImslpComposer()
    dic = get_info(unicode(id_number).encode('utf-8'), '1')['0']

    parent = dic['parent']
    extvals = dic['extvals']
    intvals = dic['intvals']

    ext_seq = (('birthDate', 'Birth Date'),
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
              ('normal_name', 'normalname'),
              ('pictureLinkRaw', 'picturelinkraw'),
              ('rawCats', 'rawcats'),
              ('totalDate', 'totaldate'))

    setattr(imslp_composer, 'parent', parent)

    for ext_pair in ext_seq:
        _utils.dic_add_attrib(imslp_composer, extvals, ext_pair)

    for int_pair in intSeq:
        _utils.dic_add_attrib(imslp_composer, intvals, int_pair)

    return imslp_composer
