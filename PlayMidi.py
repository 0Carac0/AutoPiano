import mido
import sys
from tkinter import filedialog

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
                print('Note on', message.note)
            else:
                print('Note off', message.note)

        case 'note_off':
            print('Note off', message.note)

        case 'control_change':
            if message.control == 64:
                if message.value == 0:
                    print('Pédal off')
                else:
                    print('Pédal on')