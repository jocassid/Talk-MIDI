#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Iterator

from mido import MidiFile, MidiTrack

TOLERANCE_LOW: int = 3
TOLERANCE_HIGH: int = 7
NOTE_OFFSET = 18

def process_messages(
        track_in: MidiTrack,
        data_source: Iterator[int],
        track_out: MidiTrack,
) -> None:
    has_data = True
    for message in track_in:
        if not has_data:
            track_out.append(message)
            continue

        msg_type = message.type
        if msg_type != "note_on":
            track_out.append(message)
            continue

        try:
            reading: int = next(data_source)
        except StopIteration:
            track_out.append(message)
            has_data = False
            continue

        note = message.note
        if reading < TOLERANCE_LOW:
            message.note = note - NOTE_OFFSET
        if reading > TOLERANCE_HIGH:
            message.note = note + NOTE_OFFSET
        track_out.append(message)


def data_generator(input_data_file: Path) -> Iterator[int]:
    with input_data_file.open('r') as in_file:
        for line in in_file:
            line = line.strip()
            try:
                yield int(line)
            except ValueError:
                pass


def main(args: Namespace):
    input_data_file: Path = args.input_data_file
    input_midi_file: Path = args.input_midi_file
    output_file: Path = args.output_file

    if not input_data_file.exists():
        raise IOError(f"{input_data_file} does not exist")
    if not input_midi_file.exists():
        raise IOError(f"{input_midi_file} does not exist")

    midi_file_in = MidiFile(input_midi_file)
    midi_file_out = MidiFile(
        type=midi_file_in.type,
        ticks_per_beat=midi_file_in.ticks_per_beat
    )

    for track_in in midi_file_in.tracks:
        track_out = midi_file_out.add_track()
        process_messages(
            track_in,
            data_generator(input_data_file),
            track_out,
        )

    midi_file_out.save(output_file)


def build_arg_parser():
    parser = ArgumentParser()
    parser.add_argument(
        'input_data_file',
        type=Path,
        metavar='INPUT_DATA_FILE',
    )
    parser.add_argument(
        'input_midi_file',
        type=Path,
        metavar='INPUT_MIDI_FILE',
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