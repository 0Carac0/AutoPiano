'''
POUR TESTER MANUELLEMENT LES NOTES :
 1) Ouvrir le Shell
 2) Importer le programme
 3) Allumer l'installation avec 'allumage()'
 4) Lancer le programme avec 'SetBoard(<vitesse>)'
 5) Éviter d'interromptre le cycle (si c'est absolument nécessaire, appuyer sur Ctrl+z puis
couper le courant pour épargner les électro-aimants. Ensuite, relancer le programme sans
entrer de valeur de temps, afin de reset les touches enfoncée.)
'''

'''
Importation de bibliothèques et commandes :
- LED permet d'activer/désactiver l'alimentation
- MCP23S17 initialise l'objet du même nom
- time permet de gérer des durées de temps
'''

from gpiozero import LED
import random
from Pi_MCP23S17 import MCP23S17
'''import subprocess
import sqlite3'''
from time import *



'''
Fonctions qui allument et éteignent l'alimentation.
On ne peut jouer des notes que dans ce laps de temps.
'''

led = LED(12)

def allumage():
    led.on()
    sleep(0.4)
    print("\nInstallation allumée\n")

def arret():
    led.off()
    print("\nInstallation éteinte\n")

'''
Allume puis éteint toutes les notes à tour de rôle
'''

def SetBoard(rythme = 0, seulHautes = "n", rep = "n"):
    # calcule à partir de quelle note jouer, si l'utilisateur ne veut que des notes hautes
    if rep == "y" :
        y = 5
    else :
        y = 1
    # Déclaration des pins du MCP pour relier le programme aux sorties physiques du MCP vers les électro-aimants
    mcp = []
    mcp.append(MCP23S17(ce=0x00, deviceID=0x00)) # chip A (ce =0x00 pour ce=0x01 si on change de chip sur les cartes de 128GPIO)
    mcp.append(MCP23S17(ce=0x00, deviceID=0x01)) # chip B ()
    mcp.append(MCP23S17(ce=0x00, deviceID=0x02)) # chip C
    mcp.append(MCP23S17(ce=0x00, deviceID=0x03)) # chip D
    mcp.append(MCP23S17(ce=0x00, deviceID=0x04)) # chip E
    mcp.append(MCP23S17(ce=0x00, deviceID=0x05)) # chip F
    mcp.append(MCP23S17(ce=0x00, deviceID=0x06)) # chip G
    mcp.append(MCP23S17(ce=0x00, deviceID=0x07)) # chip H

    N = len(mcp)

    for I in range(N):
        mcp[I].open()
    for nb in range (y) :
        for I in range(N) :
            for x in range(16):
                # empêche les notes basses de jouer si l'utilisateur ne veut que la partie haute
                if seulHautes == "y" and (I < 3 or (I < 2 and x >= 6)) :
                    temps = 0
                else :
                    temps = rythme
                if I <= 4 or (I == 5 and x <= 5) :
                    # génère les sorties (x = n° de touche, mcp[I] = octave)
                    mcp[I].setDirection(x, mcp[I].DIR_OUTPUT)
                    # active la note
                    mcp[I].digitalWrite(x, MCP23S17.LEVEL_HIGH)
                    # laisse la note jouer (si rythme < ~0.05, n'a pas le temps de jouer correctement)
                    sleep(temps)
                # désactive la note
                mcp[I].digitalWrite(x, MCP23S17.LEVEL_LOW)
    return N, mcp
        
def Notes_Pin(nNotes, selNote):
 
    note,octaves,piano = ['C','C#','D','D#',
                          'E','F','F#', 'G',
                          'G#', 'A','A#','B'],\
                          [0,1,2,3,4,5,6],[]
 
    qPin, bank, port, pin, pins = [],['A','B','C','D','E','F','G','H'],\
                                [1,2],\
                                [1,2,3,4,5,6,7,8],[]
 
 
    # ecriture de chaque note dans le format NOTEOCTAVE
    for j in range(len(octaves)):
        for i in range(len(note)):
            piano.append(note[i] + str(octaves[j]))

    
                
    # ecriture de tous les pins possibles dans le format BANKPORTPIN
    for x in range(len(bank)):
        for y in range(len(port)):
            for z in range(len(pin)):
                pins.append(bank[x] + str(port[y]) + str(pin[z]))
 
    for m in range(len(pins)):
        if m == piano.index(piano[selNote]):
            qPin.append(m) 

 
    return qPin