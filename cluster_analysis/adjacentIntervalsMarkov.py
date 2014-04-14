import os
import music21
import re
import numpy
from collections import Counter
from music21.interval import notesToInterval, notesToChromatic

def fileTest(pattern, filename):
    r = re.search(pattern, filename)
    if r:
        return r.string

def getIntervals(notes):
    length = len(notes)
    position = zip(range(length - 1), range(1, length))
    return [notesToChromatic(notes[x], notes[y]).semitones for x, y in position]

def makeStream(filename, base):
    f = os.path.join(base, filename)
    return music21.converter.parse(f)

def getNotes(stream):
    return stream.flat.notes

def getFiles(pattern, path):
    return [fileTest(pattern, f) for f in os.listdir(path) if fileTest(pattern, f)]

def getAdjacentIntervals(notes):
    intervals = getIntervals(notes)
    seq = range(len(intervals) - 1)
    pairs = [(intervals[i], intervals[i + 1]) for i in seq]
    return Counter(pairs)

def getAllAdjacentIntervals(path, pattern):
    countAll = Counter()
    files = []
    for f in getFiles(pattern, path):
        print 'Processing {0}'.format(f)
        try:
            stream = makeStream(f, path)
            notes = getNotes(stream)
            count = getAdjacentIntervals(notes)
            for k, v in count.items():
                if k not in countAll.keys():
                    countAll[k] = 0
                countAll[k] += v
            files.append(f)
        except (AttributeError, music21.converter.ConverterException):
            pass
    return countAll, files

def counterToMatrix(count, outFile=None):
    maxX = max(count.keys())[0]
    minX = min(count.keys())[0]
    maxY = max(count.keys(), key=lambda x: x[1])[1]
    minY = min(count.keys(), key=lambda x: x[1])[1]
    rX = range(minX, maxX + 1)
    rY = range(minY, maxY + 1)
    countX = [c[0] for c in count.keys()]
    countY = [c[1] for c in count.keys()]
    array = [[count[(x, y)] for x in rX] for y in rY]
    if outFile:
        with open(outFile, 'w') as f:
            header = ['']
            header.extend([str(el) for el in rX])
            f.write(','.join(header))
            for y in rY:
                row = [str(y)]
                row.extend([str(count[(x, y)]) for x in rX])
                f.write(','.join(row))
                f.write('\n')
    else:
        return numpy.matrix(array)

def run(pattern='^E.*E.xml$'):
    user = os.path.expanduser('~')
    base = user + '/Copy/Genos Research Group/Flauta Solo/Partituras/'
    #pattern = '^I.*.xml$'
    c, files = getAllAdjacentIntervals(base, pattern)
    counterToMatrix(c, '/tmp/intervals.csv')
    with open('/tmp/files.txt', 'w') as fname:
        for f in files:
            fname.write(f)
            fname.write('\n')
    return c

print run()
