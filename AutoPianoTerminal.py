# Ceci est le code qui permet de simplement lancer une musique sur le piano via une interface terminal en local

from alive_progress import alive_bar
from tkinter import filedialog
from PianoManager import *
import os
import time

try:
    # Importation de l'objet qui gère le piano
    pianoManager = PianoManager()
    
    # Sélection du fichier midi en ouvrant un exporateur de fichier.
    fichier = filedialog.askopenfilename(title="Sélectionner le fichier midi à convertir", filetypes=(("Fichier Midi", "*.mid"), ("All files", "*.*")), initialdir="/home/pi/Desktop/AutoPiano/Musique midi")
    if fichier:
        nom_fichier = os.path.basename(fichier)
        print("Lancement de la musique :", nom_fichier)

        # Lancement de la muisique
        pianoManager.play(fichier)

        # Affiche une barre de progression de la musique dans le terminal
        with alive_bar(pianoManager.totalTimeMusic(fichier), title='Playing', length=20, bar='smooth', spinner="notes2") as bar:
            while pianoManager.IsPlaying:
                time.sleep(1)
                bar()
        pianoManager.threadJoin()

    else:
        # Si aucun fichier n'est sélectionné, le programme s'arrête.
        print("Aucun fichier n'a été sélectionné.")

except KeyboardInterrupt:
    print("\nArrêt de l'utilisateur")

# Arret du thread dans le piano manager
pianoManager.disableNotesPedal()