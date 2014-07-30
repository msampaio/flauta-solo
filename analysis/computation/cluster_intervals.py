import numpy
from analysis.computation import utils

def get_interval_frequency(compositions, normalize=False):
    def aux(composition):
        intervals = composition.music_data.intervals_midi
        counted = utils.special_counter(intervals, True)
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


def interval_reachability(array, min_pts):
    reachability_plot = utils.make_reachability_plot_data(array, min_pts)

    reachability_plot.insert(0, ['Piece', 'Reachability value'])
    return reachability_plot


def make_clusters(compositions, array, min_pts):
    leaves = utils.get_optics_data(array, min_pts)[-1]

    clusters = []
    if not leaves: return clusters
    for leave_number, leave in enumerate(leaves):
        l_dic = {}
        l_dic['number'] = 'G' + str(leave_number + 1)
        l_dic['size'] = len(leave.order)
        songs = []
        for n in leave.order:
            composition = compositions[int(n)]
            title = composition.title
            code = composition.music_data.score.code
            songs.append({'title': title, 'code': code, 'first': False})

        songs[0]['first'] = True
        l_dic['songs'] = songs

        clusters.append(l_dic)

    return clusters


def analysis(compositions):
    array = get_interval_frequency(compositions)

    min_pts = 10
    if array.shape[0] < 10:
        min_pts = 0

    reachability_plot = interval_reachability(array, min_pts)
    cluster_table = make_clusters(compositions, array, min_pts)

    if array.any():
        args = {
            'reachability_plot': reachability_plot,
            'cluster_table': cluster_table,
        }
    else:
        args = {}

    return args