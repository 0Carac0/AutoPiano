from Pi_MCP23S17 import MCP23S17
from gpiozero import LED
from time import *
from tkinter import filedialog
import mido
import sys
import time
import threading

NB_CHIP = 8
NB_PIN = 16
Pedal = LED(21)

# Définition de la classe qui gère la pédale
class PedalManager:
    def __init__(self):
        # Création d'une liste qui fera office de "File d'attente" des actions de la pédale
        self.ls_ActionPedal = []
        
    def On(self):
        # Rajoutera un "True" à notre file d'attente quand on recevra une demande pour appuyer sur la pédale
        self.ls_ActionPedal.append(True)

    def Off(self):
        # Rajoutera un "False" à notre file d'attente quand on recevra une demande pour relacher la pédale
        self.ls_ActionPedal.append(False)
        
    def Execute(self):
        while True:
            # Si notre file d'attente n'est pas vide:
            if not len(self.ls_ActionPedal) == 0:
                # Si le premier élément de la file d'attente est un "True" alors, on appuie sur la pédale, puis on temporise et on supprime cet élément de la file.
                if self.ls_ActionPedal[0]:
                    Pedal.on()
                    time.sleep(0.2)
                    del self.ls_ActionPedal[0]
                    print('Pédal on')
                # Si le premier élément de la file d'attente est autre chose que "True" alors, on relâche la pédale, puis on temporise et on supprime cet élément de la file.
                else:
                    Pedal.off()
                    time.sleep(0.2)
                    del self.ls_ActionPedal[0]
                    print('Pédal off')

try:

    # Allumage de l'alimentation pour les électro-aimants
    Power12V = LED(12)
    Power12V.on()

    # Déclaration des pins du MCP pour relier le programme aux sorties physiques du MCP vers les électro-aimants
    ls_ChipBoard = [MCP23S17(ce=0x00,  deviceID = i ) for i in range(NB_CHIP)]
    for i in range(NB_CHIP):
        ls_ChipBoard[i].open()
        for y in range(NB_PIN):
            ls_ChipBoard[i].setDirection(y, ls_ChipBoard[i].DIR_OUTPUT)
            ls_ChipBoard[i].digitalWrite(y, MCP23S17.LEVEL_LOW)         
            
    # Création de l'objet qui gère la pédale
    pedalManager = PedalManager()
    # Lancement de l'objet en parallèle du programme pour éviter que les notes soient arrêtées par les temporisations
    thread = threading.Thread(target=pedalManager.Execute)
    thread.start()

    # Sélection du fichier midi en ouvrant une interface qui le demande. Si aucun fichier sélectionné, le programme s'arrête.
    fichier = filedialog.askopenfilename(title="Sélectionner le fichier midi à convertir", filetypes=(("Fichier Midi", "*.mid"), ("All files", "*.*")))
    if fichier == '':
        print("Aucun fichier n'a été sélectionné.")
        sys.exit()
    else:
        print("Fichier sélectionné :", fichier)

    # Lit le fichier midi et extrait ses données
    mid = mido.MidiFile(fichier)

    # Lancement de la musique
    for message in mid.play():
        match message.type:

            # Si le message du fichier midi est du type "note_on",
            case 'note_on':
                # Vérifie si la vélocité de la note n'est pas égale à 0. Car certains messages "note_on" ont une vélocité à 0, ce qui veut dire que la note doit être relâchée et non appuyée.
                if not message.velocity == 0:
                    # 6 chips contrôlent les électro-aimants (2 ne sont pas utilisé), chaque chip contrôle 16 électro-aimants (sauf le dernière qui contrôle seulement les dernière notes)
                    
                    '''
                    Pour bien comprendre cette partie, prenons comme exemple la note midi 52.
                    On a besoin de deux info pour activer le bon électro-aimant qui jouera la note 52:
                    - Sur quelle chip est l'électro-aimant (ls_ChipBoard)
                    - Sur quelle pin du chip est l'électro-aimant (digitalWrite)
                    
                    Pour la première info, on la calcule en commençant par soustraire 21 à notre nombre.
                    Parce que la librairie mido extrait les notes midi qui vont de 21 à 108. Mais la numérotation pour controler les électro-aimants est différente.
                    Cela nous permet tout simplement d'aligner la numérotation midi à la numérotation des électro-aimants.
                    Donc, dans notre cas 52-21=31.
                    Puis on fait une division entière par 16. (car 16 pins utilisées par chip)
                    31//16=1
                    Cela nous dit que notre note à jouer est sur la deuxième chip (la numérotation des chips commence par 0).

                    Pour trouver la deuxième info on commence comme pour la première, par soustraire par 21.
                    52-21=31
                    Puis cette fois-ci, on fait le modulo de notre note.
                    31%16=15
                    Cela nous dit que notre note est sur la pin 16 de notre chip (la numérotation des pins commence par 0).

                    Il ne nous reste plus qu'à dire si l'on veut allumer la pin (LEVEL_HIGH) ou l'éteindre (LEVEL_LOW).
                    '''
                    ls_ChipBoard[(message.note -21)//16].digitalWrite((message.note -21)%16, MCP23S17.LEVEL_HIGH)
                else:
                    ls_ChipBoard[(message.note -21)//16].digitalWrite((message.note -21)%16, MCP23S17.LEVEL_LOW)

            case 'note_off':
                ls_ChipBoard[(message.note -21)//16].digitalWrite((message.note -21)%16, MCP23S17.LEVEL_LOW)

            # Si le message du fichier midi est du type "control_change",
            # le "control_change" est un message pour tout ce qui est autre qu'une note.
            case 'control_change':
                # Dans notre cas, nous cherchons un appui de la pédale.
                # Donc on vérifie si le message "control_change" est égal à 64 (message pour pédale)
                if message.control == 64:
                    if message.value == 0:
                        pedalManager.Off()
                    else:
                        pedalManager.On()

# Si l'utilisateur arrête le programme, on reset tout les pins pour éviter que les électro-aimants s'actionnent au redémarrage
except KeyboardInterrupt:
    Pedal.off()
    for i in range(NB_CHIP):
        ls_ChipBoard[i].open()
        for y in range(NB_PIN):
            ls_ChipBoard[i].digitalWrite(y, MCP23S17.LEVEL_LOW)
    print("Arrêt de l'utilisateur")