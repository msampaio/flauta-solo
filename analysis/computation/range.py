from collections import Counter
import numpy


def range_analysis(compositions):
    range_list = [c.music_data.ambitus for c in compositions]
    frequency = Counter(range_list)
    values = [{"label": k, "value": v} for k, v in sorted(frequency.items())]

    return [{"key": "Cumulative Return", "values": values}]

    # range_statistics = {}
    # range_statistics['Min'] = min(range_list)
    # range_statistics['Max'] = max(range_list)
    # range_statistics['Mean'] = numpy.mean(range_list)
    # range_statistics['Standard deviation'] = numpy.std(range_list)
    #
    # return range_statistics
