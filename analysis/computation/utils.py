from collections import Counter
from django.utils.datastructures import SortedDict
import numpy


def flatten(seq):
    return [el for l in seq for el in l]


def normal_distribution(x, mu, sigma):
    first = 1 / (sigma * numpy.sqrt(2 * numpy.pi))
    second = -1/2 * (((x - mu) / sigma) ** 2)

    return first * (numpy.e ** second)


def normalization(value, mu, sigma):
    return (value - mu) / sigma


def normalize_array(array, column=0):
    c_array = array[:,column]
    mean = c_array.mean()
    std = c_array.std()
    if std != 0:
        array[:, column] = (array[:, column] - mean) / std

    return array


def special_counter(seq, proportional=False, normalized=False):
    counted = Counter(seq)
    total = len(seq)

    if proportional:
        for key in counted.keys():
            counted[key] /= total

    if normalized:
        values = counted.values()
        mean = numpy.mean(values)
        std_dev = numpy.std(values)

        for key in counted.keys():
            counted[key] = normalization(counted[key], mean, std_dev)

    return counted


def aux_basic_stats(data_seq, string, flat=False):
    if flat:
        data_seq = flatten(data_seq)

    freq = Counter(data_seq)
    freq_values = list(freq.values())

    data = SortedDict([
        ('Value Min', min(data_seq)),
        ('Value Max', max(data_seq)),
        ('Value Mean', numpy.mean(data_seq)),
        ('Value Median', numpy.median(data_seq)),
        ('Value Standard deviation', numpy.std(data_seq)),
        ('Value Quartile 1', numpy.percentile(data_seq, 25)),
        ('Value Quartile 3', numpy.percentile(data_seq, 75)),
        ('Amount with most common', max(freq.values())),
        ('Amount with less common', min(freq.values())),
        ('Amount Mean', numpy.mean(freq_values)),
        ('Amount Median', numpy.median(freq_values)),
        ('Amount Standard deviation', numpy.std(freq_values)),
        ('Amount Quartile 1', numpy.percentile(freq_values, 25)),
        ('Amount Quartile 3', numpy.percentile(freq_values, 75)),
        (string, len(data_seq)),
    ])
    return data


# chart functions #

def histogram(int_sequence, bins, label, swap=True, string=True):
    hist_data = numpy.histogram(int_sequence, bins)
    r = [label]

    for i in range(bins):
        pair = [hist_data[1][i], hist_data[0][i]]
        if swap:
            pair.reverse()
        if string:
            pair[0] = str(pair[0])
        r.append(pair)

    return r


def boxplot(basic_data):
    minimum = basic_data['Value Min']
    maximum = basic_data['Value Max']
    quartile_1 = basic_data['Value Quartile 1']
    quartile_3 = basic_data['Value Quartile 3']

    return ['', maximum, quartile_3, quartile_1, minimum]


def aux_pie_chart(counted_dic):
    return sorted(([str(k), v] for k, v in counted_dic.items()), key = lambda x: x[1], reverse=True)


def distribution(data_seq, basic_stats, amount=False):

    if amount:
        label = 'Amount'
        data_seq = Counter(data_seq).values()
    else:
        label = 'Value'

    mu = basic_stats[label + ' Mean']
    sigma = basic_stats[label + ' Standard deviation']

    label = label + ' distribution'

    normalized = [normalization(value, mu, sigma) for value in data_seq]

    bins = 10
    histogram = numpy.histogram(normalized, bins)
    total = histogram[0].sum()

    r = [['Sigma', 'Histogram', label, 'Normal distribution']]

    values = zip(histogram[0], histogram[1])

    for v, k in values:
        r.append([k, v / total, v/total, normal_distribution(k, 0, 1)])

    return r


# music functions #

def get_single_music_data_attrib(compositions, attrib):
    return [getattr(composition.music_data, attrib) for composition in compositions]


def get_music_data_attrib(compositions, attrib):
    seq = []
    for composition in compositions:
        seq.extend(getattr(composition.music_data, attrib))
    return seq

def comparison(pair):
    a, b = pair
    return (a > b) - (a < b)