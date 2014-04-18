#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy
import music21
import files


# general
def get_contour(number_sequence):
    """Return a flatten contour."""

    aux = {}
    for new, old in enumerate(sorted(list(set(number_sequence)))):
        aux[old] = new

    return [aux[new] for new in number_sequence]


def get_chromatic_ambitus(pitches):
    """Return an integer with ambitus chromatic semitones."""

    return max(pitches) - min(pitches)


# music21
def get_stream_from_path(path):
    return music21.converter.parse(path)


def get_stream(id_code, song=None, movement=None):
    """Return a Music21 stream from a given id_code."""

    return get_stream_from_path(files.get_xml_path(id_code, song, movement))


def get_stream_first_measure(music21_stream):
    part = music21_stream.getElementsByClass('Part')[0]
    measures = part.getElementsByClass('Measure')
    return measures[0]


def get_stream_flatten_notes(music21_stream):
    flatten = music21_stream.flat
    return flatten.getElementsByClass('Note')


def get_note_pitch_and_position(notes_stream_seq):
    """Return a list of tuples with position (offset) and pitch (midi
    number) of a given sequence of notes in a Music 21 stream.

    >>> get_note_pitch_and_position(<music21.notes.stream>)
    [(50, 0), (54, 0.5)...]
    """

    size = notes_stream_seq[-1].offset
    r = []
    for note in notes_stream_seq:
        pitch = note.pitch.midi
        position = note.offset * 100 / size
        r.append((position, pitch))
    return r


def get_note_duration_and_position(notes_stream_seq):
    """Return a list of tuples with proportional position (offset
    normalized to 0-100) and duration (quarterLength float) of a given
    sequence of notes in a Music 21 stream.

    >>> get_note_pitch_and_position(<music21.notes.stream>)
    [(0.5, 0), (1, 0.5)...]
    """

    size = notes_stream_seq[-1].offset
    r = []
    for note in notes_stream_seq:
        pitch = note.duration.quarterLength
        position = note.offset * 100 / size
        r.append((position, pitch))
    return r


def get_stream_general_data(music21_stream):
    first_measure = get_stream_first_measure(music21_stream)

    dic = {}
    t_sig_stream = first_measure.getElementsByClass('TimeSignature')[0]
    t_sig_aux = [str(value) for value in t_sig_stream.numerator, t_sig_stream.denominator]
    key_stream, mode = first_measure.getElementsByClass('KeySignature')[0].pitchAndMode

    dic['time_signature'] = '/'.join(t_sig_aux)
    dic['meter'] = t_sig_stream.beatCountName
    dic['key'] = key_stream.fullName
    dic['mode'] = mode

    return dic


def get_data_music21_stream(music21_stream):
    """Insert Music information such as Time Signature in Source
    object."""

    filename = os.path.basename(music21_stream.filePath)
    print '. Getting info from source {0}'.format(filename)

    dic = get_stream_general_data(music21_stream)  # get dictionary with general data
    notes_stream = get_stream_flatten_notes(music21_stream)

    notes = []
    pitches = []
    durations = []

    for note in notes_stream:
        notes.append(note.nameWithOctave)
        pitches.append(note.midi)
        durations.append(note.duration.quarterLength)

    dic['notes'] = notes
    dic['pitches'] = pitches
    dic['durations'] = durations
    dic['pitch_contour'] = get_contour(pitches)
    dic['duration_contour'] = get_contour(durations)
    dic['ambitus'] = get_chromatic_ambitus(pitches)

    return dic


## TODO: Generalize i/o and functions
def get_music21_data_from_single_file(path, fn=get_note_pitch_and_position):
    music21_stream = get_stream_from_path(path)
    flatten_notes = get_stream_flatten_notes(music21_stream)

    return fn(flatten_notes)


## TODO: Generalize i/o and functions
def get_music_data(fn=get_note_pitch_and_position, pattern='^((I.*)|(E.*E)).xml$'):
    music_data = []
    for f in files.get_files(pattern):
        print 'Processing {0}'.format(os.path.basename(f))
        try:
            music_data.extend(get_music21_data_from_single_file(f, fn))


        except (AttributeError, music21.converter.ConverterException):
            pass

    return numpy.array(music_data)
