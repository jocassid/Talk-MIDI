#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from pathlib import Path

from mido import MidiFile


def main(args: Namespace):
    path = Path(args.file_path)
    if not path.exists():
        raise ValueError(f'File {path} does not exist')

    midi = MidiFile(path)
    for i, track in enumerate(midi.tracks):
        print(f'Track {i}: {track.name}')
        for msg in track:
            print(f'    {msg}')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('file_path', metavar='FILE')
    main(parser.parse_args())


if __name__ == '__main__':
    parse_args()