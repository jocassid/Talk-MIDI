# Talk-MIDI
A talk on generating MIDI files using Python

## Ideas:
* Use "Mary had a little lamb" or "Twinkle Twinkle little Star for demos"
* https://musescore.com - has free sheet music
* Yellow Notes simple piano tunes https://www.youtube.com/@WouterBruinsma/featured

## MIDI Terminology

MIDI
: Musical Instrument Digital Interface

pitch
: Refers to the frequency of a musical note.  Values are 0 (low) to 127 
(high) with middle C as 60

program
: Each instrument has a program number associated with it.  Note that a drum
instrument can share the same program number as a non-drum instrument.

tick
: time interval (not sure what a tick is at this point)

velocity
: Volume runs 1 (quietest) to 127 (loudest)

## Libraries I'm Looking at

<table>
    <thead>
        <tr>
            <th>Library</th>
            <th>Description</th>
            <th><code>pip install</code></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="https://midiutil.readthedocs.io/en/1.2.1/">MIDUtil</a></td>
            <td>Simple, multi-track MIDI file creation</td>
            <td><a href="https://pypi.org/project/MIDIUtil/"><code>pip install MIDIUtil</code></a></td>
        </tr>
        <tr>
            <td><a href="https://craffel.github.io/pretty-midi/">pretty_midi</a></td>
            <td>Advanced manipulation and analysis</td>
            <td><a href="https://pypi.org/project/pretty-midi/">pip install pretty-midi</a></td>
        </tr>
        <tr>
            <td><a href="">mido</a></td>
            <td></td>
            <td><a href="https://pypi.org/project/mido/"><code>pip install mido</code></a></td>
        </tr>
    </tbody>
</table>


## MIDIUtil

## pretty-midi

* Jupyter Notebook Tutorial https://nbviewer.org/github/craffel/pretty-midi/blob/main/Tutorial.ipynb
* Jupyter Notebook Tutorial (in Google Colab) https://colab.research.google.com/github/craffel/pretty-midi/blob/main/Tutorial.ipynb


## LMMS Setup

From the https://lmms.io/ page:

> LMMS is an open-source cross-platform digital audio workstation designed for 
> music production. It includes an advanced Piano Roll, Beat Sequencer, Song 
> Editor, and Mixer for composing, arranging, and mixing music. It comes 
> with 15+ synthesizer plugins by default, along with VST2 and SoundFont2 support.

To get LMMS to play my MIDI file, I needed to set the default soundfont in 
LMMS. I used the FreePatsGM-SF2-20221026 soundfont.

### SoundFonts sources listed on 

https://docs.lmms.io/user-manual/resources/soundfonts

| File/Folder             | Source                                                   |
|-------------------------|----------------------------------------------------------|
| FreePatsGM-SF2-20221026 | https://freepats.zenvoid.org/SoundSets/general-midi.html |

## MuseScore

For creating sheet music I'm using 
https://musescore.org/en


# Miscellaneous Resources

* https://www.loc.gov/collections/historic-sheet-music/
* https://computermusicresource.com/midikeys.html
* https://newt.phys.unsw.edu.au/jw/notes.html