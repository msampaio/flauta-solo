from collections import Counter
import numpy


def get_ambitus_list(compositions):
    return [c.music_data.ambitus for c in compositions]


def histogram(range_list):
    bins = 10
    histogram = numpy.histogram(range_list, bins)
    r = [['Range', 'Pieces']]
    for i in range(bins):
        r.append([str(histogram[1][i]), histogram[0][i]])
    return r


def frequency(range_list):
    frequency = Counter(range_list)

    r = [['Range', 'Pieces']]
    for k, v in sorted(frequency.items()):
        r.append([k, v])
    return r


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
        'frequency': frequency(range_list),
        'histogram': histogram(range_list),
    }

    return args