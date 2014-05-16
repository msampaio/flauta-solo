from collections import Counter
import numpy


def gaussian(x, mu, sig):
    return numpy.exp(-numpy.power(x - mu, 2.) / 2 * numpy.power(sig, 2.))


def get_ambitus_list(compositions):
    return [c.music_data.ambitus for c in compositions]


def histogram(range_list, listOutput=True):
    bins = 10
    histogram = numpy.histogram(range_list, bins)
    if listOutput:
        return [[histogram[1][i], histogram[0][i]] for i in range(bins)]

    values = [{"label": histogram[1][i], "value": histogram[0][i]} for i in range(bins)]

    return [{"key": "Cumulative Return", "values": values}]

def frequency(range_list, listOutput=True):
    frequency = Counter(range_list)

    if listOutput:
        return [[k, v] for k, v in sorted(frequency.items())]

    values = [{"label": k, "value": v} for k, v in sorted(frequency.items())]
    return [{"key": "Cumulative Return", "values": values}]


def distribution(basic_stats_dic):
    print(basic_stats_dic['Max'])
    x = numpy.linspace(-3, 3, basic_stats_dic['Max'])
    mu = -1
    sig = 1
    curve = enumerate(gaussian(x, mu, sig))
    return [[x, y] for x, y in curve]


def basic_stats(range_list):
    data = {'Min': min(range_list),
            'Max': max(range_list),
            'Mean': numpy.mean(range_list),
            'Median': numpy.median(range_list),
            'Quartile 1': numpy.percentile(range_list, 25),
            'Quartile 3': numpy.percentile(range_list, 75),
            'Standard deviation': numpy.std(range_list)
    }
    return data


def analysis(compositions):

    range_list = get_ambitus_list(compositions)
    basic_stats_dic = basic_stats(range_list)

    args = {
        'basic_stats': basic_stats_dic,
        'frequency': frequency(range_list, False),
        'histogram': histogram(range_list, False),
        'histogram_list': histogram(range_list, True),
        'distribution': distribution(basic_stats_dic),
    }

    return args