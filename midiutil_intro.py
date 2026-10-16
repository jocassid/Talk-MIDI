#!/usr/bin/env python

from midiutil import MIDIFile

# File will have 1 track, defaults to format 1 ()
MyMIDI = MIDIFile(1)

track = 0
time = 0    # In beats
tempo = 60  # In BPM
MyMIDI.addTempo(track, time, tempo)

MyMIDI.addTempo(track, time=8, tempo=120)
MyMIDI.addTempo(track, time=16, tempo=240)

c_scale  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
channel  = 0
duration = 1   # In beats
volume   = 100 # 0-127, as per the MIDI standard
list_of_degrees = [
    c_scale,
    sorted(c_scale, reverse=True),
    c_scale,
]
for degrees in list_of_degrees:
    for pitch in degrees:
        MyMIDI.addNote(track, channel, pitch, time, duration, volume)
        time = time + 1

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)