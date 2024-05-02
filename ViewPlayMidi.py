import mido
import sys
from tkinter import filedialog

try:
    # Sélection du fichier midi
    fichier = filedialog.askopenfilename(title="Sélectionner le fichier midi à convertir", filetypes=(("Fichier Midi", "*.mid"), ("All files", "*.*")))
    if fichier == '':
        print("Aucun fichier n'a été sélectionné.")
        sys.exit()
    else:
        print("Fichier sélectionné :", fichier)

    # Lit le fichier midi et on extrait ses données
    mid = mido.MidiFile(fichier)

    # Lancement de la musique
    for message in mid.play():
        match message.type:

            case 'note_on':
                if not message.velocity == 0:
                    print(round(message.time, 2), 'Note on', message.note)
                else:
                    print(round(message.time, 2), 'Note off', message.note)

            case 'note_off':
                print(round(message.time, 2), 'Note off', message.note)

            case 'control_change':
                if message.control == 64:
                    if message.value == 0:
                        print(round(message.time, 2), 'Pédal off')
                    else:
                        print(round(message.time, 2), 'Pédal on')
                        
except KeyboardInterrupt:
    print("Arrêt de l'utilisateur")