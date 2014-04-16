#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import pickle
import _utils


def file_test(pattern, filename):
    r = re.search(pattern, filename)
    if r:
        return r.string


def get_files(pattern='^((I.*)|(E.*E)).xml$', path_to_folder=None):
    if not path_to_folder:
        user = os.path.expanduser('~')
        path_to_folder = os.path.join(user, u'Copy', u'Genos Research Group', u'Flauta Solo', u'Partituras')
    return [os.path.join(path_to_folder, f) for f in os.listdir(path_to_folder) if file_test(pattern, f)]


def get_xml_path(id_code, song=None, movement=None):

    base = _utils.get_cfg_info('Scores', 'path')
    filename = 'IF' + id_code

    # Song test
    if song is not None:
        filename = filename + '_' + song

        # Movement test
        if movement:
            filename = filename + movement

    path = os.path.join(base, filename + '.xml')

    # expand the path in case it's in the format ~/myfile
    expanded_path = os.path.expanduser(path)

    return expanded_path if os.path.exists(expanded_path) else None



# pickle
def save_pickle(path, data):
    """Save the given object in its corresponding filename."""

    pickleFile = os.path.join(path)
    with open(pickleFile, 'w') as fileobj:
        pickle.dump(data, fileobj)


def load_pickle(path):
    """Loads the object with the given structure type and idn."""

    with open(path, 'r') as fileobj:
        return pickle.load(fileobj)