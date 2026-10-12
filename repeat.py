#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from os.path import exists
from pathlib import Path
from sys import stdin, stdout

from mido import MidiFile

REPEAT_NUMBER_DEFAULT: int = 2
PATH_DEFAULT = Path('')

def main(args: Namespace) -> None:
    print(f"{args=}")

    file_path: str = args.input_file
    if file_path:
        if not exists(file_path):
            raise IOError(f'File {file_path} does not exist')
        midi_file_in = MidiFile(file_path)
    else:
        midi_file_in = MidiFile(file=stdin)

    midi_file_out = MidiFile()

    # First pass to determine max track time
    max_track_time: int = 0
    for track in midi_file_in.tracks:
        for message in track:
            max_track_time += message.time
            print(f"{message.type=}  {message}")

















if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-n', '--number',
        type=int,
        default=REPEAT_NUMBER_DEFAULT,
        help=f'number of times to repeat (default: {REPEAT_NUMBER_DEFAULT})'
    )
    parser.add_argument(
        '-i', '--input-file',
        type=Path,
        default=PATH_DEFAULT,
        nargs='?',
        help=f'file to load, default is to read from stdin',
    )
    parser.add_argument(
        '-o', '--output-file',
        type=Path,
        default=PATH_DEFAULT,
        nargs='?',
        help=f'file to load, default is to read from stdin',
    )
    main(parser.parse_args())