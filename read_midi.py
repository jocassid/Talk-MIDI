#!/usr/bin/env python3

from io import FileIO, BufferedReader
from struct import unpack, unpack_from
from sys import stderr


FORMAT_DESCRIPTIONS = {
    0: "file contains a single multi-channel track",
    1: "file contains one or more simultaneous tracks (or MIDI outputs) of a sequence",
    2: "file contains one or more sequentially independent single-track patterns",
}

BIT0_MASK = 1
BIT1_MASK = 2
BIT2_MASK = 4
BIT3_MASK = 8
BIT4_MASK = 16
BIT5_MASK = 32
BIT6_MASK = 64
BIT7_MASK = 128

UINT8_FORMAT = '>B'
UINT16_FORMAT = '>H'
UINT32_FORMAT = '>I'


def bytes_to_int(bytes_: bytes, struct_format: str) -> int:
    values = unpack_from(struct_format, bytes_)
    if len(values) != 1:
        raise ValueError(f"Expected 1 value, got {len(values)}")
    return values[0]


def read_int(
        reader: BufferedReader,
        number_bytes: int,
        struct_format: str,
) -> int:
    bytes_read: bytes = reader.read(number_bytes)
    return bytes_to_int(bytes_read, struct_format)


def read_uint16(reader: BufferedReader) -> int:
    return read_int(reader, 2, UINT16_FORMAT)


def read_uint32(reader: BufferedReader) -> int:
    return read_int(reader, 4, UINT32_FORMAT)








def read_header_chunk(reader: BufferedReader, chunk_length: int):
    midi_format = read_uint16(reader)  # <format> in the MIDI spec
    format_description = FORMAT_DESCRIPTIONS.get(midi_format) or f"Unknown format: {midi_format}"
    print(f"{midi_format=} ({format_description})")

    num_tracks = read_uint16(reader)  # <ntrks> in the MIDI spec
    print(f"{num_tracks=}")

    division_bytes: bytes = reader.read(2)
    print(f"{division_bytes=}")
    first_byte = division_bytes[0]
    print(f"{bin(first_byte)=}")
    division_bit15 = first_byte & BIT7_MASK
    print(f"{division_bit15=}")
    if division_bit15:
        negative_smpte_format = first_byte & (~ BIT7_MASK)
        ticks_per_frame = bytes_to_int(division_bytes, UINT8_FORMAT)
        print(f"{negative_smpte_format=}")
        print(f"{ticks_per_frame=}")
    else:
        ticks_per_quarter_note = bytes_to_int(division_bytes, UINT16_FORMAT)
        print(f"{ticks_per_quarter_note=}")
        ...

# << shift left
# >> shift right
# &  and
# |  or
# ~  not
# ^  xor



def read_track_chunk(reader: BufferedReader, chunk_length: int):
    pass


def read_chunks(reader: BufferedReader):

    while True:
        four_bytes = reader.read(4)
        if not four_bytes:
            break
        print(f"{four_bytes=}")

        chunk_type = four_bytes.decode('ascii')
        print(f"{chunk_type=}")

        chunk_length = read_uint32(reader)
        print(f"{chunk_length=}")

        if chunk_type == 'MThd':
            read_header_chunk(reader, chunk_length)
        elif chunk_type == 'MTrk':
            read_track_chunk(reader, chunk_length)
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

