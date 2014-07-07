from analysis.computation import utils


def frequency_scatter(durations):
    counted = utils.special_counter(durations, True)
    seq = sorted(map(list, counted.items()))
    seq.insert(0, ['Duration quarter', 'Amount'])
    return seq


def frequency_pie(durations):
    r = utils.aux_pie_chart(utils.special_counter(durations))
    r.insert(0, ['Duration quarter', 'Amount'])
    return r


def analysis(compositions):
    durations = utils.get_music_data_attrib(compositions, 'durations')
    total_duration = utils.get_single_music_data_attrib(compositions, 'total_duration')
    basic_stats = utils.aux_basic_stats(durations, 'Durations number', False)

    if durations and total_duration:
        args = {
            'basic_stats': basic_stats,
            'frequency_scatter': frequency_scatter(durations),
            'frequency_pie': frequency_pie(durations),
            'histogram': utils.histogram(durations, 10, ['Durations', 'Ocurrences'], False, True),
            'distribution_amount': utils.distribution(durations, basic_stats, True),
        }
    else:
        args = {}

    return args
