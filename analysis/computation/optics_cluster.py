"""
Automatic Clustering of Hierarchical Clustering Representations

Library Dependencies: numpy, if graphing is desired - matplotlib
OPTICS implementation used has dependencies include numpy, scipy, and hcluster

An implementation of the following algorithm, with some minor add-ons:
J. Sander, X. Qin, Z. Lu, N. Niu, A. Kovarsky, K. Whang, J. Jeon, K. Shim, J. Srivastava, Automatic extraction of
clusters from hierarchical clustering representations. Advances in Knowledge Discovery and Data Mining (2003)
Springer Berlin / Heidelberg. 567-567
available from http://dx.doi.org/10.1007/3-540-36175-8_8

Implemented in Python by Amy X. Zhang, Cambridge Computer Laboratory.
March 2012
amy.xian.zhang@gmail.com
http://amyxzhang.wordpress.com


Optics:

 -------------------------------------------------------------------------
 Function:
 [RD,CD,order]=optics(x,k)
 -------------------------------------------------------------------------
 Aim:
 Ordering objects of a data set to obtain the clustering structure
 -------------------------------------------------------------------------
 Input:
 x - data set (m,n); m-objects, n-variables
 k - number of objects in a neighborhood of the selected object
 (minimal number of objects considered as a cluster)
 -------------------------------------------------------------------------
 Output:
 RD - vector with reachability distances (m,1)
 CD - vector with core distances (m,1)
 order - vector specifying the order of objects (1,m)
 -------------------------------------------------------------------------
 Example of use:
 x=[randn(30,2)*.4;randn(40,2)*.5+ones(40,1)*[4 4]];
 [RD,CD,order]=optics(x,4)
 -------------------------------------------------------------------------
 References:
 [1] M. Ankrest, M. Breunig, H. Kriegel, J. Sander,
 OPTICS: Ordering Points To Identify the Clustering Structure,
 available from www.dbs.informatik.uni-muenchen.de/cgi-bin/papers?query=--CO
 [2] M. Daszykowski, B. Walczak, D.L. Massart, Looking for natural
 patterns in analytical data. Part 2. Tracing local density
 with OPTICS, J. Chem. Inf. Comput. Sci. 42 (2002) 500-507
 -------------------------------------------------------------------------
 Written by Michal Daszykowski
 Department of Chemometrics, Institute of Chemistry,
 The University of Silesia
 December 2004
 http://www.chemometria.us.edu.pl

ported to python Jan, 2009 by Brian H. Clowers, Pacific Northwest National Laboratory.
Dependencies include scipy, numpy, and hcluster.
bhclowers at gmail.com
"""


# import hcluster as H
from matplotlib import pyplot as plt
import numpy
from scipy.spatial.distance import squareform, pdist


def optics(x, k, dist_method = 'euclidean'):
    if len(x.shape)>1:
        m,n = x.shape
    else:
        m = x.shape[0]
        n = 1

    try:
        distance = squareform(pdist(x, dist_method))
    except Exception as ex:
        print(ex)
        print("squareform or pdist error")

    cd = numpy.zeros(m)
    rd = numpy.ones(m) * 1E10

    for i in range(m):
        # again you can use the euclid function if you don't want hcluster
        # distance = euclid(x[i],x)
        # distance.sort()
        # cd[i] = distance[k]

        temp_ind = distance[i].argsort()
        temp_d = distance[i][temp_ind]
        # temp_d.sort() #we don't use this function as it changes the reference
        cd[i] = temp_d[k]#**2


    order = []
    seeds = numpy.arange(m, dtype = numpy.int)

    ind = 0
    while len(seeds) != 1:
    # for seed in seeds:
        ob = seeds[ind]
        seed_ind = numpy.where(seeds != ob)
        seeds = seeds[seed_ind]

        order.append(ob)
        tempX = numpy.ones(len(seeds))*cd[ob]
        temp_d = distance[ob][seeds]#[seeds]
        # you can use this function if you don't want to use hcluster
        # temp_d = euclid(x[ob],x[seeds])

        temp = numpy.column_stack((tempX, temp_d))
        mm = numpy.max(temp, axis = 1)
        ii = numpy.where(rd[seeds]>mm)[0]
        rd[seeds[ii]] = mm[ii]
        ind = numpy.argmin(rd[seeds])


    order.append(seeds[0])
    rd[0] = 0 # we set this point to 0 as it does not get overwritten
    return rd, cd, order


