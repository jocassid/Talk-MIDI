
FLAT = '\u266d'
SHARP = '\u266f'


class Note:

    def __init__(self, value: int, label: str):
        self.value: int = value
        self.label: str = label

    def __rshift__(self, octaves: int) -> 'Note':
        return self.shift(octaves, shift_up=True)

    def __lshift__(self, octaves: int) -> 'Note':
        return self.shift(-1 * octaves, shift_up=False)

    def shift(self, octaves: int, shift_up: bool) -> 'Note':
        delta = octaves * 12
        delta = delta if shift_up else -1 * delta
        shifted_value = self.value + delta
        self.validate_shifted_note(octaves, shifted_value)
        return Note(shifted_value, self.label)

    def validate_shifted_note(
            self,
            octaves: int,
            shifted_value: int,
    ) -> None:
        if 0 <= shifted_value <= 127:
            return None
        raise ValueError(
            f"Note {self.label} ({self.value}) {'-' if octaves < 0 else '+'} "
            f"octave{'' if -1 <= octaves <= 1 else 's'} is {shifted_value}.  "
            f"Note must be between 0 and 127"
        )


C: Note = Note(60, 'C')
Cs: Note = Note(61, f'C{SHARP}')
Df: Note = Note(61, f'D{FLAT}')
D: Note = Note(62, 'D')
Ds: Note = Note(63, f'D{SHARP}')
Ef: Note = Note(63, f'E{FLAT}')
E: Note = Note(64, 'E')
F: Note = Note(65, 'F')
Fs: Note = Note(66, f'F{SHARP}')
Gf: Note = Note(66, f'G{FLAT}')
G: Note = Note(67, 'G')
Gs: Note = Note(68, f'G{SHARP}')
Af: Note = Note(68, f'A{FLAT}')
A: Note = Note(69, 'A')
As: Note = Note(70, f'A{SHARP}')
Bf: Note = Note(70, f'B{FLAT}')
B: Note = Note(71, 'B')

C_SCALE = [C, D, E, F, G, A, B, C << 1]
