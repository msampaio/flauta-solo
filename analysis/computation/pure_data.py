import os
from analysis.computation import contour
from analysis.computation import utils


def get_list_and_map_attr(music_data, attrib):
    seq = getattr(music_data, attrib)

    seq_map = sorted(set(seq))
    seq_pd = [seq_map.index(s) for s in seq]
    return seq_map, seq_pd


def print_pretty_list_map(seq_map, seq):
    pretty_map = '\n'.join(['{}, {};'.format(x, y) for x, y in enumerate(seq_map)])
    pretty_seq = ' '.join(map(str, seq)) + ';'
    return [pretty_map, pretty_seq]


def get_all_attributes(music_data):
    attribs = ['durations', 'intervals_midi', 'contour']

    r = []
    for attrib in attribs:
        data = print_pretty_list_map(*get_list_and_map_attr(music_data, attrib))
        data.insert(0, attrib)
        r.append(data)
    return r


def markov_chain(contour_list, order=1, print_pd=False):

    def split_and_count(cseg):
        without_repetition = contour.remove_adjacent_repetition(cseg)
        return contour.split_and_translate(without_repetition, order + 2)

    def check_dic(cseg_map_int, cseg_map_cseg, cseg, n):
        if cseg not in cseg_map_cseg.keys():
            cseg_map_cseg[cseg] = n
            cseg_map_int[n] = cseg
            ind = n
            n += 1
        else:
            ind = cseg_map_cseg[cseg]
        return ind, n

    def print_pretty_pd(dic):
        r = []
        for key, value in dic.items():
            if type(value) == int:
                seq = str(value)
            else:
                seq = ' '.join([str(v) for v in value])
            r.append('{}, {};\n'.format(str(key), seq))
        return r

    output_csegs = []
    for cseg in contour_list:
        output_csegs.extend(split_and_count(cseg))

    cseg_map_int = {}
    cseg_map_cseg = {}
    chain = {}
    n = 0

    for cseg in output_csegs:
        input_cseg = tuple(contour.translate(cseg[:-1]))
        output_cseg = tuple(cseg)
        input_n, n = check_dic(cseg_map_int, cseg_map_cseg, input_cseg, n)
        output_n, n = check_dic(cseg_map_int, cseg_map_cseg, output_cseg, n)

        if input_n not in chain.keys():
            chain[input_n] = []
        chain[input_n].append(output_n)

    if print_pd:
        cseg_map_int = print_pretty_pd(cseg_map_int)
        chain = print_pretty_pd(chain)

    return cseg_map_int, chain


def generate_contour_chain(compositions, order=1):
    contour_list = utils.get_single_music_data_attrib(compositions, 'contour')

    if contour_list:
        cseg_map, cseg_chain = markov_chain(contour_list, order, True)

        args = {
            'cseg_map': cseg_map,
            'cseg_chain': cseg_chain,
        }
    else:
        args = {}

    return args


def save_chain(contour_list, order=1):

    def save(string, basename):
        filename = os.path.join('/tmp/', '{}-{}.coll'.format(basename, order))
        with open(filename, 'w') as f:
            f.write(''.join(string))

    cseg_map, cseg_chain = markov_chain(contour_list, order, True)

    save(cseg_map, 'cseg_map')
    save(cseg_chain, 'cseg_chain')
