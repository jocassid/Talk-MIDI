
from pretty_midi import Instrument, PrettyMIDI

pm = PrettyMIDI(initial_tempo=120)

cello = Instrument(program=42, is_drum=False, name="My Cello")
pm.instruments.append(cello)

print(f"{pm.instruments=}")