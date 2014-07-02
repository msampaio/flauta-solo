from collections import Counter
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


def analysis(compositions):
    contour_list = utils.get_single_music_data_attrib(compositions, 'contour')

    if contour_list:
        args = {
            'basic_stats': utils.aux_basic_stats(contour_list, 'Contour number', True),
            'frequency_pie_2': frequency_pie(contour_list, 2),
            'frequency_pie_3': frequency_pie(contour_list, 3),
            'frequency_pie_4': frequency_pie(contour_list, 4),
        }
    else:
        args = {}
        
    return args