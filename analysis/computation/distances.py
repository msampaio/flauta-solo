from analysis.computation import utils
from analysis.computation import intervals
from analysis.computation import contour


def analysis(compositions):

    # intervals
    midi_intervals = utils.get_music_data_attrib(compositions, 'intervals_midi', 'extend')
    nested_midi_intervals = utils.get_music_data_attrib(compositions, 'intervals_midi', 'append')

    # durations
    dur = utils.get_music_data_attrib(compositions, 'durations', 'extend')
    nested_dur = utils.get_music_data_attrib(compositions, 'durations', 'append')

    # contour
    contour_list = utils.get_music_data_attrib(compositions, 'contour', 'append')

    tests = [midi_intervals,
             nested_midi_intervals,
             dur,
             nested_dur,
             contour_list]

    if all(tests):
        # intervals
        cat_intervals = list(map(intervals.get_category, midi_intervals))
        cat_nested_intervals = [list(map(intervals.get_category, s)) for s in nested_midi_intervals]
        coll_freq_intervals = utils.special_counter(cat_intervals, True)

        # durations
        coll_freq_durations = utils.special_counter(dur, True)

        # contour
        freq_dist_args = {}
        for size in range(2, 5):
            split_seq = list(map(tuple, contour.split_and_translate_nested(contour_list, size)))
            split_seq_nested = [list(map(tuple, contour.split_and_translate(c, size))) for c in contour_list]
            coll_freq_dic = contour.get_frequency(split_seq, size)
            freq_dist_sc = utils.frequency_distance_scatter(compositions, split_seq_nested, coll_freq_dic, True)
            freq_dist_args.update({'contour_{}_distance'.format(size): freq_dist_sc})

        freq_data = [
            ['Duration', nested_dur, coll_freq_durations],
            ['Interval', cat_nested_intervals, coll_freq_intervals],
        ]

        args = {
            'intervals_distance': utils.frequency_distance_scatter(compositions, cat_nested_intervals, coll_freq_intervals, True),
            'durations_distance': utils.frequency_distance_scatter(compositions, nested_dur, coll_freq_durations, True),
            'id_distance': utils.frequency_distance_scatter_group(compositions, freq_data, True),
        }
        args.update(freq_dist_args)
    else:
        args = {}

    return args
