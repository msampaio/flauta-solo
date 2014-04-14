import os
import music21
import re
import numpy
import pylab
import scipy.cluster.vq

def file_test(pattern, filename):
    r = re.search(pattern, filename)
    if r:
        return r.string

def get_files(pattern, path):
    return [file_test(pattern, f) for f in os.listdir(path) if file_test(pattern, f)]

def get_stream(filename, base):
    f = os.path.join(base, filename)
    return music21.converter.parse(f)

def get_notes(stream):
    return stream.flat.notes

def get_note_and_position(notes):
    size = notes[-1].offset
    r = []
    for note in notes:
        pitch = note.pitch.midi
        position = note.offset * 100 / size
        r.append((position, pitch))
    return r

def get_from_single_file(filename, base):
    return get_note_and_position(get_notes(get_stream(filename, base)))

def main():
    pattern='^E.*E.xml$'
    user = os.path.expanduser('~')
    base = user + '/Copy/Genos Research Group/Flauta Solo/Partituras/'
    pattern = '^I.*.xml$'

    aux = []
    for f in get_files(pattern, base):
        print 'Processing {0}'.format(f)
        try:
            aux.extend(get_from_single_file(f, base))

        except (AttributeError, music21.converter.ConverterException):
            pass

    data = numpy.array(aux)

    # computing K-Means with K = 2 (2 clusters)
    centroids, _ = scipy.cluster.vq.kmeans(data, 2)
    # assign each sample to a cluster_analysis
    idx, _ = scipy.cluster.vq.vq(data, centroids)

    # some plotting using numpy's logical indexing
    pylab.plot(data[idx==0,0],data[idx==0,1],'ob',
         data[idx==1,0],data[idx==1,1],'or')
    pylab.plot(centroids[:, 0],centroids[:, 1], 'sg', markersize=8)


    pylab.show()
