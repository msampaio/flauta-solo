from analysis.computation import utils
from analysis.computation import contour
import numpy
from collections import Counter
import itertools

def get_contour_frequency(contour_list, size, normalize=False):

    def make_csegs(size):
        base = list(range(size)) * size
        permutations = map(list, itertools.permutations(base, size))
        csegs_set = set([tuple(contour.translate(cseg)) for cseg in permutations])
        return sorted(list(csegs_set))

    def aux(composition_contour, csegs_map, size):
        splitted = contour.split_and_translate(composition_contour, size)
        csegs = [csegs_map.index(tuple(c)) for c in splitted]
        counted = Counter(csegs)
        seq = []
        for i in range(len(csegs_map)):
            if i in counted:
                seq.append(counted[i])
            else:
                seq.append(0)
        return seq

    csegs_map = make_csegs(size)

    array = numpy.array([aux(comp_cseg, csegs_map, size) for comp_cseg in contour_list])

    if normalize:
        for i in range(len(csegs_map)):
            array = utils.normalize_array(array, i)

    return array


def analysis(compositions, size=2):

    contour_list = utils.get_single_music_data_attrib(compositions, 'contour')
    array = get_contour_frequency(contour_list, size, True)

    min_pts = 10
    if array.shape[0] < 10:
        min_pts = 0

    reachability_plot = utils.make_reachability_plot(array, min_pts)
    cluster_table = utils.make_clusters(compositions, array, min_pts)

    if array.any():
        args = {
            'reachability_plot': reachability_plot,
            'cluster_table': cluster_table,
            'size': size,
        }
    else:
        args = {}

    return args