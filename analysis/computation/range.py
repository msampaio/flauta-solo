import numpy
import json

def range_analysis(compositions):
    range_list = [c.music_data.ambitus for c in compositions]

    # ambitus frequency analysis - for histogram
    frequency = {}
    for v in range_list:
        if(v not in frequency):
            frequency[v] = 0
        frequency[v] +=1

    values = []
    for k, v in sorted(frequency.items()):
        values.append({"label": k, "value": v})

    r = [{"key": "Cumulative Return",
          "values": values}]

    return json.dumps(r)
    # range_statistics = {}
    # range_statistics['Min'] = min(range_list)
    # range_statistics['Max'] = max(range_list)
    # range_statistics['Mean'] = numpy.mean(range_list)
    # range_statistics['Standard deviation'] = numpy.std(range_list)
    #
    # return range_statistics
