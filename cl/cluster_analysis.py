import scipy.cluster.vq
import scipy.cluster.hierarchy
import scipy.spatial.distance
import pylab


def plot_dendrogram(data_array):
    data_dist = scipy.spatial.distance.pdist(data_array)
    data_link = scipy.cluster.hierarchy.linkage(data_dist,'average')
    pylab.figure()
    scipy.cluster.hierarchy.dendrogram(data_link)
    pylab.show()


def plot_centroids(data, clusters=3):
    # computing K-Means with K = 2 (2 clusters)
    centroids, _ = scipy.cluster.vq.kmeans(data, clusters)

    # assign each sample to a cluster_analysis
    idx, _ = scipy.cluster.vq.vq(data, centroids)

    colors = list('brcmyk')
    args = []
    c = 0 # color number
    for cluster in range(clusters):
        # some plotting using numpy's logical indexing
        args.append(data[idx==cluster,0])
        args.append(data[idx==cluster,1])
        args.append('.' + colors[c % 6])
        c += 1

    pylab.plot(*args)
    pylab.plot(centroids[:, 0],centroids[:, 1], 'sg', markersize=8)
    pylab.show()
