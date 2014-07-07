import numpy
from analysis.computation import utils


def get_duration_ambitus(compositions, normalize=True, labelize=False):
    pairs = [(c.music_data.total_duration, c.music_data.ambitus) for c in compositions]
    if normalize:
        arr = numpy.array(pairs)
        for i in 0, 1:
            arr = utils.normalize_array(arr, i)
        pairs = arr.tolist()

    if labelize:
        seq = []
        for i in range(len(pairs)):
            imslp = compositions[i].collection.imslp_id
            row = []
            x, y = pairs[i]
            row.append({'v': x, 'f':'{}. {}'.format(imslp, x)})
            row.append(y)

            seq.append(row)

        pairs = seq

    pairs.insert(0, ['', 'Piece'])
    return pairs


def duration_ambitus_cluster(duration_ambitus):
    array = numpy.array(duration_ambitus[1:])
    return utils.make_optics_plot_data(array)


def analysis(compositions):
    duration_ambitus_label = get_duration_ambitus(compositions, True, True)
    duration_ambitus = get_duration_ambitus(compositions, True, False)
    cluster = duration_ambitus_cluster(duration_ambitus)

    if duration_ambitus:
        args = {
            'duration_ambitus_label': duration_ambitus_label,
            'duration_ambitus': duration_ambitus,
            'cluster': cluster,
        }
    else:
        args = {}

    return args