from gpiozero import LED
import threading
import time
import mido
import spidev

class NotesPedalManager():

    # 6 chips contrôlent les électro-aimants (2 ne sont pas utilisé)
    # chaque chip contrôle 16 électro-aimants (sauf le dernière qui contrôle seulement les dernière notes)  

    # Constantes
    NB_CHIP = 8             # Le nombre de total chip
    NB_PIN = 16             # Le nombre de pins utilisées par chip
    NB_NOTE = 85            # Le nombre de touche sur le piano
    OFFSET_PIN_MIDO = 21    # Le nombre de décalage dans la liste des notes

    def __init__(self):

        # Ouverture de la communication SPI vers les chips
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.ce)
        self.spi.max_speed_hz = 10000000

        # Déclaration des chips IO qui controlent les électro-aimants
        self.ls_ChipBoard = [ChipBoard(self.spi, i) for i in range(NotesPedalManager.NB_CHIP)]
        
        # Déclaration d'un attribut pour dire sur qu'elle gpio est l'actionnement de la pédale
        self.Pedal = LED(21)
        self.Pedal.off

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
            self.ls_ChipBoard[(note - NotesPedalManager.OFFSET_PIN_MIDO)//NotesPedalManager.NB_PIN].setPin((note - NotesPedalManager.OFFSET_PIN_MIDO)%NotesPedalManager.NB_PIN, value)
        else:
            print("[ERREUR] Note hors plage (",NotesPedalManager.OFFSET_PIN_MIDO,"-",NotesPedalManager.OFFSET_PIN_MIDO + NotesPedalManager.NB_NOTE - 1,") Note =", note)

    # Méthode pour Activer ou désactiver la pédale
    def playPedal(self, value):
        if value:
            self.Pedal.on
        else:
            self.Pedal.off

    # Méthode pour désactiver la pédale et les pins
    def disableAll(self):
        for i in range(NotesPedalManager.NB_CHIP):
            self.ls_ChipBoard[i].disableAllPin()
        self.Pedal.off

class ChipBoard():

    # Numéros des registres
    MCP23S17_IODIRA = 0x00
    MCP23S17_IODIRB = 0x01
    MCP23S17_GPIOA = 0x12
    MCP23S17_GPIOB = 0x13
    MCP23S17_IOCON = 0x0A
    MCP23S17_CMD_WRITE = 0x40

    def __init__(self, spiCom, deviceID):

        self.spiCom = spiCom        # Objet de la communication SPI des chips
        self.deviceID = deviceID    # Numéro de la chip
        self.GPIOA = 0x00           # Mémoire de l'état des pines de sortie de la partie A
        self.GPIOB = 0x00           # Mémoire de l'état des pines de sortie de la partie B

        self.writeRegister(ChipBoard.MCP23S17_IOCON, 0x08)

        # Set toutes les pins en sorties
        self.writeRegister(ChipBoard.MCP23S17_IODIRA, 0x00)
        self.writeRegister(ChipBoard.MCP23S17_IODIRB, 0x00)

        # Désactive toutes les pines
        self.disableAllPin()

    # Méthode pour set la valeur de la pin
    def setPin(self, pin, value):

        if 0 <= pin and pin < NotesPedalManager.NB_PIN:
            # Regarde à quel partie (A ou B) appartient la pin et envoie la valeur sur la bonne adresse
            if pin < 8:
                if value:
                    self.GPIOA |= 1 << pin
                else:
                    self.GPIOA &= ~(1 << pin)
                self.writeRegister(ChipBoard.MCP23S17_GPIOA, self.GPIOA)
            else:
                if value:
                    self.GPIOB |= 1 << (pin & 0x07)
                else:
                    self.GPIOB &= ~(1 << (pin & 0x07))
                self.writeRegister(ChipBoard.MCP23S17_GPIOB, self.GPIOB)
        else:
            print("[ERREUR] Pin out of range ( 0 -",NotesPedalManager.NB_PIN,") pin =", pin)

    # Méthode pour ecrire une valeur dans un registe du chip
    def writeRegister(self, register, value):
        self.spiCom.xfer2([ChipBoard.MCP23S17_CMD_WRITE | ((self.deviceID) << 1), register, value])

    # Méthode pour désactiver toutes les pins
    def disableAllPin(self):
        self.writeRegister(ChipBoard.MCP23S17_GPIOA, 0x00)
        self.writeRegister(ChipBoard.MCP23S17_GPIOB, 0x00)

# Définition de la classe qui gère l'extration des notes et l'appuie des touches
class PianoManager():

    def __init__(self):
        self.isPlaying = False                          # Permettrea de dire si une musique est en train d'être jouer et d'arreter le thread
        self.theadPianoIsInExecution = False            # Permettrea de dire si le thread du piano est toujours en execution
        self.threadpianoManager = threading.Thread(target=self.execute) # Création du thread pour pianoManager
        self.notesPedalManager = NotesPedalManager()    # Objet qui gère les notes et la pédal

    # Méthode qui lance la musique
    def play(self, PathMidi):

        # Verification que si une musique est déjà lancé, il l'arrête avant dans lancer une autre
        while self.theadPianoIsInExecution:
            self.isPlaying = False

        self.pathMidi = PathMidi        # Transfère l'argument vers l'attribut
        self.start_time = time.time()   # Enregistre le temps pour savoir quand la musique à été lancée
        self.threadpianoManager.start() # Lance le thread PianoManager

    def execute(self):

        self.theadPianoIsInExecution = True
        self.isPlaying = True

        # Lit le fichier midi et extrait ses données
        mid = mido.MidiFile(self.pathMidi)

        # Lancement de la musique
        for message in mid.play():

            # Si isPlaying est set à False, la musique s'arrête
            if not self.isPlaying:
                break

            match message.type:
                # Si le message du fichier midi est du type "note_on"
                case 'note_on':
                    self.notesPedalManager.playNote(message.note, True)

                # Si le message du fichier midi est du type "note_off"
                case 'note_off':
                    self.notesPedalManager.playNote(message.note, False)

                # Si le message du fichier midi est du type "control_change",
                # le "control_change" est un message pour tout ce qui est autre qu'une note.
                case 'control_change':
                    # Dans notre cas, nous cherchons un appui de la pédale.
                    # Donc on vérifie si le message "control_change" est égal à 64 (message pour pédale)
                    if message.control == 64:
                        if message.value == 0:
                            self.notesPedalManager.playPedal(False)
                        else:
                            self.notesPedalManager.playPedal(True)

            self.theadPianoIsInExecution = False
            self.isPlaying = False

        # Lorsque la musique est arretée ou terminée, désactive la pédal et tout les touches.
        self.notesPedalManager.disableAll()
        self.isPlaying = False

    # Méthode pour arreter la musique
    def stop(self):
        self.isPlaying = False
    
    # Méthode qui permet de mettre en pause le programme jusqu'à que la musique s'arrête
    def threadJoin(self):
        self.threadpianoManager.join()
    
    # Renvoie depuis combien de temps la musique se joue.
    @property
    def elapsedTimeMusic(self):
        elapsed_time = int(time.time() - self.start_time)
        return elapsed_time
    
    # Renvoie le temps total du fichier midi
    def totalTimeMusic(self, pathMidi):
        mid = mido.MidiFile(pathMidi)
        return int(mid.length)

    # Renvoie si la musique est en train d'être jouée
    @property
    def isPlaying(self):
        return self.isPlaying