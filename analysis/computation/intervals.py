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


def basic_stats(all_intervals):
    freq = Counter(all_intervals)
    freq_values = list(freq.values())

    data = SortedDict([
            ('Value Min', min(all_intervals)),
            ('Value Max', max(all_intervals)),
            ('Value Mean', numpy.mean(all_intervals)),
            ('Value Median', numpy.median(all_intervals)),
            ('Value Standard deviation', numpy.std(all_intervals)),
            ('Value Quartile 1', numpy.percentile(all_intervals, 25)),
            ('Value Quartile 3', numpy.percentile(all_intervals, 75)),
            ('Amount with most common', max(freq.values())),
            ('Amount with less common', min(freq.values())),
            ('Amount Mean', numpy.mean(freq_values)),
            ('Amount Median', numpy.median(freq_values)),
            ('Amount Standard deviation', numpy.std(freq_values)),
            ('Amount Quartile 1', numpy.percentile(freq_values, 25)),
            ('Amount Quartile 3', numpy.percentile(freq_values, 75)),
            ('Intervals number', len(all_intervals)),
    ])
    return data


def distribution_amount(all_intervals):
    freq = Counter(all_intervals)

    basic_data = basic_stats(all_intervals)
    mu = basic_data['Amount Mean']
    sigma = basic_data['Amount Standard deviation']

    normalized = [utils.normalization(value, mu, sigma) for value in list(freq.values())]

    bins = 10
    histogram = numpy.histogram(normalized, bins)
    total = histogram[0].sum()

    r = [['Sigma', 'Histogram', 'Amount distribution', 'Normal distribution']]

    values = zip(histogram[0], histogram[1])

    for v, k in values:
        r.append([k, v / total, v/total, utils.normal_distribution(k, 0, 1)])

    return r


def analysis(compositions):
    midi_intervals = get_midi_intervals(compositions)
    all_midi_intervals = utils.flatten(midi_intervals)
    chromatic_intervals = get_chromatic_intervals(compositions)
    args = {
        'frequency_scatter': frequency_scatter(midi_intervals),
        'basic_stats': basic_stats(all_midi_intervals),
        'frequency_pie': frequency_pie(midi_intervals),
        'chromatic_frequency_pie': chromatic_frequency_pie(chromatic_intervals),
        'chromatic_leaps_frequency_pie': chromatic_leaps_frequency_pie(chromatic_intervals),
        'histogram': utils.histogram(all_midi_intervals, 10, ['Intervals', 'Ocurrences'], False, True),
        'distribution_amount': distribution_amount(all_midi_intervals),
    }

    return args
