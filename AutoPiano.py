from Pi_MCP23S17 import MCP23S17
from gpiozero import LED
from time import *
from tkinter import filedialog
import mido
import sys

NB_CHIP = 8
NB_PIN = 16

try:

    # Allumage de l'alimentation pour les électro-aimants
    Power12V = LED(12)
    Power12V.on()
    sleep(0.4)

    # Déclaration des pins du MCP pour relier le programme aux sorties physiques du MCP vers les électro-aimants
    ls_ChipBoard = [MCP23S17(ce=0x00,  deviceID = i ) for i in range(NB_CHIP)]
    for i in range(NB_CHIP):
        ls_ChipBoard[i].open()
        for y in range(NB_PIN):
            ls_ChipBoard[i].setDirection(y, ls_ChipBoard[i].DIR_OUTPUT)
            ls_ChipBoard[i].digitalWrite(y, MCP23S17.LEVEL_LOW)

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
                    ls_ChipBoard[(message.note -21)//16].digitalWrite((message.note -21)%16, MCP23S17.LEVEL_HIGH)
                else:
                    ls_ChipBoard[(message.note -21)//16].digitalWrite((message.note -21)%16, MCP23S17.LEVEL_LOW)

            case 'note_off':
                ls_ChipBoard[(message.note -21)//16].digitalWrite((message.note -21)%16, MCP23S17.LEVEL_LOW)

            case 'control_change':
                if message.control == 64:
                    if message.value == 0:
                        print('Pédal off')
                    else:
                        print('Pédal on')
                        
except KeyboardInterrupt:
    for i in range(NB_CHIP):
        ls_ChipBoard[i].open()
        for y in range(NB_PIN):
            ls_ChipBoard[i].digitalWrite(y, MCP23S17.LEVEL_LOW)
    print("STOOOOOOOOOOOP")