def is_local_maxima(index, RPlot, RPoints, nghsize):
    # 0 = point at index is not local maxima
    # 1 = point at index is local maxima

    for i in range(1,nghsize+1):
        #process objects to the right of index
        if index + i < len(RPlot):
            if (RPlot[index] < RPlot[index+i]):
                return 0

        #process objects to the left of index
        if index - i >= 0:
            if (RPlot[index] < RPlot[index-i]):
                return 0

    return 1


def find_local_maxima(RPlot, RPoints, nghsize):

    local_maxima_points = {}

    # 1st and last points on Reachability Plot are not taken as local maxima points
    for i in range(1,len(RPoints)-1):
        # if the point is a local maxima on the reachability plot with
        # regard to nghsize, insert it into priority queue and maxima list
        if all([RPlot[i] > RPlot[i-1], RPlot[i] >= RPlot[i+1], is_local_maxima(i,RPlot,RPoints,nghsize) == 1]):
            local_maxima_points[i] = RPlot[i]

    return sorted(local_maxima_points, key=local_maxima_points.__getitem__ , reverse=True)


def cluster_tree(node, parent_node, local_maxima_points, RPlot, RPoints, min_cluster_size):
    # node is a node or the root of the tree in the first call
    # parentNode is parent node of N or None if node is root of the tree
    # localMaximaPoints is list of local maxima points sorted in descending order of reachability
    if len(local_maxima_points) == 0:
        return # parentNode is a leaf

    # take largest local maximum as possible separation between clusters
    s = local_maxima_points[0]
    node.assign_split_point(s)
    local_maxima_points = local_maxima_points[1:]

    # create two new nodes and add to list of nodes
    node_1 = TreeNode(RPoints[node.start:s],node.start,s, node)
    node_2 = TreeNode(RPoints[s+1:node.end],s+1, node.end, node)
    local_max_1 = []
    local_max_2 = []

    for i in local_maxima_points:
        if i < s:
            local_max_1.append(i)
        if i > s:
            local_max_2.append(i)

    node_list = []
    node_list.append((node_1,local_max_1))
    node_list.append((node_2,local_max_2))

    #set a lower threshold on how small a significant maxima can be
    significant_min = .003

    if RPlot[s] < significant_min:
        node.assign_split_point(-1)
        #if split_point is not significant, ignore this split and continue
        cluster_tree(node, parent_node, local_maxima_points, RPlot, RPoints, min_cluster_size)
        return


    #only check a certain ratio of points in the child nodes formed to the left and right of the maxima
    check_ratio = .8
    check_value_1 = int(numpy.round(check_ratio*len(node_1.points)))
    check_value_2 = int(numpy.round(check_ratio*len(node_2.points)))
    if check_value_2 == 0:
        check_value_2 = 1
    avg_reach_value_1 = float(numpy.average(RPlot[(node_1.end - check_value_1):node_1.end]))
    avg_reach_value_2 = float(numpy.average(RPlot[node_2.start:(node_2.start + check_value_2)]))


    """
    To adjust the fineness of the clustering, adjust the following ratios.
    The higher the ratio, the more generous the algorithm is to preserving
    local minimums, and the more cuts the resulting tree will have.
    """

    #the maximum ratio we allow of average height of clusters on the right and left to the local maxima in question
    maxima_ratio = .75

    #if ratio above exceeds maxima_ratio, find which of the clusters to the left and right to reject based on rejection_ratio
    rejection_ratio = .7

    if float(avg_reach_value_1 / float(RPlot[s])) > maxima_ratio or float(avg_reach_value_2 / float(RPlot[s])) > maxima_ratio:

        if float(avg_reach_value_1 / float(RPlot[s])) < rejection_ratio:
          #reject node 2
            node_list.remove((node_2, local_max_2))
        if float(avg_reach_value_2 / float(RPlot[s])) < rejection_ratio:
          #reject node 1
            node_list.remove((node_1, local_max_1))
        if float(avg_reach_value_1 / float(RPlot[s])) >= rejection_ratio and float(avg_reach_value_2 / float(RPlot[s])) >= rejection_ratio:
            node.assign_split_point(-1)
            #since split_point is not significant, ignore this split and continue (reject both child nodes)
            cluster_tree(node,parent_node, local_maxima_points, RPlot, RPoints, min_cluster_size)
            return

    #remove clusters that are too small
    if len(node_1.points) < min_cluster_size:
        #cluster 1 is too small"
        try:
            node_list.remove((node_1, local_max_1))
        except Exception:
            # sys.exc_clear()
            pass
    if len(node_2.points) < min_cluster_size:
        #cluster 2 is too small
        try:
            node_list.remove((node_2, local_max_2))
        except Exception:
            # sys.exc_clear()
            pass
    if len(node_list) == 0:
        #parentNode will be a leaf
        node.assign_split_point(-1)
        return

