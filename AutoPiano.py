import mido 

mid = mido.MidiFile('Musique midi/C418 - Aria Math.mid', clip=True)

for msg in mid:
    if msg.type == 'program_change' and msg.program == 0:
        print(msg)