import random
import note_seq
from note_seq.protobuf import music_pb2

# --- Epic adventure scale (D minor-ish cinematic) ---
scale = [62, 64, 65, 67, 69, 70, 72]  # D E F G A Bb C

# --- Chord progression (cinematic staple) ---
chords = [
    [62, 65, 69],   # Dm
    [70, 74, 77],   # Bb
    [67, 71, 74],   # Gm
    [69, 72, 76]    # A
]

def next_note(prev):
    step = random.choice([-2, -1, 1, 2, 3])  # bigger leaps = heroic feel
    new = prev + step
    return min(scale, key=lambda x: abs(x - new))

def generate_sequence(length=120):
    sequence = music_pb2.NoteSequence()
    sequence.tempos.add(qpm=120)

    # Instruments
    STRINGS = 48
    BRASS = 56
    BASS = 33
    DRUM = 9

    current_pitch = random.choice(scale)
    time = 0.0
    chord_index = 0

    for i in range(length):

        # --- Sections ---
        if i < 30:
            durations = [0.5, 1.0]     # intro
        elif i < 80:
            durations = [0.25, 0.5]    # build
        else:
            durations = [0.25]         # climax

        duration = random.choice(durations)

        # --- Current chord ---
        chord = chords[chord_index % len(chords)]

        # 🎻 STRINGS (melody)
        melody = sequence.notes.add()
        melody.pitch = current_pitch
        melody.start_time = time
        melody.end_time = time + duration
        melody.velocity = random.randint(80, 110)
        melody.instrument = 0
        melody.program = STRINGS

        # 🎼 CHORD PAD (Narnia feel)
        for note_pitch in chord:
            pad = sequence.notes.add()
            pad.pitch = note_pitch
            pad.start_time = time
            pad.end_time = time + duration * 2
            pad.velocity = 60
            pad.instrument = 3
            pad.program = STRINGS

        # 🎸 BASS (Pirates drive)
        if i % 2 == 0:
            bass = sequence.notes.add()
            bass.pitch = chord[0] - 12
            bass.start_time = time
            bass.end_time = time + duration * 2
            bass.velocity = 75
            bass.instrument = 1
            bass.program = BASS

        # 🎺 BRASS (Indiana hero hits)
        if i > 60 and i % 4 == 0:
            brass = sequence.notes.add()
            brass.pitch = current_pitch + 12
            brass.start_time = time
            brass.end_time = time + duration
            brass.velocity = 120
            brass.instrument = 2
            brass.program = BRASS

        # 🥁 DRUMS (cinematic rhythm)
        # Kick
        kick = sequence.notes.add()
        kick.pitch = 36
        kick.start_time = time
        kick.end_time = time + 0.1
        kick.velocity = 110
        kick.instrument = DRUM
        kick.is_drum = True

        # Snare (on off-beats)
        if i % 2 == 1:
            snare = sequence.notes.add()
            snare.pitch = 38
            snare.start_time = time
            snare.end_time = time + 0.1
            snare.velocity = 110
            snare.instrument = DRUM
            snare.is_drum = True

        # Hi-hat (motion)
        hat = sequence.notes.add()
        hat.pitch = 42
        hat.start_time = time
        hat.end_time = time + 0.1
        hat.velocity = 60
        hat.instrument = DRUM
        hat.is_drum = True

        # Move melody
        current_pitch = next_note(current_pitch)

        # Change chord every few steps
        if i % 8 == 0:
            chord_index += 1

        time += duration

    return sequence

def save_midi(sequence, filename="ai_output.mid"):
    note_seq.sequence_proto_to_midi_file(sequence, filename)
    print("Generated:", filename)

if __name__ == "__main__":
    seq = generate_sequence()
    save_midi(seq)
    input("Press Enter to exit...")
