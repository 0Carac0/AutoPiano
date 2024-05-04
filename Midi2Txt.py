import mido
from tkinter import filedialog
import sys

# Sélection du fichier midi
fichier = filedialog.askopenfilename(title="Sélectionner le fichier midi à convertir", filetypes=(("Fichier Midi", "*.mid"), ("All files", "*.*")))
if fichier == '':
    print("Aucun fichier n'a été sélectionné.")
    sys.exit()
else:
    print("Fichier sélectionné :", fichier)

# Lit le fichier midi et on extrait ses données
ls_noteInfo = mido.MidiFile(fichier)

#Ecrit la mémoire dans un fichier txt
with open(fichier[:fichier.rfind('.')] + '.txt', 'w') as f:
    # Rediriger la sortie standard vers le fichier
    sys.stdout = f
    print(ls_noteInfo)
    # Restaurer la sortie standard
    sys.stdout = sys.__stdout__

print('Midi convertit en txt')