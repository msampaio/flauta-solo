from collections import Counter
import numpy

def get_ambitus_list(compositions):
    return [c.music_data.ambitus for c in compositions]

def range_histogram(range_list):
    frequency = Counter(range_list)
    values = [{"label": k, "value": v} for k, v in sorted(frequency.items())]
    return [{"key": "Cumulative Return", "values": values}]

def range_basics(range_list):
    data = {}
    data['Min'] = min(range_list)
    data['Max'] = max(range_list)
    data['Mean'] = numpy.mean(range_list)
    data['Standard deviation'] = numpy.std(range_list)
    return data

def range_analysis(compositions):
    range_list = get_ambitus_list(compositions)

    data = {}
    data['histogram'] = range_histogram(range_list)
    data['statistics'] = range_basics(range_list)

    return data
