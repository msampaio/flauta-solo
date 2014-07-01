from collections import Counter
from django.utils.datastructures import SortedDict
import numpy
from analysis.computation import utils

# contour operations #

def translate(cseg):

    transition = {}
    for translated, original in enumerate(sorted(set(cseg))):
        transition[original] = translated

    for i in range(len(cseg)):
        cseg[i] = transition[cseg[i]]

    return cseg


def split_and_translate(cseg, size=2):

    def aux(cseg, i, size):
        return translate(cseg[i:i + size])

    return [aux(cseg, i, size) for i in range(len(cseg) - size)]


def contour_adjacency_series(contour_list):
    pairs = zip(contour_list, contour_list[1:])
    return list(map(utils.comparison, pairs))


def count_movements(contour_list):
    return Counter(contour_adjacency_series(contour_list))


def print_cseg(cseg):
    return "< {0} >".format(" ".join(str(p) for p in cseg))


def frequency_pie(contour_list, size=2):
    splitted = []
    for cseg in contour_list:
        splitted.extend(split_and_translate(cseg, size))

    counted = Counter(map(tuple, splitted))
    r = []
    for k, v in sorted(counted.items(), key=lambda x: x[1], reverse=True):
        r.append([print_cseg(k), v])
    r.insert(0, ['Contour', 'Amount'])
    return r


def count_contour_subseq(cseg, n):
    slices = split_and_translate(cseg, n)
    return Counter(map(tuple, slices))


def basic_stats(contour_list):
    contour_list = utils.flatten(contour_list)
    freq = Counter(contour_list)
    freq_values = list(freq.values())

    data = SortedDict([
            ('Value Min', min(contour_list)),
            ('Value Max', max(contour_list)),
            ('Value Mean', numpy.mean(contour_list)),
            ('Value Median', numpy.median(contour_list)),
            ('Value Standard deviation', numpy.std(contour_list)),
            ('Value Quartile 1', numpy.percentile(contour_list, 25)),
            ('Value Quartile 3', numpy.percentile(contour_list, 75)),
            ('Amount with most common', max(freq.values())),
            ('Amount with less common', min(freq.values())),
            ('Amount Mean', numpy.mean(freq_values)),
            ('Amount Median', numpy.median(freq_values)),
            ('Amount Standard deviation', numpy.std(freq_values)),
            ('Amount Quartile 1', numpy.percentile(freq_values, 25)),
            ('Amount Quartile 3', numpy.percentile(freq_values, 75)),
            ('Contour number', len(contour_list)),
    ])
    return data


def analysis(compositions):
    contour_list = utils.get_single_music_data_attrib(compositions, 'contour')
    args = {
        'basic_stats': basic_stats(contour_list),
        'frequency_pie_2': frequency_pie(contour_list, 2),
        'frequency_pie_3': frequency_pie(contour_list, 3),
        'frequency_pie_4': frequency_pie(contour_list, 4),
    }

    return args