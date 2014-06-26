import numpy

from collections import Counter


def flatten(seq):
    return [el for l in seq for el in l]


def get_intervals_list(compositions):
    return [c.music_data.intervals_midi for c in compositions]

def get_piece_frequency(intervals_list, proportional=False, limit=48):
    intervals_range = range(-limit, limit + 1)
    c = Counter()
    for i in intervals_range:
        c[i] = 0
    c.update(intervals_list)

    seq = numpy.array([c[i] for i in intervals_range])
    total = seq.sum()

    if proportional:
        seq = numpy.array([(el/total) for el in seq])

    return seq


def normalize_array(array, column=0):
    c_array = array[:,column]
    mean = c_array.mean()
    std = c_array.std()
    if std != 0:
        array[:,column] = (array[:,column] - mean) / std

    return array


def get_frequency(intervals_list, normalized=False, limit=48):
    seq = [get_piece_frequency(s, normalized, limit) for s in intervals_list]

    array = numpy.array(seq)

    if normalized:
        row_size = len(array[0])
        for i in range(row_size):
            normalize_array(array, 1)

    return array

def array_to_pairs(array, init=None):
    pairs = []
    for column in range(len(array[0])):
        rows = array[:,column]
        for row in rows:
            c = column
            if init != None:
                c = init + c
            pairs.append([c, rows[row]])
    return pairs


def frequency_scatter(intervals):
    limit = 48
    array = get_frequency(intervals, True, limit)
    seq = array_to_pairs(array, -limit)
    seq.insert(0, ['Interval', 'Amount'])
    return seq


def basic_stats(intervals_list):
    flat = flatten(intervals_list)
    data = {'Min': min(flat),
            'Max': max(flat),
            'Mean': numpy.mean(flat),
            'Standard deviation': numpy.std(flat),
            'Pieces number': len(intervals_list),
    }
    return data


def analysis(compositions):
    intervals = get_intervals_list(compositions)
    args = {
        'frequency_scatter': frequency_scatter(intervals),
        'basic_stats': basic_stats(intervals),
    }

    return args