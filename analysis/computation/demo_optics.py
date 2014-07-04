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

numpy.random.seed(0)

n_points_per_cluster = 250

X = numpy.empty((0, 2))
X = numpy.r_[X, [-5,-2] + .8 * numpy.random.randn(n_points_per_cluster, 2)]

X = numpy.r_[X, [4,-1] + .1 * numpy.random.randn(n_points_per_cluster, 2)]

X = numpy.r_[X, [1,-2] + .2 * numpy.random.randn(n_points_per_cluster, 2)]

X = numpy.r_[X, [-2,3] + .3 * numpy.random.randn(n_points_per_cluster, 2)]

X = numpy.r_[X, [3,-2] + 1.6 * numpy.random.randn(n_points_per_cluster, 2)]

X = numpy.r_[X, [5,6] + 2 * numpy.random.randn(n_points_per_cluster, 2)]


#plot scatterplot of points

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(X[:,0], X[:,1], 'b.', ms=2)

# plt.savefig('Graph.png', dpi=None, facecolor='w', edgecolor='w',
#     orientation='portrait', papertype=None, format=None,
#     transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)

plt.show()



#run the OPTICS algorithm on the points, using a smoothing value (0 = no smoothing)
RD, CD, order = optics_cluster.optics(X,9)

RPlot = []
RPoints = []

for item in order:
    RPlot.append(RD[item]) #Reachability Plot
    RPoints.append([X[item][0],X[item][1]]) #points in their order determined by OPTICS

#hierarchically cluster the data
rootNode = optics_cluster.automatic_cluster(RPlot, RPoints)

#print Tree (DFS)
optics_cluster.print_tree(rootNode, 0)

#graph reachability plot and tree
optics_cluster.graph_tree(rootNode, RPlot)

#array of the TreeNode objects, position in the array is the TreeNode's level in the tree
array = optics_cluster.get_array(rootNode, 0, [0])

#get only the leaves of the tree
leaves = optics_cluster.get_leaves(rootNode, [])

#graph the points and the leaf clusters that have been found by OPTICS
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(X[:,0], X[:,1], 'y.')
colors = itertools.cycle('gmkrcbgrcmk')
for item, c in zip(leaves, colors):
    node = []
    for v in range(item.start,item.end):
        node.append(RPoints[v])
    node = numpy.array(node)
    ax.plot(node[:,0],node[:,1], c+'o', ms=5)

# plt.savefig('Graph2.png', dpi=None, facecolor='w', edgecolor='w',
#     orientation='portrait', papertype=None, format=None,
#     transparent=False, bbox_inches=None, pad_inches=0.1)
plt.show()
