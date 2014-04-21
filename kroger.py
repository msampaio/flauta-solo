import glob
import numpy
import scipy
import scipy.cluster.vq
import scipy.cluster.hierarchy
import scipy.spatial.distance
import pylab

from analysis import music


def get_music_note_data():
    files = glob.glob("/Users/kroger/Copy/Flauta Solo/Partituras/*.xml")
    music_data = []
    for filename in files[0:1]:
        print filename
        music_data.extend(music.get_music21_data_from_single_file(filename))

    return numpy.array(music_data)


def plot_dendrogram(data_array):
    data_dist = scipy.spatial.distance.pdist(data_array)
    data_link = scipy.cluster.hierarchy.linkage(data_dist,'average')
    pylab.figure(figsize=(50,50))
    #scipy.cluster.hierarchy.dendrogram(data_link, p=3, truncate_mode="level", show_contracted=True, orientation='left', show_leaf_counts=None, leaf_font_size=12)
    scipy.cluster.hierarchy.dendrogram(data_link, show_leaf_counts=None, leaf_font_size=8)
    pylab.savefig("foo.pdf")


data = get_music_note_data()
plot_dendrogram(data)
