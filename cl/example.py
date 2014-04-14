# http://glowingpython.blogspot.com.br/2012/04/k-means-clustering-with-scipy.html

from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

# data generation
a = rand(150,2)
b = a + array([.5,.5])

data = vstack((a, b))

# computing K-Means with K = 2 (2 clusters)
centroids,_ = kmeans(data,2)
# assign each sample to a cluster_analysis
idx,_ = vq(data,centroids)

print(data[:10])
print centroids

# some plotting using numpy's logical indexing
plot(data[idx==0,0],data[idx==0,1],'ob',
     data[idx==1,0],data[idx==1,1],'or')
plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
show()