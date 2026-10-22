#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from pathlib import Path

from mido import Message, MidiFile, MidiTrack

from notes import C_SCALE


TICKS_PER_BEAT = 360
QUARTER_NOTE_TIME = int(TICKS_PER_BEAT / 4)


def add_quarter_note(track: MidiTrack, note: int, channel: int):
    track.append(
        Message(
            type='note_on',
            channel=channel,
            note=note,
            velocity=127,
            time=0,
        )
    )
    track.append(
        Message(
            type='note_off',
            channel=channel,
            note=note,
            velocity=127,
            time=QUARTER_NOTE_TIME,
        )
    )


def main(args: Namespace):

    file = MidiFile(type=1, ticks_per_beat=TICKS_PER_BEAT)

    program = args.program
    if not (0 <= program <= 127):
        raise ValueError('Program number must be between 0 and 127')

    channel = args.channel
    if not (1 <= channel <= 16):
        raise ValueError('Channel number must be between 1 and 16')
    # Musicians count from 1, programmers count from 0
    channel -= 1

    track = file.add_track(name="many instruments")
    track.append(
        Message(type='program_change', channel=channel, program=program)
    )


    for _ in range(4):
        for note in C_SCALE:
            note = note >> 2
            add_quarter_note(
                track,
                note.value,
                channel,
            )

    file.save(args.output_file)


def build_arg_parser() -> ArgumentParser:
    # TODO: remove the channel option, write to channel 0
    parser = ArgumentParser(
        description=(
            'Generate MIDI file with specified program (instrument) on the '
            'specified channel'
        ),
    )
    parser.add_argument(
        'program',
        type=int,
        metavar='PROGRAM',
        help='program (instrument) number (0-127)',
    )
    parser.add_argument(
        'channel',
        type=int,
        metavar='CHANNEL',
        help='channel number (1-16).  Channel 10 is for percussion',
    )
    parser.add_argument(
        'output_file',
        type=Path,
        metavar='OUTPUT_FILE',
        help='output file path',
    )
    return parser


if __name__ == '__main__':
    main(build_arg_parser().parse_args())