from analysis.computation import utils
from analysis.computation import cluster_contour
from analysis.computation import cluster_duration_ambitus
from analysis.computation import cluster_durations_frequency
from analysis.computation import cluster_intervals_frequency
import numpy


def analysis(compositions, size=2):
    duration_ambitus = cluster_duration_ambitus.get_duration_ambitus(compositions, True, False)
    contour_list = utils.get_music_data_attrib(compositions, 'contour', 'append')

    a = numpy.array(duration_ambitus[1:])
    b = cluster_contour.get_contour_frequency(contour_list, size, True)
    c = cluster_intervals_frequency.get_interval_frequency(compositions)
    d = cluster_durations_frequency.get_duration_frequency(compositions)

    array = numpy.column_stack((a, b, c, d))

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