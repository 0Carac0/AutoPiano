# Programme pour tester toutes les notes à la suite

import time
from PianoManager import NotesPedalManager

notesPedalManager = NotesPedalManager()

try:
    for i in range(21, 96):
        notesPedalManager.playNote(i, True)
        time.sleep(0.1)
        notesPedalManager.playNote(i, False)
        time.sleep(0.3)
    notesPedalManager.disableAll()

except KeyboardInterrupt:
    notesPedalManager.disableAll()
    print("Arrêt de l'utilisateur")
