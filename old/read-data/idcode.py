#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class IdCodeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def id_code_checker(id_code_dic):

    n = [str(x) for x in range(100)]
    n.append(None)
    w = list('abcdefghijklmnopqrstuvwxyz')
    w.append(None)

    conditions_one = [
        id_code_dic['source_origin'] in list('EI'),
        id_code_dic['source_type'] in list('FT'),
        len(id_code_dic['source_id']) == 5
        ]

    conditions_two = [
        not 'source_song_number' in id_code_dic or id_code_dic['source_song_number'] in n,
        not 'source_movement' in id_code_dic or id_code_dic['source_movement'] in w,
        id_code_dic['source_expansion'] in (True, False)
        ]

    if not all(conditions_one) and all(conditions_two):
        raise IdCodeError('The given id_code is wrong.')


def id_code_parser(id_code):
    """Return a dictionary with id_code parsed.

    >>> id_code_parser('ET00001_12aE')
    {'source_expansion': True,
    'source_id': '00001',
    'source_movement': 'a',
    'source_origin': 'E',
    'source_song_number': '1',
    'source_type': 'T'}
    """

    splitted = id_code.split('-')
    prefix = splitted[0]

    id_code_dic = {}

    if len(splitted) > 1:
        id_code_dic['source_suffix'] = ' '.join(splitted[1:])

    id_code_dic['source_origin'] = prefix[0]
    id_code_dic['source_type'] = prefix[1]

    if prefix[-1] == 'E':
        id_code_dic['source_expansion'] = True
        prefix = prefix.rstrip('E')
    else:
        id_code_dic['source_expansion'] = False

    if '_' in prefix:
        pre_prefix, middle = prefix.split('_')

        source_song_number, source_movement = re.match(r"([0-9]*)([a-z]*)", middle).groups()

        if source_song_number is not None:
            id_code_dic['source_song_number'] = source_song_number

        if source_movement is not None:
            id_code_dic['source_movement'] = source_movement

    if 'pre_prefix' in locals():
        id_code_dic['source_id'] = pre_prefix[2:]
    else:
        id_code_dic['source_id'] = re.match(r"([0-9]*)([a-z]*)", prefix[2:]).groups()[0]

    try:
        id_code_checker(id_code_dic)
        return id_code_dic
    except IdCodeError():
        print 'IdCode Error'


def id_code_maker(source_origin, source_type, source_id, source_song_number=None, source_movement=None, source_expansion=False, source_suffix=None):
    """Return an id_code in a string.

    >>> id_code_maker('E', 'T', '00001', '23', 'a', True, 'Foobar')
    'ET00001_23aE-Foobar'
    """

    prefix = ''.join([source_origin, source_type, source_id])

    optionals = []

    if source_song_number:
        optionals.append('_' + source_song_number)
    if source_movement:
        optionals.append(source_movement)
    if source_expansion:
        optionals.append('E')
    if source_suffix:
        optionals.append('-' + source_suffix)

    suffix = ''.join(optionals)

    return prefix + suffix