###
    """
    Check if nodes can be moved up one level - the new cluster created
    is too "similar" to its parent, given the similarity threshold.
    Similarity can be determined by 1)the size of the new cluster relative
    to the size of the parent node or 2)the average of the reachability
    values of the new cluster relative to the average of the
    reachability values of the parent node
    A lower value for the similarity threshold means less levels in the tree.
    """

    similarity_threshold = 0.4
    bypass_node = 0
    if parent_node != None:
        sum_RP = numpy.average(RPlot[node.start:node.end])
        sum_parent = numpy.average(RPlot[parent_node.start:parent_node.end])
        if float(float(node.end-node.start) / float(parent_node.end-parent_node.start)) > similarity_threshold: #1)
        #if float(float(sum_RP) / float(sum_parent)) > similarity_threshold: #2)
            parent_node.children.remove(node)
            bypass_node = 1

    for nl in node_list:
        if bypass_node == 1:
            parent_node.add_child(nl[0])
            cluster_tree(nl[0], parent_node, nl[1], RPlot, RPoints, min_cluster_size)
        else:
            node.add_child(nl[0])
            cluster_tree(nl[0], node, nl[1], RPlot, RPoints, min_cluster_size)


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


def get_array(node,num, arr):
    if node is not None:
        if len(arr) <= num:
            arr.append([])
        try:
            arr[num].append(node)
        except:
            arr[num] = []
            arr[num].append(node)
        for n in node.children:
            get_array(n,num+1,arr)
        return arr
    else:
        return arr


def get_leaves(node, arr):
    if node is not None:
        if node.split_point == -1:
            arr.append(node)
        for n in node.children:
            get_leaves(n,arr)
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


def graph_node(node, num, ax):
    ax.hlines(num,node.start,node.end,color="red")
    for item in node.children:
        graph_node(item, num - .4, ax)


def automatic_cluster(RPlot, RPoints):

    min_cluster_size_ratio = .005
    min_neighborhood_size = 2
    min_maxima_ratio = 0.001

    min_cluster_size = int(min_cluster_size_ratio * len(RPoints))

    if min_cluster_size < 5:
        min_cluster_size = 5


    nghsize = int(min_maxima_ratio*len(RPoints))

    if nghsize < min_neighborhood_size:
        nghsize = min_neighborhood_size

    local_maxima_points = find_local_maxima(RPlot, RPoints, nghsize)

    root_node = TreeNode(RPoints, 0, len(RPoints), None)
    cluster_tree(root_node, None, local_maxima_points, RPlot, RPoints, min_cluster_size)


    return root_node


class TreeNode(object):
    def __init__(self, points, start, end, parent_node):
        self.points = points
        self.start = start
        self.end = end
        self.parent_node = parent_node
        self.children = []
        self.split_point = -1

    def __str__(self):
        return "start: %d, end %d, split: %d" % (self.start, self.end, self.split_point)


    def assign_split_point(self,split_point):
        self.split_point = split_point

    def add_child(self, child):
        self.children.append(child)


def euclid(i, x):
    """euclidean(i, x) -> euclidean distance between x and y"""
    y = numpy.zeros_like(x)
    y += 1
    y *= i
    if len(x) != len(y):
        raise ValueError("vectors must be same length")

    d = (x-y)**2
    return numpy.sqrt(numpy.sum(d, axis = 1))