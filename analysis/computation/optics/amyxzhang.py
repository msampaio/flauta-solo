from matplotlib import pyplot as plt
import numpy
from scipy.spatial.distance import squareform, pdist


def optics(array, min_pts, distance_method="euclidean"):
    """Order data and return reachability plot.

    Algorithm based on Ankerst et al and Daszykowski et al.
    Available at http://www.chemometria.us.edu.pl/download/optics.py

    :param array: data set in m-objects x n-variables numpy.array format
    :param min_pts: the number of points to be a cluster
    :param distance_method: scipy distance method
    :return: reachability distances, core distances and data set order
    """

    if len(array.shape) > 1:
        m, _ = array.shape
    else:
        m = array.shape[0]

    distance_array = squareform(pdist(array, distance_method))

    core_distance = numpy.zeros(m)
    reach_distance = numpy.ones(m) * numpy.inf

    for i in range(m):
        tmp_index = distance_array[i].argsort()
        tmp_distance = distance_array[i][tmp_index]
        core_distance[i] = tmp_distance[min_pts]

    order = []
    seeds = numpy.arange(m, dtype=numpy.int)

    ind = 0
    while len(seeds) != 1:
        obj = seeds[ind]
        seed_ind = numpy.where(seeds != obj)
        seeds = seeds[seed_ind] # array sem o objeto

        order.append(obj)
        tmp_array = numpy.ones(len(seeds)) * core_distance[obj]
        tmp_distance = distance_array[obj][seeds]

        stacked = numpy.column_stack((tmp_array, tmp_distance))
        stacked_max = numpy.max(stacked, axis = 1)
        ii = numpy.where(reach_distance[seeds] > stacked_max)[0]
        reach_distance[seeds[ii]] = stacked_max[ii]
        ind = numpy.argmin(reach_distance[seeds])

    order.append(seeds[0])
    reach_distance[0] = 0 # we set this point to 0 as it does not get overwritten

    return reach_distance, core_distance, order


class TreeNode(object):
    def __init__(self, points, order, start, end, parent_node):
        self.points = points
        self.start = start
        self.end = end
        self.parent_node = parent_node
        self.children = []
        self.split_point = -1
        self.order = order

    def __str__(self):
        return "start: %d, end %d, split: %d" % (self.start, self.end, self.split_point)


    def assign_split_point(self,split_point):
        self.split_point = split_point

    def add_child(self, child):
        self.children.append(child)


def _is_local_maxima(index, reach_plot, nbh_size):
    """Test if a reachability_plot value is a local maxima

    :param index: The index of the value in reach_plot to check
    :param reach_plot: An array of reachability plot values
    :param nbh_size: The size of the neighborhood
    :return: Boolean True or False
    """

    reach_plot_size = len(reach_plot)

    for i in range(1, nbh_size + 1):
        # test if index is inside limits
        if index + i < reach_plot_size and index - i >= 0:
            current = reach_plot[index]
            previous = reach_plot[index - i]
            next = reach_plot[index + i]
            return previous <= current >= next

    return False


def _find_local_maxima(reach_plot, reach_points, nbh_size):

    def aux_comparison(i, reach_plot, nbh_size):
        higher = reach_plot[i+1] <= reach_plot[i] > reach_plot[i-1]
        local_max_text = _is_local_maxima(i, reach_plot, nbh_size)
        return local_max_text and higher

    local_maxima_points = {}

    # 1st and last points on Reachability Plot are not taken as local maxima points
    for i in range(1, len(reach_points) - 1):
        # if the point is a local maxima on the reachability plot with
        # regard to nbh_size, insert it into priority queue and maxima list
        if aux_comparison(i, reach_plot, nbh_size):
            local_maxima_points[i] = reach_plot[i]

    return sorted(local_maxima_points, key=local_maxima_points.__getitem__ , reverse=True)


def _get_check_value(node, check_ratio=0.8):
    return int(numpy.round(check_ratio * len(node.points)))


def _get_average_reach_value(node, reach_plot, node_number, check_ratio=0.8):
    check_value = _get_check_value(node, check_ratio)
    if node_number == 1:
        init = node.end - check_value
        final = node.end
    else:
        init = node.start
        final = node.start + check_value
    value = reach_plot[init:final]
    return float(numpy.average(value))


def _split_local_maxima(local_maxima_points, split_point):
    seq_1 = []
    seq_2 = []
    for point in local_maxima_points:
        if point < split_point:
            seq_1.append(point)
        elif point > split_point:
            seq_2.append(point)
    return seq_1, seq_2


