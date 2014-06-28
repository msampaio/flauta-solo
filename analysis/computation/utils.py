import numpy


def flatten(seq):
    return [el for l in seq for el in l]


def normal_distribution(x, mu, sigma):
    first = 1 / (sigma * numpy.sqrt(2 * numpy.pi))
    second = -1/2 * (((x - mu) / sigma) ** 2)

    return first * (numpy.e ** second)


def normalization(value, mu, sigma):
    return (value - mu) / sigma


def normalize_array(array, column=0):
    c_array = array[:,column]
    mean = c_array.mean()
    std = c_array.std()
    if std != 0:
        array[:, column] = (array[:, column] - mean) / std

    return array


# chart functions #

def histogram(int_sequence, bins, label, swap=True, string=True):
    hist_data = numpy.histogram(int_sequence, bins)
    r = [label]

    for i in range(bins):
        pair = [hist_data[1][i], hist_data[0][i]]
        if swap:
            pair.reverse()
        if string:
            pair[0] = str(pair[0])
        r.append(pair)

    return r


def boxplot(basic_data):
    minimum = basic_data['Min']
    maximum = basic_data['Max']
    quartile_1 = basic_data['Quartile 1']
    quartile_3 = basic_data['Quartile 3']

    return ['', maximum, quartile_3, quartile_1, minimum]


def aux_pie_chart(counted_dic):
    return sorted(([str(k), v] for k, v in counted_dic.items()), key = lambda x: x[1], reverse=True)
