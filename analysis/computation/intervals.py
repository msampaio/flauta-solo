from analysis.computation import utils


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


def frequency_basic_scatter(intervals):
    simple_intervals = [abs(x) % 12 for x in intervals]
    counted = utils.special_counter(simple_intervals, True)
    seq = sorted(map(list, counted.items()))
    seq.insert(0, ['Interval', 'Amount'])
    return seq


def frequency_pie(intervals):
    r = utils.aux_pie_chart(utils.special_counter(intervals))
    r.insert(0, ['Interval', 'Amount'])
    return r


def chromatic_frequency_pie(chromatic_intervals):
    r = utils.aux_pie_chart(utils.special_counter(chromatic_intervals, False))
    r.insert(0, ['Interval', 'Amount'])
    return r


def chromatic_leaps_frequency_pie(chromatic_intervals):
    counted = utils.special_counter(chromatic_intervals, False)
    for i in ['P1', 'M2', 'm2', 'M3', 'm3']:
        del counted[i]
    r = utils.aux_pie_chart(counted)
    r.insert(0, ['Interval', 'Amount'])
    return r


def analysis(compositions):
    midi_intervals = utils.get_music_data_attrib(compositions, 'intervals_midi')
    chromatic_intervals = utils.get_music_data_attrib(compositions, 'intervals')
    basic_stats = utils.aux_basic_stats(midi_intervals, 'Intervals number', False)

    if midi_intervals and chromatic_intervals:
        args = {
            'frequency_scatter': frequency_scatter(midi_intervals),
            'frequency_basic_scatter': frequency_basic_scatter(midi_intervals),
            'basic_stats': basic_stats,
            'frequency_pie': frequency_pie(midi_intervals),
            'chromatic_frequency_pie': chromatic_frequency_pie(chromatic_intervals),
            'chromatic_leaps_frequency_pie': chromatic_leaps_frequency_pie(chromatic_intervals),
            'histogram': utils.histogram(midi_intervals, 10, ['Intervals', 'Ocurrences'], False, True),
            'distribution_amount': utils.distribution(midi_intervals, basic_stats, True),
            'category_frequency_pie': frequency_pie(list(map(get_category, midi_intervals))),
        }
    else:
        args = {}

    return args
