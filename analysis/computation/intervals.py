import numpy

from collections import Counter


def flatten(seq):
    return [el for l in seq for el in l]


def get_intervals_list(compositions):
    return [c.music_data.intervals_midi for c in compositions]



def count_intervals(intervals_list, proportional=False, limit=48):
    counted = Counter(intervals_list)
    total = len(intervals_list)

    if limit != None:
        intervals_range = range(-limit, limit + 1)
        for i in intervals_range:
            if i not in counted:
                counted[i] = 0
            if proportional:
                counted[i] = counted[i] / total

    return counted


def get_piece_frequency(intervals_list, proportional=False, limit=48):
    counted = count_intervals(intervals_list, proportional, limit)

    return numpy.array([v for _, v in sorted(counted.items())])


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


def frequency_pie(intervals):
    all_intervals = flatten(intervals)
    r = sorted(([str(k), v] for k, v in count_intervals(all_intervals).items()), key = lambda x: x[1], reverse=True)
    r.insert(0, ['Interval', 'Amount'])
    return r


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
        'frequency_pie': frequency_pie(intervals),
    }

    return args