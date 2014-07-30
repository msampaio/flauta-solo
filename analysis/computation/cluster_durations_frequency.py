import numpy
from analysis.computation import utils


def get_duration_frequency(compositions, normalize=False):
    def aux(composition):
        durations = composition.music_data.durations
        counted = utils.special_counter(durations, True)
        seq = []
        for i in range(-48, 49):
            if i in counted:
                seq.append(counted[i])
            else:
                seq.append(0)
        return seq

    array = numpy.array([aux(composition) for composition in compositions])

    if normalize:
        for i in range(-48, 49):
            array = utils.normalize_array(array, i)

    return array


def duration_reachability(array, min_pts):
    reachability_plot = utils._make_reachability_plot_data(array, min_pts)

    reachability_plot.insert(0, ['Piece', 'Reachability value'])
    return reachability_plot


def analysis(compositions):
    array = get_duration_frequency(compositions)

    min_pts = 10
    if array.shape[0] < 10:
        min_pts = 0

    reachability_plot = utils.make_reachability_plot(array, min_pts)
    cluster_table = utils.make_clusters(compositions, array, min_pts)

    if array.any():
        args = {
            'reachability_plot': reachability_plot,
            'cluster_table': cluster_table,
        }
    else:
        args = {}

    return args