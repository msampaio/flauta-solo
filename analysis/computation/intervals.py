from collections import Counter
from django.utils.datastructures import SortedDict
import numpy
from analysis.computation import utils


def get_midi_intervals(compositions):
    return [c.music_data.intervals_midi for c in compositions]


def get_chromatic_intervals(compositions):
    return [c.music_data.intervals for c in compositions]


def count_intervals(intervals_list, proportional=False, limit=48):
    counted = Counter(intervals_list)
    total = len(intervals_list)

    if limit:
        intervals_range = range(-limit, limit + 1)
        for i in intervals_range:
            if i not in counted:
                counted[i] = 0
            if proportional:
                counted[i] /= total

    return counted


def get_piece_frequency(intervals_list, proportional=False, limit=48):
    counted = count_intervals(intervals_list, proportional, limit)

    return numpy.array([v for _, v in sorted(counted.items())])


def get_frequency(intervals_list, normalized=False, limit=48):
    seq = [get_piece_frequency(s, normalized, limit) for s in intervals_list]

    array = numpy.array(seq)

    if normalized:
        row_size = len(array[0])
        for i in range(row_size):
            utils.normalize_array(array, 1)

    return array


def array_to_pairs(array, init=None):
    pairs = []
    for column in range(len(array[0])):
        rows = array[:, column]
        for row in rows:
            c = column
            if init:
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
    all_intervals = utils.flatten(intervals)
    r = utils.aux_pie_chart(count_intervals(all_intervals))
    r.insert(0, ['Interval', 'Amount'])
    return r


def chromatic_frequency_pie(chromatic_intervals):
    all_chromatic_intervals = utils.flatten(chromatic_intervals)
    r = utils.aux_pie_chart(count_intervals(all_chromatic_intervals, False, None))
    r.insert(0, ['Interval', 'Amount'])
    return r


def chromatic_leaps_frequency_pie(chromatic_intervals):
    all_chromatic_intervals = utils.flatten(chromatic_intervals)
    counted = count_intervals(all_chromatic_intervals, False, None)
    for i in ['P1', 'M2', 'm2', 'M3', 'm3']:
        del counted[i]
    r = utils.aux_pie_chart(counted)
    r.insert(0, ['Interval', 'Amount'])
    return r


def basic_stats(intervals_list):
    all_intervals = utils.flatten(intervals_list)
    data = SortedDict([
            ('Min', min(all_intervals)),
            ('Max', max(all_intervals)),
            ('Mean', numpy.mean(all_intervals)),
            ('Standard deviation', numpy.std(all_intervals)),
            ('Pieces number', len(intervals_list)),
            ])
    return data


def analysis(compositions):
    midi_intervals = get_midi_intervals(compositions)
    all_midi_intervals = utils.flatten(midi_intervals)
    chromatic_intervals = get_chromatic_intervals(compositions)
    args = {
        'frequency_scatter': frequency_scatter(midi_intervals),
        'basic_stats': basic_stats(midi_intervals),
        'frequency_pie': frequency_pie(midi_intervals),
        'chromatic_frequency_pie': chromatic_frequency_pie(chromatic_intervals),
        'chromatic_leaps_frequency_pie': chromatic_leaps_frequency_pie(chromatic_intervals),
        'histogram': utils.histogram(all_midi_intervals, 10, ['Intervals', 'Ocurrences'], False, True),
    }

    return args
