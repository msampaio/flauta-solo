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
    piece_durations = utils.get_single_music_data_attrib(compositions, 'total_duration')
    basic_stats_duration = utils.aux_basic_stats(durations, 'Durations number', False)
    basic_stats_piece_duration = utils.aux_basic_stats(piece_durations, 'Durations number', False)

    if durations and piece_durations:
        args = {
            'basic_stats_duration': basic_stats_duration,
            'note_frequency_scatter': frequency_scatter(durations),
            'note_frequency_pie': frequency_pie(durations),
            'note_histogram': utils.histogram(durations, 10, ['Durations', 'Ocurrences'], False, True),
            'note_distribution_amount': utils.distribution(durations, basic_stats_duration, True),
            'basic_stats_piece_duration': basic_stats_piece_duration,
            'piece_frequency_scatter': frequency_scatter(piece_durations),
            'piece_frequency_pie': frequency_pie(piece_durations),
            'piece_histogram': utils.histogram(piece_durations, 10, ['Durations', 'Ocurrences'], False, True),
            'piece_distribution_amount': utils.distribution(piece_durations, basic_stats_duration, True),
        }
    else:
        args = {}

    return args
