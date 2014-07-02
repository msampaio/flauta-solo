from collections import Counter
from django.utils.datastructures import SortedDict
import numpy
from analysis.computation import utils


def frequency_scatter(intervals):
    counted = utils.special_counter(intervals, True)
    seq = sorted(map(list, counted.items()))
    seq.insert(0, ['Interval', 'Amount'])
    return seq


def frequency_basic_scatter(intervals):
    simple_intervals = [abs(x) % 12 for x in intervals]
    counted = utils.special_counter(simple_intervals, True)
    seq = sorted(map(list, counted.items()))
    seq.insert(0, ['Interval', 'Amount'])
    return seq


def frequency_pie(intervals):
    r = utils.aux_pie_chart(utils.special_counter(intervals))
    r.insert(0, ['Interval', 'Amount'])
    return r


def chromatic_frequency_pie(chromatic_intervals):
    r = utils.aux_pie_chart(utils.special_counter(chromatic_intervals, False))
    r.insert(0, ['Interval', 'Amount'])
    return r


def chromatic_leaps_frequency_pie(chromatic_intervals):
    counted = utils.special_counter(chromatic_intervals, False)
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
    midi_intervals = utils.get_music_data_attrib(compositions, 'intervals_midi')
    chromatic_intervals = utils.get_music_data_attrib(compositions, 'intervals')

    if midi_intervals and chromatic_intervals:
        args = {
            'frequency_scatter': frequency_scatter(midi_intervals),
            'frequency_basic_scatter': frequency_basic_scatter(midi_intervals),
            'basic_stats': basic_stats(midi_intervals),
            'frequency_pie': frequency_pie(midi_intervals),
            'chromatic_frequency_pie': chromatic_frequency_pie(chromatic_intervals),
            'chromatic_leaps_frequency_pie': chromatic_leaps_frequency_pie(chromatic_intervals),
            'histogram': utils.histogram(midi_intervals, 10, ['Intervals', 'Ocurrences'], False, True),
            'distribution_amount': distribution_amount(midi_intervals),
        }
    else:
        args = {}

    return args
