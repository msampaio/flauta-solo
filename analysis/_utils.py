#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os


def dateParser(dateString):
    """Return a datetime object from a dateString argument in
    format YYYYMMDD."""

    y, m, d = [int(s) for s in dateString[:4], dateString[5:6], dateString[6:]]
    return datetime.date(y, m, d)


def nameParser(completeNameStr):
    """Return prename and name in two separate strings."""

    names = completeNameStr.split()
    return ' '.join(names[:-1]), names[-1:][0]


def mkdir(path):
    """Make a path of a given path, if it doesn't exist."""

    if not os.path.exists(path):
        os.mkdir(path)
