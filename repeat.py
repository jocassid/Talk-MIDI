#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from os.path import exists
from pathlib import Path
from sys import stdin, stdout
from typing import Callable, Iterable

from mido import Message, MidiFile, MidiTrack

REPEAT_NUMBER_DEFAULT: int = 2
PATH_DEFAULT = Path('')


MessageHandler = Callable[[MidiTrack, Message, int], None]


def copy_message(track: MidiTrack, message: Message):
    print(message)
    track.append(message)


def ignore_message(track: MidiTrack, message: Message, repetition: int):
    pass


def handle_track_name(track: MidiTrack, message: Message, repetition: int):
    if repetition > 1:
        return
    copy_message(track, message)


def process_messages(
        track_in: MidiTrack,
        track_out: MidiTrack,
        repetition: int,
        track_index: int,
        pause_before_first_note: int,
):
    track_time = 0
    has_notes = False
    for message_index, message in enumerate(track_in):
        track_time += message.time
        print(f"{repetition=}  {track_index=}  {message_index=}  {track_time=}")
        msg_type: str = message.type
        if msg_type in [
            'note_on',
            'note_off',
        ]:
            has_notes = True
            copy_message(track_out, message)
        elif msg_type == 'set_tempo':
            copy_message(track_out, message)
        elif message.type == 'track_name':
            handle_track_name(track_out, message, repetition)
        elif message.type == 'end_of_track':
            continue
        else:
            print(f"Unhandled message type: {message}")
            continue
    return track_time, has_notes


def get_pause_before_first_note(
        total_track_time_by_track: dict[int, int],
        track_index,
) -> int:
    max_track_length: int = max(total_track_time_by_track.values())
    track_length: int = total_track_time_by_track.get(track_index) or 0
    if track_length < 1:
        return 0
    return max_track_length - track_length


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

    total_track_time_by_track: dict[int, int] = {}
    for repetition in range(1, args.number + 1):
        for track_index, track_in in enumerate(midi_file_in.tracks):
            print(f"{track_in.name=}")

            if repetition == 1:
                track_out = midi_file_out.add_track(f"{track_index + 1}")
                pause_before_first_note = 0
            else:
                track_out= midi_file_out.tracks[track_index]
                pause_before_first_note = get_pause_before_first_note(
                    total_track_time_by_track,
                    track_index,
                )

            track_time, has_notes = process_messages(
                track_in,
                track_out,
                repetition,
                track_index,
                pause_before_first_note,
            )

            if repetition == 1 and has_notes:
                print(f"recording track time {track_index=}  {track_time=}")
                total_track_time_by_track[track_index] = track_time



    print(f"{total_track_time_by_track=}")



















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