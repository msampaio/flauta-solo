import numpy
from scipy.spatial.distance import squareform, pdist


class DistanceArray(object):
    def __init__(self):
        self.array = None
        self.columns_index = [] # true index
        self.rows_index = [] # true index
        self.columns_size = 0
        self.rows_size = 0

    def __repr__(self):
        return "<Array {} x {}>".format(self.rows_size, self.columns_size)

    def add_column(self, array_1d, ind):
        updated = numpy.column_stack((self.array, array_1d))
        self.columns_index.append(ind)
        self.array = updated
        self.columns_size += 1

    def get_min(self):
        # Create temporary row_index and array.
        # The processed indexes (from column_index) will be removed from them.

        tmp_row_index = self.rows_index
        tmp_array = numpy.delete(self.array, [self.columns_index], 0)

        # FIXME: use deque to become faster
        for ind in self.columns_index:
            if ind in tmp_row_index:
                tmp_row_index.remove(ind)

        min_value = tmp_array.min()
        tmp_min_index = int(numpy.floor(tmp_array.argmin() / self.columns_size))
        min_index = tmp_row_index[tmp_min_index]

        return min_index, min_value

    def pop_column(self, ind):
        false_index = self.columns_index.index(ind)
        column = self.array[:,false_index]
        self.array = numpy.delete(self.array, false_index, 1)
        self.columns_size -= 1
        self.columns_index.remove(ind)
        return column


def _make_distance_array(array):
    m, n = array.shape
    distance_array_obj = DistanceArray()
    distance_array_obj.array = array
    distance_array_obj.columns_index = list(range(n))
    distance_array_obj.rows_index = list(range(m))
    distance_array_obj.columns_size = n
    distance_array_obj.rows_size = m
    return distance_array_obj


def _move_array_to_left(left_array_obj, right_array_obj, current_ind):
    column = right_array_obj.pop_column(current_ind)
    left_array_obj.add_column(column, current_ind)
    return left_array_obj, right_array_obj


def _get_reachability(left_array_obj, right_array_obj):
    min_index, min_value = left_array_obj.get_min()
    _move_array_to_left(left_array_obj, right_array_obj, min_index)
    return min_index, min_value


def single_optics(array, dist_method="euclidean"):

    columns_n = array.shape[0]
    distance_array = squareform(pdist(array, dist_method))
    processed_array = numpy.tile(distance_array, 0)

    processed_obj = _make_distance_array(processed_array)
    next_set_obj = _make_distance_array(distance_array)

    reachability_pairs = numpy.ones(columns_n) * numpy.inf
    processed_order = []

    # first element
    _move_array_to_left(processed_obj, next_set_obj, 0)
    processed_order.append(0)

    # from second element
    walk_ind = 1
    reach_index = 1
    items_to_process = columns_n - 1

    while(items_to_process > 0):
        reachability_pair = _get_reachability(processed_obj, next_set_obj)
        i, v = reachability_pair
        reachability_pairs[reach_index] = v
        processed_order.append(walk_ind)

        walk_ind = i
        items_to_process -= 1
        reach_index += 1

    return reachability_pairs, processed_order
