
def sharp(c):
    return f"{c}\u266f"

def flat(c):
    return f"{c}\u266d"

def sharp_and_flat(note_before: str) -> str:
    note_after = chr(ord(note_before) + 1)
    if note_after == 'H':
        note_after = 'A'
    return "{}/{}".format(
        sharp(note_before),
        flat(note_after)
    )

notes: list[str] = [
    'C', sharp_and_flat('C'),
    'D', sharp_and_flat('D'),
    'E',
    'F', sharp_and_flat('F'),
    'G', sharp_and_flat('G'),
    'A', sharp_and_flat('A'),
    'B',
]

headings = ['Octave', *notes]
column_widths = [max(w, 3) for w in (len(s) for s in headings)]
spacer = ' '
print(
    spacer.join([
        h.rjust(w) for h, w in zip(headings, column_widths)
    ])
)
print(spacer.join(['-' * w for w in column_widths]))
for octave in range(-2, 9):
    multiple = octave + 2
    pieces = [
        str(octave).rjust(column_widths[0])
    ]
    for i, w in enumerate(column_widths[1:]):
        note_number = multiple * 12 + i
        if note_number > 127:
            pieces.append(''.rjust(w))
        else:
            pieces.append(str(note_number).rjust(w))
    print(spacer.join(pieces))

