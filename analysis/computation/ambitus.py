from collections import Counter
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
    data = {'Min': min(ambitus_list),
            'Max': max(ambitus_list),
            'Mean': numpy.mean(ambitus_list),
            'Median': numpy.median(ambitus_list),
            'Quartile 1': numpy.percentile(ambitus_list, 25),
            'Quartile 3': numpy.percentile(ambitus_list, 75),
            'Standard deviation': numpy.std(ambitus_list),
            'Pieces number': len(ambitus_list)
    }
    return data


def distribution(ambitus_list):

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


def analysis(compositions):

    ambitus_list = get_ambitus_list(compositions)
    basic_stats_dic = basic_stats(ambitus_list)
    distribution(ambitus_list)

    args = {
        'basic_stats': basic_stats_dic,
        'frequency': frequency(ambitus_list),
        'histogram': utils.histogram(ambitus_list, 10, ['Ambitus', 'Pieces'], True),
        'distribution': distribution(ambitus_list),
        'boxplot': utils.boxplot(basic_stats_dic),
    }

    return args