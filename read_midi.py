#!/usr/bin/env python3

from io import FileIO, BufferedReader
from struct import unpack, unpack_from
from sys import stderr


FORMAT_DESCRIPTIONS = {
    0: "file contains a single multi-channel track",
    1: "file contains one or more simultaneous tracks (or MIDI outputs) of a sequence",
    2: "file contains one or more sequentially independent single-track patterns",
}

BIT0_MASK = 128



def read_int(
        reader: BufferedReader,
        number_bytes: int,
        struct_format: str,
) -> int:
    bytes_read: bytes = reader.read(number_bytes)
    values = unpack_from(struct_format, bytes_read)
    if len(values) != 1:
        raise ValueError(f"Expected 1 value, got {len(values)}")
    return values[0]


def read_uint16(reader: BufferedReader) -> int:
    return read_int(reader, 2, '>H')


def read_uint32(reader: BufferedReader) -> int:
    return read_int(reader, 4, '>I')






def read_header_chunk(reader: BufferedReader, chunk_length: int):
    midi_format = read_uint16(reader)  # <format> in the MIDI spec
    format_description = FORMAT_DESCRIPTIONS.get(midi_format) or f"Unknown format: {midi_format}"
    print(f"{midi_format=} ({format_description})")

    num_tracks = read_uint16(reader)  # <ntrks> in the MIDI spec
    print(f"{num_tracks=}")

    division_bytes: bytes = reader.read(2)
    first_bit_value = division_bytes[0] & BIT0_MASK
    if first_bit_value:  # does the first byte start with 1
        print(f"{first_bit_value=}")





def read_track_chunk(reader: BufferedReader, chunk_length: int):
    pass


def read_chunks(reader: BufferedReader):
    four_bytes = reader.read(4)
    chunk_type = four_bytes.decode('ascii')
    print(f"{chunk_type=}")

    chunk_length = read_uint32(reader)
    print(f"{chunk_length=}")

    if chunk_type == 'MThd':
        return read_header_chunk(reader, chunk_length)
    elif chunk_type == 'MTrk':
        return read_track_chunk(reader, chunk_length)
    else:
        print(f'Unknown chunk type: {chunk_type}', file=stderr)
    pass

def read_midi(file_path):
    with FileIO(file_path, 'rb') as in_file:
        reader = BufferedReader(in_file, buffer_size=512)
        read_chunks(reader)


def main():
    read_midi('Drum_sample2.mid')


if __name__ == '__main__':
    main()

