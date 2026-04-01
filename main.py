import random
import note_seq
from note_seq.protobuf import music_pb2

# --- Scale (D minor cinematic) ---
scale = [62, 64, 65, 67, 69, 70, 72]

# --- Chords ---
chords = [
    [62, 65, 69],   # Dm
    [70, 74, 77],   # Bb
    [67, 71, 74],   # Gm
    [69, 72, 76]    # A
]

STRINGS = 48
BRASS = 56
BASS = 33
DRUM = 9


def next_note(prev):
    step = random.choice([-2, -1, 1, 2, 3])
    new = prev + step
    return min(scale, key=lambda x: abs(x - new))


def generate_sequence(length=120):
    sequence = music_pb2.NoteSequence()
    sequence.tempos.add(qpm=120)

    current_pitch = random.choice(scale)
    time = 0.0
    chord_index = 0

    for i in range(length):

        # --- Section timing ---
        if i < 30:
            durations = [0.5, 1.0]
        elif i < 80:
            durations = [0.25, 0.5]
        else:
            durations = [0.25]

        duration = random.choice(durations)

        # --- Humanization ---
        time_offset = random.uniform(-0.02, 0.02)
        start = max(0, time + time_offset)
        end = start + duration

        # --- Chord ---
        chord = chords[chord_index % len(chords)]

        # --- Melody rests ---
        if random.random() < 0.15:
            time += duration
            continue

        # --- Melody note ---
        melody = sequence.notes.add()
        melody.pitch = current_pitch
        melody.start_time = start
        melody.end_time = end
        melody.velocity = random.randint(75, 110)
        melody.instrument = 0
        melody.program = STRINGS

        # --- Chord pads ---
        for note_pitch in chord:
            pad = sequence.notes.add()
            pad.pitch = note_pitch
            pad.start_time = start
            pad.end_time = end
            pad.velocity = 55
            pad.instrument = 3
            pad.program = STRINGS

        # --- Bass (root notes) ---
        root = chord[0]
        bass = sequence.notes.add()
        bass.pitch = root - 24
        bass.start_time = start
        bass.end_time = end + 0.2
        bass.velocity = 75
        bass.instrument = 1
        bass.program = BASS

        # --- Brass accents (climax) ---
        if i > 60 and i % 4 == 0:
            brass = sequence.notes.add()
            brass.pitch = current_pitch + 12
            brass.start_time = start
            brass.end_time = end
            brass.velocity = 120
            brass.instrument = 2
            brass.program = BRASS

        # --- Drum grid ---
        step = i % 4

        # Kick (downbeats)
        if step == 0:
            kick = sequence.notes.add()
            kick.pitch = 36
            kick.start_time = start
            kick.end_time = start + 0.1
            kick.velocity = 115
            kick.instrument = DRUM
            kick.is_drum = True

        # Snare (backbeat)
        if step == 2:
            snare = sequence.notes.add()
            snare.pitch = 38
            snare.start_time = start
            snare.end_time = start + 0.1
            snare.velocity = 105
            snare.instrument = DRUM
            snare.is_drum = True

        # Hi-hat (steady motion)
        hat = sequence.notes.add()
        hat.pitch = 42
        hat.start_time = start
        hat.end_time = start + 0.1
        hat.velocity = random.randint(50, 75)
        hat.instrument = DRUM
        hat.is_drum = True

        # Occasional extra percussion
        if random.random() < 0.1:
            tom = sequence.notes.add()
            tom.pitch = 45
            tom.start_time = start
            tom.end_time = start + 0.2
            tom.velocity = 90
            tom.instrument = DRUM
            tom.is_drum = True

        # --- Motion updates ---
        if random.random() < 0.7:
            current_pitch = next_note(current_pitch)

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
