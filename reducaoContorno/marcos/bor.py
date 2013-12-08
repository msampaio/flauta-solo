# -*- coding: utf-8 -*-

import copy


def reductWindow(cseg, window_size):
    """Returns a contour segment reduced by Bor Window Algorithm.

    >>> reductWindow([1, 3, 4, 2, 5, 6], 3)
    [1, 4, 2, 6]
    """

    newCseg = copy.deepcopy(cseg)
    increment = window_size / 2
    reducedCseg = []

    posInf = float('inf')
    negInf = posInf * -1

    # insert null elements in tuple edges
    for i in range(increment):
        newCseg.insert(0, negInf)
        newCseg.append(posInf)

    for j in range(increment, len(newCseg) - increment):
        left = newCseg[j - increment:j]
        right = newCseg[j+1: j + increment + 1]
        middle_point = newCseg[j]

        if any([middle_point == cseg[0],
                middle_point == cseg[-1],
                middle_point <= min(left),
                middle_point >= max(right)]):
            reducedCseg.append(middle_point)

    return reducedCseg


def reductBor(cseg, windows):
    """Returns a contour segment reduction by Bor Reduction Algorithm.

    >>> reductionBor([1, 3, 4, 2, 5, 6], 35)
    [1, 6]
    """

    reducedCseg = copy.deepcopy(cseg)
    windows = map(int, list(str(windows)))

    for window in windows:
        reducedCseg = reductWindow(reducedCseg, window)

    return reducedCseg

# Exemplos
print reductWindow([1, 3, 4, 2, 5, 6], 3)
print reductBor([1, 3, 4, 2, 5, 6], 35)