def _make_node_list(node, reach_points, order, local_maxima_points, split_point):
    points_1 = reach_points[node.start:split_point]
    points_2 = reach_points[split_point + 1:node.end]

    order_1 = order[node.start:split_point]
    order_2 = order[split_point + 1:node.end]

    node_1 = TreeNode(points_1, order_1, node.start,split_point, node)
    node_2 = TreeNode(points_2, order_2, split_point + 1, node.end, node)
    local_max_1, local_max_2 = _split_local_maxima(local_maxima_points, split_point)

    node_list = []
    node_list.append((node_1, local_max_1))
    node_list.append((node_2, local_max_2))
    return node_list


def _inside_ratios_test(node, node_and_local_1, node_and_local_2, node_list, reach_plot, local_maxima_value):
    # only check a certain ratio of points in the child nodes
    # formed to the left and right of the maxima

    node_1 = node_and_local_1[0]
    node_2 = node_and_local_2[0]

    check_ratio = .8

    avg_reach_value_1 = _get_average_reach_value(node_1, reach_plot, 1, check_ratio)
    avg_reach_value_2 = _get_average_reach_value(node_2, reach_plot, 2, check_ratio)

    # To adjust the fineness of the clustering, adjust the following ratios.
    # The higher the ratio, the more generous the algorithm is to preserving
    # local minimums, and the more cuts the resulting tree will have.

    # the maximum ratio we allow of average height of clusters
    # on the right and left to the local maxima in question
    maxima_ratio = .75

    # if ratio above exceeds maxima_ratio, find which of the clusters
    # to the left and right to reject based on rejection_ratio
    rejection_ratio = .7

    ratio_avg_reach_value_1 = avg_reach_value_1 / local_maxima_value
    ratio_avg_reach_value_2 = avg_reach_value_2 / local_maxima_value

    if ratio_avg_reach_value_1 > maxima_ratio or ratio_avg_reach_value_2 > maxima_ratio:

        if ratio_avg_reach_value_1 < rejection_ratio:
            #reject node 2
            node_list.remove(node_and_local_2)

        if ratio_avg_reach_value_2 < rejection_ratio:
            #reject node 1
            node_list.remove(node_and_local_1)

        if ratio_avg_reach_value_1 >= rejection_ratio <= ratio_avg_reach_value_2:
            node.assign_split_point(-1)
            # since split_point is not significant, ignore this split and continue (reject both child nodes)
            return True

    return False


def _remove_small_clusters(node_and_local_1, node_and_local_2, node_list, min_cluster_size):
    node_1 = node_and_local_1[0]
    node_2 = node_and_local_2[0]

    #remove clusters that are too small
    if len(node_1.points) < min_cluster_size:
        if node_and_local_1 in node_list:
            node_list.remove(node_and_local_1)
    if len(node_2.points) < min_cluster_size:
        if node_and_local_2 in node_list:
            node_list.remove(node_and_local_2)


def _get_node_or_parent(node, parent_node, reach_plot, similarity_threshold):
    """
    Check if nodes can be moved up one level - the new cluster created
    is too "similar" to its parent, given the similarity threshold.
    Similarity can be determined by 1)the size of the new cluster relative
    to the size of the parent node or 2)the average of the reachability
    values of the new cluster relative to the average of the
    reachability values of the parent node
    A lower value for the similarity threshold means less levels in the tree.
    """

    if parent_node != None:
        sum_reach_plot = numpy.average(reach_plot[node.start:node.end])
        sum_parent_node = numpy.average(reach_plot[parent_node.start:parent_node.end])
        if node.end-node.start / float(parent_node.end-parent_node.start) > similarity_threshold: #1)
            # if sum_reach_plot / float(sum_parent_node) > similarity_threshold: #2)
            parent_node.children.remove(node)
            return parent_node

    return node


