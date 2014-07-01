from collections import Counter
from django.utils.datastructures import SortedDict
import numpy
from analysis.computation import utils


def frequency(ambitus_list):
    freq = Counter(ambitus_list)

    r = [['Ambitus', 'Pieces']]
    for k, v in sorted(freq.items()):
        r.append([k, v])
    return r


def basic_stats(ambitus_list):
    freq = Counter(ambitus_list)
    freq_values = list(freq.values())

    data = SortedDict([
            ('Value Min', min(ambitus_list)),
            ('Value Max', max(ambitus_list)),
            ('Value Mean', numpy.mean(ambitus_list)),
            ('Value Median', numpy.median(ambitus_list)),
            ('Value Standard deviation', numpy.std(ambitus_list)),
            ('Value Quartile 1', numpy.percentile(ambitus_list, 25)),
            ('Value Quartile 3', numpy.percentile(ambitus_list, 75)),
            ('Amount with most common', max(freq.values())),
            ('Amount with less common', min(freq.values())),
            ('Amount Mean', numpy.mean(freq_values)),
            ('Amount Median', numpy.median(freq_values)),
            ('Amount Standard deviation', numpy.std(freq_values)),
            ('Amount Quartile 1', numpy.percentile(freq_values, 25)),
            ('Amount Quartile 3', numpy.percentile(freq_values, 75)),
            ('Pieces number', len(ambitus_list)),
    ])
    return data


def distribution_value(ambitus_list):

    basic_data = basic_stats(ambitus_list)
    mu = basic_data['Value Mean']
    sigma = basic_data['Value Standard deviation']

    normalized = [utils.normalization(value, mu, sigma) for value in ambitus_list]

    bins = 10
    histogram = numpy.histogram(normalized, bins)
    total = histogram[0].sum()

    r = [['Sigma', 'Histogram', 'Value distribution', 'Normal distribution']]

    values = zip(histogram[0], histogram[1])

    for v, k in values:
        r.append([k, v / total, v/total, utils.normal_distribution(k, 0, 1)])

    return r


def distribution_amount(ambitus_list):

    freq = Counter(ambitus_list)
    basic_data = basic_stats(ambitus_list)
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


def frequency_pie(ambitus_list):
    r = utils.aux_pie_chart(Counter(ambitus_list))
    r.insert(0, ['Ambitus', 'Amount'])
    return r


def analysis(compositions):
    ambitus_list = utils.get_single_music_data_attrib(compositions, 'ambitus')

    if ambitus_list:
        basic_stats_dic = basic_stats(ambitus_list)
        distribution_value(ambitus_list)

        args = {
            'basic_stats': basic_stats_dic,
            'frequency': frequency(ambitus_list),
            'histogram': utils.histogram(ambitus_list, 10, ['Ambitus', 'Pieces'], False, True),
            'distribution_value': distribution_value(ambitus_list),
            'distribution_amount': distribution_amount(ambitus_list),
            'frequency_pie': frequency_pie(ambitus_list),
            'boxplot': utils.boxplot(basic_stats_dic),
        }
        return args
    else:
        return {}
