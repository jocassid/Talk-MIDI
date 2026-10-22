#!/usr/bin/env python3

from typing import Iterator

from notes import C, D, E, F, G, Note


NoteBeatsAndWord = tuple[Note, int, str]


def merrily() -> Iterator[NoteBeatsAndWord]:
    for note in [C << 1, G, E, C]:
        for word in ['mer', 'ri', 'ly']:
            yield note, 1, word


# 3/4 time 100 BPM
NOTES: tuple[tuple[Note, int, str], ...] = (
    (C, 3, 'row'),
    (C, 3, 'row'),
    (C, 2, 'row'),
    (D, 1, 'your'),
    (E, 3, 'boat'),
    (E, 2, 'gen'),
    (D, 1, 'tly'),
    (E, 2, 'down'),
    (F, 1, 'the'),
    (G, 6, 'stream'),
    *merrily(),
    (G, 2, 'Life'),
    (F, 1, 'is'),
    (E, 2, 'but'),
    (D, 1, 'a'),
    (C, 6, 'dream'),
)


def write_row_row_row_your_boat(file_path: str):
    from midiutil import MIDIFile

    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)

    time = 0
    for note, duration, _ in NOTES:
        midi.addNote(
            track=0,
            channel=0,
            pitch=note.value,
            time=time,
            duration=duration,
            volume=100,
        )
        time = time + duration

    with open(file_path, 'wb') as output_file:
        midi.writeFile(output_file)

def main():
    write_row_row_row_your_boat('row_row_row_your_boat.mid')


if __name__ == '__main__':
    main()