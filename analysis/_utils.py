#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import ConfigParser
import idcode


def date_parser(date_string):
    """Return a datetime object from a date_string argument in
    format YYYYMMDD."""

    y, m, d = [int(s) for s in date_string[:4], date_string[4:6], date_string[6:]]
    return datetime.date(y, m, d)


def name_parser(complete_name_str):
    """Return prename and name in two separate strings."""

    names = complete_name_str.split()
    return ' '.join(names[:-1]), names[-1:][0]


def equality_comparisons(object_one, object_two, inequality=False):
    attrib_list = object_one.__dict__.keys()
    if attrib_list != object_two.__dict__.keys():
        return False
    else:
        comparisons = []
        if object_one and object_two:
            for method in ['__class__', '__dict__']:
                methodOne = getattr(object_one, method)
                methodTwo = getattr(object_two, method)
                comparisons.append(methodOne == methodTwo)
            for atrb in attrib_list:
                atrb_one = object_one.__getattribute__(atrb)
                atrb_two = object_two.__getattribute__(atrb)
                comparisons.append(atrb_one == atrb_two)
        else:
            comparisons.append(False)
        if inequality:
            return not all(comparisons)
        else:
            return all(comparisons)


def get_cfg_info(section, item, cfg_file='.musiAnalysis.cfg'):
    """Return a given item from a section in config file."""

    basename = os.path.expanduser('~')
    path = os.path.join(basename, cfg_file)
    config = ConfigParser.ConfigParser()
    config.read(path)

    return config.get(section, item)


def dic_add_attrib(outputDic, inputDic, pair):
    """Set an attribute from a input dictionary in a output one. The
    pair is the key in both dictionaries."""

    if pair[1] in inputDic:
        setattr(outputDic, pair[0], inputDic[pair[1]])


def split_filename(abs_filename):
    """Return id and song number from a given absolute path
    filename.

    >>> split_filename('Flauta Solo/Partituras')
    """

    basename = os.path.basename(abs_filename)

    id_code = idcode.id_code_parser(basename.strip('.xml'))
    id_number = id_code['source_id']

    if 'source_song_number' in id_code:
        song_number = id_code['source_song_number']
    else:
        song_number = None

    if 'source_movement' in id_code:
        movement = id_code['source_movement']
    else:
        movement = None

    return id_number, song_number, movement


def get_xml_files(path):
    """Return a list of xml files from a given path."""

    return [f for f in os.listdir(path) if f.endswith('.xml') and f.startswith('IF')]
