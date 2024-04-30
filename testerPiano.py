from Pi_MCP23S17 import MCP23S17
from gpiozero import LED
from time import *

NB_CHIP = 8
NB_PIN = 16

# Allumage de l'alimentation pour les électro-aimants
try:
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

    for i in range(NB_CHIP):
        for y in range(NB_PIN):
            ls_ChipBoard[i].digitalWrite(y, MCP23S17.LEVEL_HIGH)
            sleep(0.05)
            ls_ChipBoard[i].digitalWrite(y, MCP23S17.LEVEL_LOW)
            sleep(0.5)

except KeyboardInterrupt:
    Pedal.off()
    for i in range(NB_CHIP):
        ls_ChipBoard[i].open()
        for y in range(NB_PIN):
            ls_ChipBoard[i].digitalWrite(y, MCP23S17.LEVEL_LOW)
    print("Arrêt de l'utilisateur")