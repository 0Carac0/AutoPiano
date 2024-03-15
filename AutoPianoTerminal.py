from alive_progress import alive_bar
from tkinter import filedialog
from PianoManager import *
import sys
import os
import time

try:
    pianoManager = PianoManager()
    
    # Sélection du fichier midi en ouvrant une interface qui le demande. Si aucun fichier sélectionné, le programme s'arrête.
    fichier = filedialog.askopenfilename(title="Sélectionner le fichier midi à convertir", filetypes=(("Fichier Midi", "*.mid"), ("All files", "*.*")), initialdir="/home/pi/Desktop/AutoPiano/Musique midi")
    if fichier:
        nom_fichier = os.path.basename(fichier)
        print("Lancement de la musique :", nom_fichier)
    else:
        print("Aucun fichier n'a été sélectionné.")
        pianoManager.stop()
        sys.exit()

    pianoManager.play(fichier)
    with alive_bar(pianoManager.totalTimeMusic(fichier), title='Playing', length=20, bar='smooth', spinner="notes2") as bar:
        while pianoManager.IsPlaying:
                time.sleep(1)
                bar()
    pianoManager.threadJoin()
    
except KeyboardInterrupt:
    print("\nArrêt de l'utilisateur")
    pass
pianoManager.stop()