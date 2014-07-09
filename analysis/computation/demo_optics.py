"""
Created on Mar 17, 2012

@author: Amy X Zhang
amy.xian.zhang@gmail.com
http://amyxzhang.wordpress.com


Demo of OPTICS Automatic Clustering Algorithm
https://github.com/amyxzhang/OPTICS-Automatic-Clustering
"""

import numpy
import itertools
import matplotlib.pyplot as plt

# generate some spatial data with varying densities
from analysis.computation import optics_cluster

def generate_x(n_points_per_cluster, *data):
    numpy.random.seed(0)
    empty = (0, 2)
    columns = 2
    x = numpy.empty(empty)

    for pair, f in data:
        x = numpy.r_[x, pair + f * numpy.random.randn(n_points_per_cluster, columns)]

    return x


def make_reachability_and_order(x, smoothing=9):
    # run the OPTICS algorithm on the points, using a smoothing value (0 = no smoothing)
    reach_dist, core_dist, order = optics_cluster.optics(x, smoothing)
    reach_plot = []
    reach_points = []

    for item in order:
        reach_plot.append(reach_dist[item]) #Reachability Plot
        reach_points.append([x[item][0],x[item][1]]) #points in their order determined by OPTICS

    return reach_plot, reach_points, order


def get_optics_data(x, smoothing=9):
    reach_plot, reach_points, order = make_reachability_and_order(x, smoothing)

    #hierarchically cluster the data
    root_node = optics_cluster.automatic_cluster(reach_plot, reach_points)

    #array of the TreeNode objects, position in the array is the TreeNode's level in the tree
    array = optics_cluster.get_array(root_node, 0, [0])

    #get only the leaves of the tree
    leaves = optics_cluster.get_leaves(root_node, [])

    return root_node, reach_plot, reach_points, leaves


def scatter_plot_points(x, marker, ms):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x[:,0], x[:,1], marker, ms)
    plt.show()


def scatter_optics(x, leaves, reach_points):
    # graph the points and the leaf clusters that have been found by OPTICS
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x[:,0], x[:,1], 'y.')
    colors = itertools.cycle('gmkrcbgrcmk')
    for item, c in zip(leaves, colors):
        node = []
        for v in range(item.start,item.end):
            node.append(reach_points[v])
        node = numpy.array(node)
        ax.plot(node[:,0],node[:,1], c+'o', ms=5)

    plt.show()

####

my_data = (([-5, -2], .8),
           ([4, -1], .1),
           ([1, -2], .2),
           ([-2, 3], .3),
           ([3, -2], 1.6),
           ([5, 6], 2))

X = generate_x(250, *my_data)

def main(x=X, smoothing=9):
    # get optics stuff
    root_node, reach_plot, reach_points, leaves = get_optics_data(x, smoothing=9)

    # plot scatterplot of points
    scatter_plot_points(x, 'b.', 2)

    # print Tree (DFS)
    optics_cluster.print_tree(root_node, 0)

    # graph reachability plot and tree
    optics_cluster.graph_tree(root_node, reach_plot)

    # graph the points and the leaf clusters that have been found by OPTICS
    scatter_optics(x, leaves, reach_points)