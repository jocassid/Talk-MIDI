
# Snippets of code from:
# * https://nbviewer.org/github/craffel/pretty-midi/blob/main/Tutorial.ipynb

from pretty_midi import Instrument, Note, PrettyMIDI

pm = PrettyMIDI(initial_tempo=120)

cello = Instrument(program=42, is_drum=False, name="My Cello")
pm.instruments.append(cello)

print(f"{pm.instruments=}")

velocity = 100
for pitch, start, end in zip(
        [60, 62, 64],
        [0.2, 0.6, 1.0],  # "wall clock" time (seconds)
        [1.1, 1.7, 2.3],
):
    cello.notes.append(Note(velocity, pitch, start, end))
print(f"{cello.notes=}")