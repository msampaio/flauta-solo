import os
import music21
import re
import numpy
import pickle


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


def get_music_data(pattern='^((I.*)|(E.*E)).xml$'):
    user = os.path.expanduser('~')
    base = os.path.join([user, 'Copy', 'Genos Research', 'Flauta Solo', 'Partituras'])

    music_data = []
    for f in get_files(pattern, base):
        print 'Processing {0}'.format(f)
        try:
            music_data.extend(get_from_single_file(f, base))

        except (AttributeError, music21.converter.ConverterException):
            pass

    return numpy.array(music_data)

def save_pickle(path, data):
    """Save the given object in its corresponding filename."""

    pickleFile = os.path.join(path)
    with open(pickleFile, 'w') as fileobj:
        pickle.dump(data, fileobj)


def load_pickle(path):
    """Loads the object with the given structure type and idn."""

    with open(path, 'r') as fileobj:
        return pickle.load(fileobj)
