import mido
import rtmidi
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
PITDH_LIST = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

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


def notes_to_code(note_list):
    note_list = convert_to_base_note(note_list)
    if len(note_list) < 3:
        return
    print(note_list)
    sorted_note_list = sorted(note_list)
    diff_1 = sorted_note_list[1] - sorted_note_list[0]
    diff_2 = sorted_note_list[2] - sorted_note_list[1]
    if diff_1 == 4 and diff_2 == 3:
        root = sorted_note_list[0]
        scale = ""
    elif diff_1 == 3 and diff_2 == 5:
        root = sorted_note_list[2]
        scale = ""
    elif diff_1 == 5 and diff_2 == 4:
        root = sorted_note_list[1]
        scale = ""
    elif diff_1 == 3 and diff_2 == 4:
        root = sorted_note_list[0]
        scale = "m"
    elif diff_1 == 4 and diff_2 == 5:
        root = sorted_note_list[2]
        scale = "m"
    elif diff_1 == 5 and diff_2 == 3:
        root = sorted_note_list[1]
        scale = "m"
    else:
        print("????")
        return
    print(note_to_pitch(root) + scale)


while True:
    msg = inport.receive()
    if msg.type == 'note_on':
        note_on_list.append(msg.note)
    if msg.type == 'note_off':
        note_on_list.remove(msg.note)
    if len(note_on_list) >= 3:
        notes_to_code(note_on_list)
    outport.send(msg)

