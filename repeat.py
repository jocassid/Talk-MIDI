#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from os.path import exists
from pathlib import Path
from sys import stdin, stdout
from typing import Callable, Iterable, Any

from mido import Message, MidiFile, MidiTrack

REPEAT_NUMBER_DEFAULT: int = 2
PATH_DEFAULT = Path('')


MessageHandler = Callable[[MidiTrack, Message, int], None]



def update_message_time(
        message_in: Message,
        pause_before_first_note: int,
) -> Message:
    msg_time: int = vars(message_in).get('time') or 0
    return message_in.copy(
        time=msg_time + pause_before_first_note
    )


def add_message_to_track(track_out: MidiTrack, message: Message):
    print(f"{message}")
    track_out.append(message)


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
        if msg_type in 'note_on':
            if not has_notes:
                message = update_message_time(message, pause_before_first_note)
                has_notes = True
            add_message_to_track(track_out, message)
        elif msg_type in ['note_off', 'set_tempo']:
            add_message_to_track(track_out, message)
        elif message.type == 'track_name':
            if repetition < 2:
                add_message_to_track(track_out, message)
        elif message.type == 'end_of_track':
            continue
        else:
            print(f"Unhandled message type: {message}")
            continue
    return track_time, has_notes


class MidiFileProcessor:

    @staticmethod
    def get_midi_file_in(input_file: Path) -> MidiFile:
        if not input_file or input_file == PATH_DEFAULT:
            return MidiFile(file=stdin)
        if not input_file.exists():
            raise IOError(f'File {input_file} does not exist')
        return MidiFile(input_file)

    @staticmethod
    def get_save_kwargs(output_file: Path) -> dict[str, Any]:
        if not output_file or output_file == PATH_DEFAULT:
            return {'file': stdout}
        return {'filename': output_file}


class Repeater(MidiFileProcessor):

    @staticmethod
    def get_pause_before_first_note(
            total_track_time_by_track: dict[int, int],
            track_index,
    ) -> int:
        max_track_length: int = max(total_track_time_by_track.values())
        track_length: int = total_track_time_by_track.get(track_index) or 0
        if track_length < 1:
            return 0
        return max_track_length - track_length



    def process(self, args: Namespace):
        self.process_inner(
            args.input_file,
            args.output_file,
            args.number,
        )

    def process_inner(self, input_file: Path, output_file: Path, repetitions: int):
        midi_file_in = self.get_midi_file_in(input_file)
        midi_file_out = MidiFile()

        total_track_time_by_track: dict[int, int] = {}
        for repetition in range(1, repetitions + 1):
            for track_index, track_in in enumerate(midi_file_in.tracks):

                if repetition == 1:
                    track_out = midi_file_out.add_track(f"{track_index + 1}")
                    pause_before_first_note = 0
                else:
                    track_out= midi_file_out.tracks[track_index]
                    pause_before_first_note = self.get_pause_before_first_note(
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

        midi_file_out.save(**self.get_save_kwargs(output_file))




def main(args: Namespace) -> None:
    print(f"{args=}")
    Repeater().process(args)


def build_arg_parser() -> ArgumentParser:
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
    return parser


if __name__ == '__main__':
    main(build_arg_parser().parse_args())