import numpy

def range_analysis(compositions):
    range_list = [c.music_data.ambitus for c in compositions]

    range_statistics = {}
    range_statistics['Min'] = min(range_list)
    range_statistics['Max'] = max(range_list)
    range_statistics['Mean'] = numpy.mean(range_list)
    range_statistics['Standard deviation'] = numpy.std(range_list)

    return range_statistics
