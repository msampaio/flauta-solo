from collections import Counter
from django.utils.datastructures import SortedDict
import numpy
from analysis.computation import utils


def get_ambitus_list(compositions):
    return [c.music_data.ambitus for c in compositions]


def frequency(ambitus_list):
    frequency = Counter(ambitus_list)

    r = [['Ambitus', 'Pieces']]
    for k, v in sorted(frequency.items()):
        r.append([k, v])
    return r


def basic_stats(ambitus_list):
    freq = Counter(ambitus_list)
    freq_values = list(freq.values())

    data = SortedDict([
            ('Min', min(ambitus_list)),
            ('Max', max(ambitus_list)),
            ('Mean', numpy.mean(ambitus_list)),
            ('Median', numpy.median(ambitus_list)),
            ('Standard deviation', numpy.std(ambitus_list)),
            ('Quartile 1', numpy.percentile(ambitus_list, 25)),
            ('Quartile 3', numpy.percentile(ambitus_list, 75)),
            ('Pieces with most common', max(freq.values())),
            ('Pieces with less common', min(freq.values())),
            ('Pieces amount mean', numpy.mean(freq_values)),
            ('Pieces amount median', numpy.median(freq_values)),
            ('Pieces amount standard deviation', numpy.std(freq_values)),
            ('Pieces amount Quartile 1', numpy.percentile(freq_values, 25)),
            ('Pieces amount Quartile 3', numpy.percentile(freq_values, 75)),
            ('Pieces number', len(ambitus_list)),
    ])
    return data


def distribution_value(ambitus_list):

    basic_data = basic_stats(ambitus_list)
    mu = basic_data['Mean']
    sigma = basic_data['Standard deviation']

    normalized = [utils.normalization(value, mu, sigma) for value in ambitus_list]

    bins = 10
    histogram = numpy.histogram(normalized, bins)
    total = histogram[0].sum()

    r = [['Sigma', 'Histogram', 'Ambitus distribution', 'Normal distribution']]

    values = zip(histogram[0], histogram[1])

    for v, k in values:
        r.append([k, v / total, v/total, utils.normal_distribution(k, 0, 1)])

    return r


def distribution_amount(ambitus_list):

    freq = Counter(ambitus_list)
    basic_data = basic_stats(ambitus_list)
    mu = basic_data['Pieces amount mean']
    sigma = basic_data['Pieces amount standard deviation']

    normalized = [utils.normalization(value, mu, sigma) for value in list(freq.values())]

    bins = 10
    histogram = numpy.histogram(normalized, bins)
    total = histogram[0].sum()

    r = [['Sigma', 'Histogram', 'Pieces amount distribution', 'Normal distribution']]

    values = zip(histogram[0], histogram[1])

    for v, k in values:
        r.append([k, v / total, v/total, utils.normal_distribution(k, 0, 1)])

    return r

def analysis(compositions):

    ambitus_list = get_ambitus_list(compositions)
    basic_stats_dic = basic_stats(ambitus_list)
    distribution_value(ambitus_list)

    args = {
        'basic_stats': basic_stats_dic,
        'frequency': frequency(ambitus_list),
        'histogram': utils.histogram(ambitus_list, 10, ['Ambitus', 'Pieces'], False, True),
        'distribution_value': distribution_value(ambitus_list),
        'distribution_amount': distribution_amount(ambitus_list),
        'boxplot': utils.boxplot(basic_stats_dic),
    }

    return args
