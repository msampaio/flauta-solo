import numpy
from analysis.computation import utils

def analysis(composition):
    midi_notes = composition.music_data.notes
    durations_seq = composition.music_data.durations

    notes_scatter = list(map(list, enumerate(midi_notes)))
    notes_scatter.insert(0, ['Time point', 'Midi note'])
    notes_scatter_array = numpy.array(notes_scatter[1:])

    min_pts = 10
    if notes_scatter_array.shape[0] < 10:
        min_pts = 0

    notes_reachability_plot = utils.make_reachability_plot(notes_scatter_array, min_pts)

    durations_scatter = list(map(list, enumerate(durations_seq)))
    durations_scatter.insert(0, ['Time point', 'Duration note'])
    durations_scatter_array = numpy.array(durations_scatter[1:])

    min_pts = 10
    if notes_scatter_array.shape[0] < 10:
        min_pts = 0

    durations_reachability_plot = utils.make_reachability_plot(durations_scatter_array, min_pts)

    notes_cluster = utils.make_optics_plot_data(notes_scatter_array, min_pts)
    durations_cluster = utils.make_optics_plot_data(durations_scatter_array, min_pts)

    if midi_notes and durations_seq:
        args = {
            'composition': composition,
            'notes_scatter': notes_scatter,
            'durations_scatter': durations_scatter,
            'notes_reachability_plot': notes_reachability_plot,
            'durations_reachability_plot': durations_reachability_plot,
            'notes_cluster': notes_cluster,
            'durations_cluster': durations_cluster,
        }
    else:
        args = {}

    return args
