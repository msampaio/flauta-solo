from collections import Counter
from analysis.computation import utils


def frequency(ambitus_list):
    freq = Counter(ambitus_list)

    r = [['Ambitus', 'Pieces']]
    for k, v in sorted(freq.items()):
        r.append([k, v])
    return r


def frequency_pie(ambitus_list):
    r = utils.aux_pie_chart(Counter(ambitus_list))
    r.insert(0, ['Ambitus', 'Amount'])
    return r


def analysis(compositions):
    ambitus_list = utils.get_single_music_data_attrib(compositions, 'ambitus')

    if ambitus_list:
        basic_stats = utils.aux_basic_stats(ambitus_list, 'Pieces number', False)
        dist_value = utils.distribution(ambitus_list, basic_stats, False)

        args = {
            'basic_stats': basic_stats,
            'frequency': frequency(ambitus_list),
            'histogram': utils.histogram(ambitus_list, 10, ['Ambitus', 'Pieces'], False, True),
            'distribution_value': dist_value,
            'distribution_amount': utils.distribution(ambitus_list, basic_stats, True),
            'frequency_pie': frequency_pie(ambitus_list),
            'boxplot': utils.boxplot(basic_stats),
        }
        return args
    else:
        return {}
