#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


def dateParser(dateString):
    """Return a datetime object from a dateString argument in
    format YYYYMMDD."""

    y, m, d = [int(s) for s in dateString[:4], dateString[4:6], dateString[6:]]
    return datetime.date(y, m, d)


def nameParser(completeNameStr):
    """Return prename and name in two separate strings."""

    names = completeNameStr.split()
    return ' '.join(names[:-1]), names[-1:][0]


def equalityComparisons(objectOne, objectTwo, inequality=False):
    attribList = objectOne.__dict__.keys()
    if attribList != objectTwo.__dict__.keys():
        return False
    else:
        comparisons = []
        if objectOne and objectTwo:
            for method in ['__class__', '__dict__']:
                methodOne = getattr(objectOne, method)
                methodTwo = getattr(objectTwo, method)
                comparisons.append(methodOne == methodTwo)
            for atrb in attribList:
                atrbOne = objectOne.__getattribute__(atrb)
                atrbTwo = objectTwo.__getattribute__(atrb)
                comparisons.append(atrbOne == atrbTwo)
        else:
            comparisons.append(False)
        if inequality:
            return not all(comparisons)
        else:
            return all(comparisons)
