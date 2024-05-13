# Ce programme permet de tester une note en écrivant la note midi à jouer dans le terminal.
# Si on tape 0, cela testera la pédale et les touches sont situé entre 21 et 96.

import time
from StructuralFunction.PianoManager import NotesPedalManager

notesPedalManager = NotesPedalManager()

try:
    while True:
        note = int(input("Entrer la note à jouer: "))
        if note == 0:
            notesPedalManager.playPedal(True)
            time.sleep(3)
            notesPedalManager.playPedal(False)
        else:
            notesPedalManager.playNote(note, True)
            print("num chip", (note -21)//16)
            print("num pin", (note -21)%16)
            time.sleep(0.05)
            notesPedalManager.playNote(note, False)

except KeyboardInterrupt:
    notesPedalManager.disableAll()
    print("Arrêt de l'utilisateur")