def cluster_tree(node, parent_node, local_maxima_points, reach_plot, reach_points, order, min_cluster_size):
    # node is a node or the root of the tree in the first call
    # parentNode is parent node of N or None if node is root of the tree
    # localMaximaPoints is list of local maxima points sorted in descending order of reachability
    # set a lower threshold on how small a significant maxima can be
    significant_min = .003
    similarity_threshold = 0.4

    if len(local_maxima_points) == 0:
        return # parentNode is a leaf

    # take largest local maximum as possible separation between clusters
    split_point = local_maxima_points[0]
    node.assign_split_point(split_point)
    local_maxima_points = local_maxima_points[1:]

    local_maxima_value = reach_plot[split_point]

    # create two new nodes and add to list of nodes
    node_list = _make_node_list(node, reach_points, order, local_maxima_points, split_point)
    node_and_local_1, node_and_local_2 = node_list

    if local_maxima_value < significant_min:
        node.assign_split_point(-1)
        # if split_point is not significant, ignore this split and continue
        cluster_tree(node, parent_node, local_maxima_points, reach_plot, reach_points, order, min_cluster_size)
        return

    if _inside_ratios_test(node, node_and_local_1, node_and_local_2, node_list, reach_plot, local_maxima_value):
        cluster_tree(node, parent_node, local_maxima_points, reach_plot, reach_points, order, min_cluster_size)
        return

    #remove clusters that are too small
    _remove_small_clusters(node_and_local_1, node_and_local_2, node_list, min_cluster_size)

    if len(node_list) == 0:
        #parentNode will be a leaf
        node.assign_split_point(-1)
        return

    # move up node

    # set obj as node or parent_node
    node_or_parent_obj = _get_node_or_parent(node, parent_node, reach_plot, similarity_threshold)

    for n, l in node_list:
        node_or_parent_obj.add_child(n)
        cluster_tree(n, node_or_parent_obj, l, reach_plot, reach_points, order, min_cluster_size)


def automatic_cluster(reach_plot, reach_points, order):

    min_cluster_size_ratio = .005
    min_neighborhood_size = 2
    min_maxima_ratio = 0.001

    min_cluster_size = int(min_cluster_size_ratio * len(reach_points))

    if min_cluster_size < 5:
        min_cluster_size = 5


    nbh_size = int(min_maxima_ratio * len(reach_points))

    if nbh_size < min_neighborhood_size:
        nbh_size = min_neighborhood_size

    local_maxima_points = _find_local_maxima(reach_plot, reach_points, nbh_size)

    root_node = TreeNode(reach_points, order, 0, len(reach_points), None)
    cluster_tree(root_node, None, local_maxima_points, reach_plot, reach_points, order, min_cluster_size)

    return root_node


def automatic_optics_cluster(array, min_pts=9, distance_method="euclidean"):
    reach_plot, reach_points, order = optics(array, min_pts, distance_method)
    return automatic_cluster(reach_plot, reach_points, order)


def get_array(node, num, arr):
    if node:
        if len(arr) <= num:
            arr.append([])
        try:
            arr[num].append(node)
        except:
            arr[num] = []
            arr[num].append(node)
        for n in node.children:
            get_array(n, num + 1, arr)
        return arr
    else:
        return arr


def get_leaves(node, arr):
    if node:
        if node.split_point == -1:
            arr.append(node)
        for n in node.children:
            get_leaves(n, arr)
    return arr


def graph_tree(root, RPlot):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    a1 = [i for i in range(len(RPlot))]
    ax.vlines(a1, 0, RPlot)

    plt.xlabel('Order of points')
    plt.ylabel('Reachability-distance')

    num = 2
    graph_node(root, num, ax)

    # plt.savefig('RPlot.png', dpi=None, facecolor='w', edgecolor='w',
    #   orientation='portrait', papertype=None, format=None,
    #  transparent=False, bbox_inches=None, pad_inches=0.1)
    plt.show()


def order_reach_plot(array, min_pts=9):
    # run the OPTICS algorithm on the points, using a min_pts value (0 = no min_pts)
    reach_dist, core_dist, order = optics(array, min_pts)
    reach_plot = []
    reach_points = []

    # return reach_dist, reach_points, order

    for item in order:
        reach_plot.append(reach_dist[item]) # Reachability Plot
        reach_points.append([array[item][0], array[item][1]]) # points in their order determined by OPTICS

    return reach_plot, reach_points, order


def graph_node(node, num, ax):
    ax.hlines(num,node.start,node.end,color="red")
    for item in node.children:
        graph_node(item, num - .4, ax)


def print_tree(node, num):
    if node is not None:
        print(("Level %d" % num))
        print((str(node)))
        for n in node.children:
            print_tree(n, num+1)


def write_tree(file_w, location_map, RPoints, node, num):
    if node is not None:
        file_w.write("Level " + str(num) + "\n")
        file_w.write(str(node) + "\n")
        for x in range(node.start,node.end):
            item = RPoints[x]
            lon = item[0]
            lat = item[1]
            place_name = location_map[(lon,lat)]
            s = str(x) + ',' + place_name + ', ' + str(lat) + ', ' + str(lon) + '\n'
            file_w.write(s)
        file_w.write("\n")
        for n in node.children:
            write_tree(file_w, location_map, RPoints, n, num+1)
