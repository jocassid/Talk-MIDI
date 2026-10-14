#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from os.path import exists
from pathlib import Path
from typing import Callable, Iterable, Any

from mido import Message, MetaMessage, MidiFile, MidiTrack


REPEAT_NUMBER_DEFAULT: int = 2


def add_message_to_track(track_out: MidiTrack, message: Message):
    """print the message before appending it to track"""
    print(f"{message}")
    track_out.append(message)


def process_messages(
        track_in: MidiTrack,
        track_out: MidiTrack,
        repetition: int,
) -> None:

    for message_index, message in enumerate(track_in):
        msg_type: str = message.type
        if msg_type in ['note_on', 'note_off']:
            add_message_to_track(track_out, message)
        elif message.type in ['track_name', 'set_tempo']:
            if repetition < 1:
                add_message_to_track(track_out, message)
        elif message.type == 'end_of_track':
            continue
        else:
            print(f"Unhandled message type: {message}")
            continue


def has_notes(track: MidiTrack) -> bool:
    for message in track:
        if message.type == 'note_on':
            return True
    return False


def main(args: Namespace):
    input_file: Path = args.input_file
    output_file: Path = args.output_file
    repetitions: int = args.number

    if not input_file.exists():
        raise IOError(f'File {input_file} does not exist')

    midi_file_in = MidiFile(input_file)
    midi_file_out = MidiFile(
        type=midi_file_in.type,
        ticks_per_beat=midi_file_in.ticks_per_beat
    )

    for repetition in range(repetitions):
        for track_index, track_in in enumerate(midi_file_in.tracks):
            if repetition == 0:
                track_out = midi_file_out.add_track()
            else:
                track_out= midi_file_out.tracks[track_index]

            process_messages(
                track_in,
                track_out,
                repetition,
            )

        for track in midi_file_out.tracks:
            track.append(MetaMessage('end_of_track'))

    midi_file_out.save(output_file)


def build_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        '-n', '--number',
        type=int,
        default=REPEAT_NUMBER_DEFAULT,
        help=f'number of times to repeat (default: {REPEAT_NUMBER_DEFAULT})'
    )
    parser.add_argument(
        'input_file',
        type=Path,
        metavar='INPUT_FILE',
        help='input MIDI file',
    )
    parser.add_argument(
        'output_file',
        type=Path,
        metavar='OUTPUT_FILE',
        help='output MIDI file',
    )
    return parser


if __name__ == '__main__':
    main(build_arg_parser().parse_args())