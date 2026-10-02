
from midiutil import MIDIFile

C = 60
D = 62
E = 64
F = 65
G = 67
C2 = 72

MERRILY = ['mer', 'ri', 'ly']

# 3/4 time 100 BPM
NOTES = (
    (C, 3, 'row'),
    (C, 3, 'row'),
    (C, 2, 'row'),
    (D, 1, 'your'),
    (E, 3, 'boat'),
    (E, 2, 'gen'),
    (D, 1, 'tly'),
    (E, 2, 'down'),
    (F, 1, 'the'),
    (G, 6, 'stream'),
    *[(C2, 1, w) for w in MERRILY],
    *[(G, 1, w) for w in MERRILY],
    *[(E, 1, w) for w in MERRILY],
    *[(C, 1, w) for w in MERRILY],
    (G, 2, 'Life'),
    (F, 1, 'is'),
    (E, 2, 'but'),
    (D, 1, 'a'),
    (C, 6, 'dream'),
)

midi = MIDIFile(1)
midi.addTempo(0, 0, 100)

channel = 0
track = 0
time = 0
volume = 100
for pitch, duration, _ in NOTES:
    midi.addNote(track, channel, pitch, time, duration, volume)
    time = time + duration

with open('row_row_row_your_boat.mid', 'wb') as output_file:
    midi.writeFile(output_file)