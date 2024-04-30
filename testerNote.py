# Permet de tester une note en écrivant la note midi à jouer. Si on tape 0, cela testera la pédale.

from Pi_MCP23S17 import MCP23S17
from gpiozero import LED
from time import *

NB_CHIP = 8
NB_PIN = 16

# Allumage de l'alimentation pour les électro-aimants
try:
    Pedal = LED(21)
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

    while True:
        note = int(input("Entrer la note à jouer: "))
        if note == 0:
            Pedal.on()
            sleep(3)
            Pedal.off()
        else:
            ls_ChipBoard[(note -21)//NB_PIN].digitalWrite((note -21)%NB_PIN, MCP23S17.LEVEL_HIGH)
            print("num chip", (note -21)//NB_PIN)
            print("num pin", (note -21)%NB_PIN)
            sleep(0.05)
            ls_ChipBoard[(note -21)//NB_PIN].digitalWrite((note -21)%NB_PIN, MCP23S17.LEVEL_LOW)

except KeyboardInterrupt:
    Pedal.off()
    for i in range(NB_CHIP):
        ls_ChipBoard[i].open()
        for y in range(NB_PIN):
            ls_ChipBoard[i].digitalWrite(y, MCP23S17.LEVEL_LOW)
    print("Arrêt de l'utilisateur")