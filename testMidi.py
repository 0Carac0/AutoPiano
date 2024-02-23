import mido
import sys

def ConvertDoubleTrack(NameMusic):
    # Ouvrir un fichier en mode écriture
    with open('Musique txt/' + NameMusic + '.txt', 'w') as f:
        # Rediriger la sortie standard vers le fichier
        sys.stdout = f
    
        ls_Track = mido.MidiFile('Musique midi/' + NameMusic + '.mid', clip=True)

        print(ls_Track)
    
        # Restaurer la sortie standard
        sys.stdout = sys.__stdout__

def extract_bpm(NameMusic):
    mid = mido.MidiFile('Musique midi/' + NameMusic + '.mid')
    #ticks_per_beat = mid.ticks_per_beat
    
    for track in mid.tracks:
        for msg in track:
            # Recherche des événements de changement de tempo (meta messages)
            if msg.type == 'set_tempo':
                # Calcul du BPM à partir de l'événement de changement de tempo
                bpm = mido.tempo2bpm(msg.tempo)

                return bpm
            
def extract_TimeTick(NameMusic):
    mid = mido.MidiFile('Musique midi/' + NameMusic + '.mid')
    ticks_per_beat = mid.ticks_per_beat
    
    for track in mid.tracks:
        for msg in track:
            # Recherche des événements de changement de tempo (meta messages)
            if msg.type == 'set_tempo':
                # Calcul du BPM à partir de l'événement de changement de tempo
                bpm = mido.tempo2bpm(msg.tempo)

    return 60000 / (bpm * ticks_per_beat)

NameMusicfile = "Amélie Poulain - Comptine Dun autre été"

"""print("BPM de la musique MIDI:", int(extract_bpm(NameMusicfile)))

print("Temps d'un tick de la musique MIDI:", extract_TimeTick(NameMusicfile), '[ms]')"""


ConvertDoubleTrack(NameMusicfile)