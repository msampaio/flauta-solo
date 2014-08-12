from analysis.computation import utils
import numpy
from scipy.spatial import distance


def get_category(interval):
    interval_class = interval % 12
    if interval_class > 6:
        interval_class = 12 - interval_class
    return range(7).index(interval_class)


def frequency_scatter(intervals):
    counted = utils.special_counter(intervals, True)
    seq = sorted(map(list, counted.items()))
    seq.insert(0, ['Interval', 'Amount'])
    return seq


def frequency_pie(intervals):
    r = utils.aux_pie_chart(utils.special_counter(intervals))
    r.insert(0, ['Interval', 'Amount'])
    return r


def chromatic_leaps_frequency_pie(chromatic_intervals):
    counted = utils.special_counter(chromatic_intervals, False)
    for i in ['P1', 'M2', 'm2', 'M3', 'm3']:
        del counted[i]
    r = utils.aux_pie_chart(counted)
    r.insert(0, ['Interval', 'Amount'])
    return r


def get_pitch_class_frequency(intervals):
    categorized = list(map(get_category, intervals))
    counted = utils.special_counter(categorized, True)
    for i in range(7):
        if i not in counted.keys():
            counted[i] = 0
    return list(map(lambda x: x[1], sorted(counted.items())))


def get_pitch_class_distance(intervals, vector):
    x = get_pitch_class_frequency(intervals)
    array_vector = numpy.array(vector)
    array_x = numpy.array(x)
    return distance.euclidean(array_vector, array_x)


def get_all_pieces_pc_distance(intervals, vector):
    return [get_pitch_class_distance(i, vector) for i in intervals]


def get_pc_distance_scatter(seq, compositions):
    zipped = zip(compositions, seq)
    r = [[c.music_data.score.code, s] for c, s in zipped]
    r.insert(0, ['Composition', 'Value'])
    return r

def analysis(compositions):
    midi_intervals = utils.get_music_data_attrib(compositions, 'intervals_midi', 'extend')
    nested_midi_intervals = utils.get_music_data_attrib(compositions, 'intervals_midi', 'append')
    simple_intervals = [abs(x) % 12 for x in midi_intervals]
    chromatic_intervals = utils.get_music_data_attrib(compositions, 'intervals')
    basic_stats = utils.aux_basic_stats(midi_intervals, 'Intervals number', False)
    pitch_class_frequency_vector = get_pitch_class_frequency(midi_intervals)
    pitch_class_distances = get_all_pieces_pc_distance(nested_midi_intervals, pitch_class_frequency_vector)

    if midi_intervals and chromatic_intervals:
        args = {
            'frequency_scatter': frequency_scatter(midi_intervals),
            'frequency_basic_scatter': frequency_scatter(simple_intervals),
            'basic_stats': basic_stats,
            'frequency_pie': frequency_pie(midi_intervals),
            'chromatic_frequency_pie': frequency_pie(chromatic_intervals),
            'chromatic_leaps_frequency_pie': chromatic_leaps_frequency_pie(chromatic_intervals),
            'histogram': utils.histogram(midi_intervals, 10, ['Intervals', 'Ocurrences'], False, True),
            'distribution_amount': utils.distribution(midi_intervals, basic_stats, True),
            'category_frequency_pie': frequency_pie(list(map(get_category, midi_intervals))),
            'pitch_class_distance': get_pc_distance_scatter(pitch_class_distances, compositions),
        }
    else:
        args = {}

    return args
