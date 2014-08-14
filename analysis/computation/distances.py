from analysis.computation import utils
from analysis.computation import intervals


def analysis(compositions):

    # intervals
    midi_intervals = utils.get_music_data_attrib(compositions, 'intervals_midi', 'extend')
    nested_midi_intervals = utils.get_music_data_attrib(compositions, 'intervals_midi', 'append')


    if midi_intervals and nested_midi_intervals:
        # intervals
        categorized_midi_intervals = list(map(intervals.get_category, midi_intervals))
        categorized_nested_midi_intervals = [list(map(intervals.get_category, s)) for s in nested_midi_intervals]
        coll_freq_dic = utils.special_counter(categorized_midi_intervals, True)

        args = {
            'intervals_distance': utils.frequency_distance_scatter(compositions, categorized_nested_midi_intervals, coll_freq_dic),
        }
    else:
        args = {}

    return args
