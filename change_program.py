#!/usr/bin/env python3

from mido import Message, MidiFile, MidiTrack

from pretty_midi_intro import velocity

TICKS_PER_BEAT = 360


def add_quarter_note(track: MidiTrack, start_time: int):
    track.append(
        Message(
            type='note_on',
            channel=0,
            note=60,
            velocity=100,
            time=start_time,
        )
    )
    track.append(
        Message(
            type='note_off',
            channel=0,
            note=60,
            velocity=127,
            time=int(TICKS_PER_BEAT / 4),
        )
    )


def main():

    file = MidiFile(type=1, ticks_per_beat=TICKS_PER_BEAT)

    track = file.add_track(name="many instruments")

    for p in range(127):
        track.append(Message(type='program_change', program=p))
        for i in range(2):
            add_quarter_note(
                track,
                start_time=0 if i == 0 else TICKS_PER_BEAT * 2,
            )
            add_quarter_note(track, TICKS_PER_BEAT * 2)

    file.save('change_program.mid')


if __name__ == '__main__':
    # channel 10 used for percussion
    # add args for channel and program (instrument)
    main()