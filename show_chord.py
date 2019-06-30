import mido
import rtmidi
import signal
import pychord

signal.signal(signal.SIGINT, signal.SIG_DFL)
PITDH_LIST = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
C_MAJOR = [0, 4, 7]
C_MINOR = [0, 3, 7]
C_SUS4 = [0, 5, 7]
C_DIM = [0, 3, 6]
C_AUG = [0, 4, 8]
C_7 = [0, 4, 10]
C_MINOR_7 = [0, 3, 10]
CHORD_FROM_3 = {}
MAJOR_CHORD = {}
for i, chord in enumerate(PITDH_LIST):
    MAJOR_CHORD[chord] = {"list": [(note + i) % 12 for note in C_MAJOR],
                          "root_note": i,
                          "root": chord,
                          }
CHORD_FROM_3.update(MAJOR_CHORD)
MINOR_CHORD = {}
for i, chord in enumerate(PITDH_LIST):
    MINOR_CHORD["{}m".format(chord)] = {"list": [(note + i) % 12 for note in C_MINOR],
                                        "root_note": i,
                                        "root": chord,
                                        }
CHORD_FROM_3.update(MINOR_CHORD)
SUS4_CHORD = {}
for i, chord in enumerate(PITDH_LIST):
    SUS4_CHORD["{}sus4".format(chord)] = {"list": [(note + i) % 12 for note in C_SUS4],
                                          "root_note": i,
                                          "root": chord,
                                          }
CHORD_FROM_3.update(SUS4_CHORD)

DIM_CHORD = {}
for i, chord in enumerate(PITDH_LIST):
    DIM_CHORD["{}dim".format(chord)] = {"list": [(note + i) % 12 for note in C_DIM],
                                        "root_note": i,
                                        "root": chord,
                                        }
CHORD_FROM_3.update(DIM_CHORD)

AUG_CHORD = {}
for i, chord in enumerate(PITDH_LIST):
    AUG_CHORD["{}aug".format(chord)] = {"list": [(note + i) % 12 for note in C_AUG],
                                        "root_note": i,
                                        "root": chord,
                                        }
CHORD_FROM_3.update(AUG_CHORD)

SEVEN_CHORD = {}
for i, chord in enumerate(PITDH_LIST):
    SEVEN_CHORD["{}7".format(chord)] = {"list": [(note + i) % 12 for note in C_7],
                                        "root_note": i,
                                        "root": chord,
                                        }
CHORD_FROM_3.update(SEVEN_CHORD)

MINOR_SEVEN_CHORD = {}
for i, chord in enumerate(PITDH_LIST):
    MINOR_SEVEN_CHORD["{}m7".format(chord)] = {"list": [(note + i) % 12 for note in C_MINOR_7],
                                               "root_note": i,
                                               "root": chord,
                                               }
CHORD_FROM_3.update(MINOR_SEVEN_CHORD)

MAJOR_AND_MINOR_CHORD = MAJOR_CHORD
MAJOR_AND_MINOR_CHORD.update(MINOR_CHORD)
print(mido.get_input_names())
print(mido.get_output_names())

# inport = mido.open_input("loopMIDI Port 1")
inport = mido.open_input("Q49 0")
outport = mido.open_output("loopMIDI Port 2")
note_on_list = []


def note_to_pitch(note):
    return PITDH_LIST[note % 12]


def convert_to_base_note(note_list):
    base_note_list = []
    for note in note_list:
        base_note = note % 12
        if base_note not in base_note_list:
            base_note_list.append(base_note)
    return base_note_list


def get_base_chords_from_notes(note_list):
    base_chords = []
    for chord in CHORD_FROM_3.keys():
        if all(elem in note_list for elem in CHORD_FROM_3[chord]["list"]):
            base_chords.append(chord)
    return base_chords


def notes_to_chord(note_list):
    note_list = convert_to_base_note(note_list)
    # pitch_list = [note_to_pitch(pitch) for pitch in note_list]
    # print(pychord.note_to_chord(pitch_list))
    # return
    if len(note_list) < 3:
        return
    base_chords = get_base_chords_from_notes(note_list)
    possibility_chords = []
    if not base_chords:
        print("????")
        return
    if len(note_list) == 3:
        print(base_chords)
        return
    elif len(note_list) == 4:
        for chord in base_chords:
            root_note = CHORD_FROM_3[chord]["root_note"]
            if (root_note + 10) % 12 in note_list and chord[-1] != "7":
                chord += "7"
            elif chord[-1] == "7":
                if (root_note + 8) % 12 in note_list:
                    chord += "+5"
                elif (root_note + 6) % 12 in note_list:
                    chord += "-5"
            elif (root_note + 11) % 12 in note_list:
                chord += "M7"
            elif (root_note + 9) % 12 in note_list:
                chord += "6"
            elif (root_note + 2) % 12 in note_list:
                chord += "add9"
            else:
                continue
            possibility_chords.append(chord)
    elif len(note_list) == 5:
        for chord in base_chords:
            root_note = CHORD_FROM_3[chord]["root_note"]
            if (root_note + 10) % 12 in note_list and (root_note + 2) % 12 in note_list:
                chord += "9"
            elif (root_note + 11) % 12 in note_list and (root_note + 2) % 12 in note_list:
                chord += "M9"
            elif (root_note + 9) % 12 in note_list and (root_note + 2) % 12 in note_list:
                chord += "69"
            elif (root_note + 10) % 12 in note_list and (root_note + 3) % 12 in note_list:
                chord += "+9"
            elif (root_note + 10) % 12 in note_list and (root_note + 1) % 12 in note_list:
                chord += "-9"
            else:
                continue
            possibility_chords.append(chord)
    print(possibility_chords)


while True:
    msg = inport.receive()
    if msg.type == 'note_on':
        note_on_list.append(msg.note)
    if msg.type == 'note_off':
        note_on_list.remove(msg.note)
    if len(note_on_list) >= 3:
        notes_to_chord(note_on_list)
    outport.send(msg)
