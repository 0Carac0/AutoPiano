from Pi_MCP23S17 import MCP23S17
from gpiozero import LED
import threading
import time
import mido

# Définition de la classe qui gère la pédale
class PedalManager:
    def __init__(self):
        self.ls_ActionPedal = []    # Création d'une liste qui fera office de "File d'attente" des actions de la pédale.
        self.Pedal = LED(21)        # Création d'un attribut pour dire sur qu'elle gpio est l'actionnement de la pédale
        self.IsRunning = True       # Création d'un attribut qui permettra d'arrêter le thread
        self.threadPedalManager = threading.Thread(target= self.execute)    # Création du thread pour la pédal
        
    def on(self):
        # Rajoutera un "True" à notre file d'attente quand on recevra une demande pour appuyer sur la pédale
        self.ls_ActionPedal.append(True)

    def off(self):
        # Rajoutera un "False" à notre file d'attente quand on recevra une demande pour relacher la pédale
        self.ls_ActionPedal.append(False)

    def start(self):
        # Lance le thread pedalManager
        self.threadPedalManager.start()

    def close(self):
        # désactive la pédale puis arrête la boucle dans execute pour arreter le thread.
        self.Pedal.off()
        self.IsRunning = False
        
    def execute(self):
        # La boucle while s'arretera si le IsRunnung est égal à False
        while self.IsRunning:
            # Si notre file d'attente n'est pas vide:
            if not len(self.ls_ActionPedal) == 0:
                # Si le premier élément de la file d'attente est un "True" alors, on appuie sur la pédale, puis on temporise et on supprime cet élément de la file.
                if self.ls_ActionPedal[0]:
                    self.Pedal.on()
                    time.sleep(0.2)
                    del self.ls_ActionPedal[0]
                # Si le premier élément de la file d'attente est autre chose que "True" alors, on relâche la pédale, puis on temporise et on supprime cet élément de la file.
                else:
                    self.Pedal.off()
                    time.sleep(0.2)
                    del self.ls_ActionPedal[0]

# Définition de la classe qui gère l'extration des notes et l'appuie des touches
class PianoManager():

    NB_CHIP = 8 # Le nombre de total chip
    NB_PIN = 16 # Le nombre de pins utilisée par chip

    def __init__(self):
        # Allumage de l'alimentation pour les électro-aimants
        self.Power12V = LED(12)
        self.Power12V.on()
        time.sleep(1)                       # Laisse le temps pour que l'alimentation démarre
        self.IsPlaying = False              # Permettrea de dire si une musique est en train d'être jouer et de l'arreter
        self.pedalManager = PedalManager()  # Création de l'objet qui gère la pédale
        self.threadpianoManager = threading.Thread(target=self.execute) # Création du thread pour pianoManager

        # Déclaration des pins du MCP pour relier le programme aux sorties physiques du MCP vers les électro-aimants
        self.ls_ChipBoard = [MCP23S17(ce=0x00,  deviceID = i ) for i in range(PianoManager.NB_CHIP)]
        for i in range(PianoManager.NB_CHIP):
            self.ls_ChipBoard[i].open()
            for y in range(PianoManager.NB_PIN):
                self.ls_ChipBoard[i].setDirection(y, self.ls_ChipBoard[i].DIR_OUTPUT)
                self.ls_ChipBoard[i].digitalWrite(y, MCP23S17.LEVEL_LOW)         

    # Méthode qui lance la musique
    def play(self, PathMidi):
        self.IsPlaying = True           # Dit que la musique est en train de jouer
        self.pathMidi = PathMidi        # Transfère l'argument vers l'attribut
        self.start_time = time.time()   # Enregistre le temps pour savoir quand la musique à été lancée
        self.threadpianoManager.start() # Lance le thread PianoManager
        self.pedalManager.start()       # Lance le thread PedalManager

    def execute(self):
        # Lit le fichier midi et extrait ses données
        mid = mido.MidiFile(self.pathMidi)

        # Lancement de la musique
        for message in mid.play():

            # Si IsPlaying est set à False, la musique s'arrête
            if not self.IsPlaying:
                break

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
                        self.ls_ChipBoard[(message.note -21)//16].digitalWrite((message.note -21)%16, MCP23S17.LEVEL_HIGH)
                    else:
                        self.ls_ChipBoard[(message.note -21)//16].digitalWrite((message.note -21)%16, MCP23S17.LEVEL_LOW)

                case 'note_off':
                    self.ls_ChipBoard[(message.note -21)//16].digitalWrite((message.note -21)%16, MCP23S17.LEVEL_LOW)

                # Si le message du fichier midi est du type "control_change",
                # le "control_change" est un message pour tout ce qui est autre qu'une note.
                case 'control_change':
                    # Dans notre cas, nous cherchons un appui de la pédale.
                    # Donc on vérifie si le message "control_change" est égal à 64 (message pour pédale)
                    if message.control == 64:
                        if message.value == 0:
                            self.pedalManager.off()
                        else:
                            self.pedalManager.on()

        # Lorsque la musique est arretée ou terminée, reset la pédal et tout les touches.
        self.pedalManager.off()
        for i in range(PianoManager.NB_CHIP):
            for y in range(PianoManager.NB_PIN):
                self.ls_ChipBoard[i].digitalWrite(y, MCP23S17.LEVEL_LOW)
        self.IsPlaying = False
        self.pedalManager.close()

    # Méthode pour arreter la musique
    def stop(self):
        self.IsPlaying = False
    
    # Méthode qui permet de mettre en pause le programme jusqu'à que la musique s'arrête
    def threadJoin(self):
        self.threadpianoManager.join()
    
    # Renvoie depuis combien de temps la musique se joue.
    @property
    def elapsedTimeMusic(self):
        elapsed_time = int(time.time() - self.start_time)
        return elapsed_time
    
    # Renvoie le temps Total de lu fichier midi
    def totalTimeMusic(self, pathMidi):
        mid = mido.MidiFile(pathMidi)
        return int(mid.length)

    # Renvoie si la musique est en train de jouer
    @property
    def isPlaying(self):
        return self.IsPlaying