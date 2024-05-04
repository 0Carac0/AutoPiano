from gpiozero import LED
import threading
import time
import mido
import spidev

class NotesPedalManager():

    # 6 chips contrôlent les électro-aimants (2 ne sont pas utilisé)
    # chaque chip contrôle 16 électro-aimants (sauf le dernière qui contrôle seulement les dernière notes)

    # Enclanchement de l'alimentation
    Power_12V = LED(12)
    Power_12V.on()

    # Constantes
    NB_CHIP = 8             # Le nombre de total chip
    NB_PIN = 16             # Le nombre de pins utilisées par chip
    NB_NOTE = 85            # Le nombre de touche sur le piano
    OFFSET_PIN_MIDO = 21    # Le nombre de décalage dans la liste des notes

    def __init__(self):

        # Ouverture de la communication SPI vers les chips
        self._spi = spidev.SpiDev()
        self._spi.open(0, 0)
        self._spi.max_speed_hz = 10000000

        # Déclaration des chips IO qui controlent les électro-aimants
        self._ls_ChipBoard = [ChipBoard(self._spi, i) for i in range(NotesPedalManager.NB_CHIP)]
        
        # Déclaration d'un attribut pour dire sur qu'elle gpio est l'actionnement de la pédale
        self._Pedal = LED(21)
        self._Pedal.off()

    # Méthode pour Activer ou désactiver une note
    def playNote(self, note, value):
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
        if NotesPedalManager.OFFSET_PIN_MIDO <= note and note < NotesPedalManager.OFFSET_PIN_MIDO + NotesPedalManager.NB_NOTE:
            self._ls_ChipBoard[(note - NotesPedalManager.OFFSET_PIN_MIDO)//NotesPedalManager.NB_PIN].setOut((note - NotesPedalManager.OFFSET_PIN_MIDO)%NotesPedalManager.NB_PIN, value)
        else:
            print("[ERROR] Note out of range (",NotesPedalManager.OFFSET_PIN_MIDO,"-",NotesPedalManager.OFFSET_PIN_MIDO + NotesPedalManager.NB_NOTE - 1,") Note =", note)

    # Méthode pour Activer ou désactiver la pédale
    def PedalOn(self):
        self._Pedal.on()
    def PedalOff(self):
        self._Pedal.off()

    # Méthode pour désactiver la pédale et les pins des chips
    def disableAll(self):
        for i in range(NotesPedalManager.NB_CHIP):
            self._ls_ChipBoard[i].disableAllPins()
        self._Pedal.off()

class ChipBoard():

    # Numéros des registres
    MCP23S17_IODIRA = 0x00
    MCP23S17_IODIRB = 0x01
    MCP23S17_GPIOA = 0x12
    MCP23S17_GPIOB = 0x13
    MCP23S17_IOCON = 0x0A
    MCP23S17_CMD_WRITE = 0x40

    def __init__(self, spiCom, deviceID):

        self._spiCom = spiCom        # Objet de la communication SPI des chips
        self._deviceID = deviceID    # Numéro de la chip
        self._GPIOA = 0x00           # Mémoire de l'état des pines de sortie de la partie A
        self._GPIOB = 0x00           # Mémoire de l'état des pines de sortie de la partie B

        self.__writeRegister(ChipBoard.MCP23S17_IOCON, 0x08)

        # Set toutes les pins en sorties
        self.__writeRegister(ChipBoard.MCP23S17_IODIRA, 0x00)
        self.__writeRegister(ChipBoard.MCP23S17_IODIRB, 0x00)

        # Désactive toutes les pines
        self.disableAllPins()

    # Méthode pour set la valeur de la pin dans la mémoire
    def setOut(self, pin, value):

        if 0 <= pin and pin < NotesPedalManager.NB_PIN:
            # Regarde à quel partie (A ou B) appartient la pin et envoie la valeur sur la bonne adresse
            if pin < 8:
                if value:
                    self._GPIOA |= 1 << pin
                else:
                    self._GPIOA &= ~(1 << pin)
                self.__writeRegister(ChipBoard.MCP23S17_GPIOA, self._GPIOA)
            else:
                if value:
                    self._GPIOB |= 1 << (pin & 0x07)
                else:
                    self._GPIOB &= ~(1 << (pin & 0x07))
                self.__writeRegister(ChipBoard.MCP23S17_GPIOB, self._GPIOB)
        else:
            print("[ERROR] Pin out of range ( 0 -",NotesPedalManager.NB_PIN,") pin =", pin)

    # Méthode pour ecrire une valeur dans un registe du chip
    def __writeRegister(self, register, value):
        self._spiCom.xfer2([ChipBoard.MCP23S17_CMD_WRITE | ((self._deviceID) << 1), register, value])

    # Méthode pour désactiver toutes les pins
    def disableAllPins(self):
        self.writeRegister(ChipBoard.MCP23S17_GPIOA, 0x00)
        self.writeRegister(ChipBoard.MCP23S17_GPIOB, 0x00)
        self._GPIOA     = 0
        self._GPIOB     = 0

# Définition de la classe qui gère l'extration des notes et l'appuie des touches
class PianoManager():

    def __init__(self):

        self._isReady = False                                                            # Indique si le thread est pret à lancer une musique
        self._threadpianoManagerEvent = threading.Event()                               # Créer un event pour relancer le thread de la musique
        self._threadpianoManager = threading.Thread(target=self.execute, daemon=True)   # Création du thread pour pianoManager
        self._threadpianoManager.start()                                                 # Lance le thread PianoManager
        self._notesPedalManager = NotesPedalManager()                                    # Objet qui gère les notes et la pédal

    # Méthode qui lance la musique
    def play(self, PathMidi):

        # Verification que si une musique est déjà lancé, il l'arrête avant dans lancer une autre
        self._threadpianoManagerEvent.clear()
        self.__WaitIsReady()
        self._pathMidi = PathMidi               # Transfère l'argument vers l'attribut
        self._start_time = time.time()          # Enregistre le temps pour savoir quand la musique à été lancée
        self._threadpianoManagerEvent.set()    # Lance le thread pour jouer la musique

    def execute(self):

        while True:

            # Attend qu'ont le lance
            self._notesPedalManager.disableAll()
            self._threadpianoManagerEvent.clear()
            self._isReady = True
            self._threadpianoManagerEvent.wait()
            self._isReady = False

            # Lit le fichier midi et extrait ses données
            mid = mido.MidiFile(self._pathMidi)

            # Lancement de la musique
            for message in mid.play():

                # S'il la musique est arrêté on arrête
                if not self._threadpianoManagerEvent.is_set():
                    break

                match message.type:
                    # Si le message du fichier midi est du type "note_on"
                    case 'note_on':
                        if message.velocity == 0:
                            self._notesPedalManager.playNote(message.note, False)
                        else:
                            self._notesPedalManager.playNote(message.note,  True)

                    # Si le message du fichier midi est du type "note_off"
                    case 'note_off':
                        self._notesPedalManager.playNote(message.note,  False)

                    # Si le message du fichier midi est du type "control_change",
                    # le "control_change" est un message pour tout ce qui est autre qu'une note.
                    case 'control_change':
                        # Dans notre cas, nous cherchons un appui de la pédale.
                        # Donc on vérifie si le message "control_change" est égal à 64 (message pour pédale)
                        if message.control == 64:
                            if message.value == 0:
                                self._notesPedalManager.PedalOff()
                            else:
                                self._notesPedalManager.PedalOn()

    # Attand que le player soit arrêté
    def __WaitIsReady(self):
        while not self._isReady:
            time.sleep(0.05)

    # Méthode pour arreter la musique
    def stop(self):
        self._threadpianoManagerEvent.clear()
        self.__WaitIsReady()

    # Méthode qui permet de mettre en pause le programme jusqu'à que la musique s'arrête
    def threadJoin(self):
        self.__WaitIsReady()
    
    # Renvoie depuis combien de temps la musique se joue.
    @property
    def elapsedTimeMusic(self):
        elapsed_time = int(time.time() - self._start_time)
        return elapsed_time
    
    # Renvoie le temps total du fichier midi
    def totalTimeMusic(self, pathMidi):
        mid = mido.MidiFile(pathMidi)
        return int(mid.length)

    # Renvoie Vrais si la musique est arrêté
    @property
    def isStoped(self):
        return self._isReady
    
    # Renvoie quel musique il est en train de jouer
    @property
    def whatPlay(self):
        if self._isReady:
            return ''
        else:
            return self._pathMidi

