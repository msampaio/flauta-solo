from collections import Counter
import itertools
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


def markov_chain(contour_list, size=2):

    def split_and_count(cseg):
        without_repetition = remove_adjacent_repetition(cseg)
        splitted = map(tuple, split_and_translate(without_repetition, size + 1))
        return Counter(splitted)

    output_csegs_counter = Counter()

    for cseg in contour_list:
        output_csegs_counter.update(split_and_count(cseg))

    output_csegs = output_csegs_counter.keys()
    total = sum(output_csegs_counter.values())

    translation_dic = {}
    for output_cseg in output_csegs:
        translated_input_cseg = tuple(translate(list(output_cseg[:-1])))
        if translated_input_cseg not in translation_dic:
            translation_dic[translated_input_cseg] = []
        translation_dic[translated_input_cseg].append(output_cseg)

    input_csegs = sorted(set([tuple(translate(list(k[:-1]))) for k in output_csegs]))

    chain = []

    for output_cseg in sorted(output_csegs):
        row = [output_cseg]
        for input_cseg in input_csegs:
            translation_csegs = translation_dic[input_cseg]
            if output_cseg in output_csegs_counter and output_cseg in translation_csegs:
                value = output_csegs_counter[output_cseg] / total
            else:
                value = 0
            row.append(value)
        chain.append(row)
    input_csegs.insert(0, None)
    chain.insert(0, input_csegs)

    return chain


def contour_adjacency_series(contour_list):
    pairs = zip(contour_list, contour_list[1:])
    return list(map(utils.comparison, pairs))


def count_movements(contour_list):
    return Counter(contour_adjacency_series(contour_list))


def print_cseg(cseg):
    return "< {0} >".format(" ".join(str(p) for p in cseg))


def remove_adjacent_repetition(cseg):
    return [point for point, _ in itertools.groupby(cseg)]


def single_repetition_index(cseg):
    without_repetition = remove_adjacent_repetition(cseg)
    return 1 - (max(without_repetition) / float(len(without_repetition)))


def repetition_index(contour_list):
    return [single_repetition_index(cseg) for cseg in contour_list]


def repetition_scatter(contour_list):
    repetition = repetition_index(contour_list)
    counted = utils.special_counter(repetition, True)
    seq = sorted(map(list, counted.items()))
    seq.insert(0, ['Proportion', 'Amount'])
    return seq


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
        basic_stats = utils.aux_basic_stats(contour_list, 'Contour number', True)
        repetition_scatter_data = repetition_scatter(contour_list)
        repetition_seq = repetition_index(contour_list)
        repetition_stats = utils.aux_basic_stats(repetition_seq, 'Pieces Number', False)
        dist_value = utils.distribution(repetition_seq, repetition_stats, False)
        dist_amount = utils.distribution(repetition_seq, repetition_stats, True)

        args = {
            'basic_stats': basic_stats,
            'repetition_stats': repetition_stats,
            'frequency_pie_2': frequency_pie(contour_list, 2),
            'frequency_pie_3': frequency_pie(contour_list, 3),
            'frequency_pie_4': frequency_pie(contour_list, 4),
            'repetition_scatter': repetition_scatter_data,
            'distribution_value': dist_value,
            'distribution_amount': dist_amount,
            'histogram': utils.histogram(repetition_seq, 10, ['Index', 'Pieces'], False, True),
        }
    else:
        args = {}
        
    return args