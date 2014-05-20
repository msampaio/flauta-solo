from collections import Counter
import numpy


def gaussian(x, mu, sig):
    return numpy.exp(-numpy.power(x - mu, 2.) / 2 * numpy.power(sig, 2.))


def get_ambitus_list(compositions):
    return [c.music_data.ambitus for c in compositions]


def range_values2(compositions):
    range_list = get_ambitus_list(compositions)
    frequency = Counter(range_list)
    values = [v for (k, v) in sorted(frequency.items())]
    curve = [x for x in gaussian(numpy.linspace(-3, 3, 120), -1, 1)]
    return values, curve


def range_values(range_list):
    frequency = Counter(range_list)
    values = [{"label": k, "value": v} for k, v in sorted(frequency.items())]
    return [{"key": "Cumulative Return", "values": values}]


def range_histogram(range_list):
    bins = 10
    histogram = numpy.histogram(range_list, bins)
    values = [{"label": histogram[1][i], "value": histogram[0][i]} for i in range(bins)]

    return [{"key": "Cumulative Return", "values": values}]


def range_basics(range_list):
    data = {'Min': min(range_list),
            'Max': max(range_list),
            'Mean': numpy.mean(range_list),
            'Median': numpy.median(range_list),
            'Quartile 1': numpy.percentile(range_list, 25),
            'Quartile 3': numpy.percentile(range_list, 75),
            'Standard deviation': numpy.std(range_list)
    }
    return data


def range_analysis(compositions):
    range_list = get_ambitus_list(compositions)

    data = {'values': range_values(range_list),
            'histogram': range_histogram(range_list),
            'statistics': range_basics(range_list)
    }

    return data
