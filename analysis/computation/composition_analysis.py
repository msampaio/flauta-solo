
def analysis(composition):
    midi_notes = composition.music_data.notes
    durations_seq = composition.music_data.durations

    notes_scatter = list(map(list, enumerate(midi_notes)))
    notes_scatter.insert(0, ['Time point', 'Midi note'])

    durations_scatter = list(map(list, enumerate(durations_seq)))
    durations_scatter.insert(0, ['Time point', 'Duration note'])

    if midi_notes and durations_seq:
        args = {
            'composition': composition,
            'notes_scatter': notes_scatter,
            'durations_scatter': durations_scatter,
        }
    else:
        args = {}

    return args
