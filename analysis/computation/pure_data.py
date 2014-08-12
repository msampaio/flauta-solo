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


def print_pretty_pd(dic):
    r = []
    for key, value in dic.items():
        if type(value) == int:
            seq = str(value)
        else:
            seq = ' '.join([str(v) for v in value])
        r.append('{}, {};\n'.format(str(key), seq))
    return r


def get_all_attributes(music_data):
    attribs = ['durations', 'intervals_midi', 'contour']

    r = []
    for attrib in attribs:
        data = print_pretty_list_map(*get_list_and_map_attr(music_data, attrib))
        data.insert(0, attrib)
        r.append(data)
    return r


def split_sequence(seq, order=2):
    return list(zip(*[seq[o:] for o in range(order)]))


def split_nested_sequences(nested_seq, order=2):
    spl = []
    for seq in nested_seq:
        spl.extend(split_sequence(seq, order))

    return spl


def make_markov_chain(split_seq):

    def update_dic(seq, chain_map, aux_map, map_index):
        if seq not in aux_map.keys():
            seq_index = map_index
            aux_map[seq] = seq_index
            chain_map[seq_index] = seq
            map_index += 1
        else:
            seq_index = aux_map[seq]
        return seq_index, map_index

    chain_dic = {}
    chain_map = {}
    aux_map = {}
    map_ind = 0

    for seq in split_seq:
        input_seq = tuple(seq[:-1])
        output_seq = tuple([seq[-1]])

        input_ind, map_ind = update_dic(input_seq, chain_map, aux_map, map_ind)
        output_ind, map_ind = update_dic(output_seq, chain_map, aux_map, map_ind)

        if input_ind not in chain_dic:
            chain_dic[input_ind] = []

        chain_dic[input_ind].append(output_ind)

    return chain_dic, chain_map


def pd_dic_pretty_print(key, value):
    if type(value) == list or type(value) == tuple:
        value = ' '.join(map(str, value))
    else:
        value = str(value)
    return '{}, {};'.format(key, value)


def markov_print(chain_dic, chain_map):
    chain_str = '\n'.join((pd_dic_pretty_print(k, v) for k, v in chain_dic.items()))
    map_str = '\n'.join((pd_dic_pretty_print(k, v) for k, v in chain_map.items()))
    return chain_str, map_str


def markov_chain_contour(contour_list, order=1, print_pd=False):
    def split_and_count_contour(cseg, order):
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


    output_csegs = []
    for cseg in contour_list:
        output_csegs.extend(split_and_count_contour(cseg, order))

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
    contour_list = utils.get_music_data_attrib(compositions, 'contour', 'append')

    if contour_list:
        cseg_map, cseg_chain = markov_chain_contour(contour_list, order, True)

        args = {
            'cseg_map': cseg_map,
            'cseg_chain': cseg_chain,
        }
    else:
        args = {}

    return args


def make_general_chain(compositions, attrib, order=1):
    nested_seq = utils.get_music_data_attrib(compositions, attrib, 'append')
    if nested_seq:
        spl = split_nested_sequences(nested_seq, order)
        chain_str, map_str = markov_print(*make_markov_chain(spl))

        args = {
            'chain': chain_str,
            'map': map_str,
        }
    else:
        args = {}

    return args


def save_chain(contour_list, order=1):

    def save(string, basename):
        filename = os.path.join('/tmp/', '{}-{}.coll'.format(basename, order))
        with open(filename, 'w') as f:
            f.write(''.join(string))

    cseg_map, cseg_chain = markov_chain_contour(contour_list, order, True)

    save(cseg_map, 'cseg_map')
    save(cseg_chain, 'cseg_chain')
