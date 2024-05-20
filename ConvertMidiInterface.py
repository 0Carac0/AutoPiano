import mido
import tkinter as tk
from tkinter import font
from tkinter import filedialog
import sys
import json
from StructuralFunction.ConvertMidi import convertMidi
#from .. StructuralFunction.ConvertMidi import convertMidi

# ls_   |   List
# lb_   |   Label
# cb_   |   Check box
# eb_   |   Entry box
# bt_   |   Button
# fn_   |   Font
# tx_   |   Text

def submit():

    isCorectEnterys = True
    # Verifie les entrées des temps
    ls_en_time_float = []
    try:
        for i in range(len(ls_en_time)):
            ls_en_time_float.append(float(ls_en_time[i].get()))
    except ValueError:
        Error_label.config(text="[ERROR] Un des paramètres de temps est faux.", fg="red")
        isCorectEnterys = False

    # Verifie si l'utlilisateur veux supprimer toutes les tracks
    asAllDeletTrack = True
    for cb_trackValue in ls_cb_trackValue:
        if not cb_trackValue.get():
            asAllDeletTrack = False
    if asAllDeletTrack:
        Error_label.config(text="[ERROR] Vous supprimez toutes les tracks.", fg="red")
        isCorectEnterys = False

    if isCorectEnterys:

        if convertMidi(
            filePath, 
            MinTimeOffPedal=ls_en_time_float[0], 
            MinTimeOffNote=ls_en_time_float[1], 
            MinTimeOnNote=ls_en_time_float[2], 
            MaxTimeOnNote=ls_en_time_float[3],
            ls_deleteTracks= [cb_trackValue.get() for cb_trackValue in ls_cb_trackValue],
            MesurePedal=0
            ):

            Error_label.config(text="[INFO] Le fichier midi converti a été créer au même emplacement.", fg="green")
        else:
            Error_label.config(text="[ERROR] Une erreur est survenue lors de la conversion.", fg="red")

# Ouvrir la boîte de dialogue de sélection de fichier
filePath = filedialog.askopenfilename(title="Sélectionner le fichier midi à convertir", filetypes=(("Fichier Midi", "*.mid"), ("All files", "*.*")))
if filePath == '':
    print("Aucun fichier n'a été sélectionné.")
    sys.exit()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Modification du fichier midi")
root.geometry("450x800")

# Memoire de la combientième ligne en est le programme 
CurrentRow = 0

# Configuration de la police pour les sous titres
fn_chapter = font.Font(family="Helvetica", size=9, weight="bold")


# Création de la partie pour afficher le chemin du fichier


# Ajout du sous-titre
lb_TimeParameters = tk.Label(root, text='Fichier sélectinné :', font=fn_chapter)
lb_TimeParameters.grid(row=CurrentRow, column=0, sticky='w', padx=10, pady=10)
CurrentRow += 1

# Label pour afficher le chemin du fichier
path_label = tk.Label(root, text='... ' + filePath[-65:])
path_label.grid(row=CurrentRow, column=0, columnspan=2, sticky='w', padx=20)
CurrentRow += 1


# Création de la partie pour les paramètres de temps


# Ajout du sous-titre
lb_TimeParameters = tk.Label(root, text='Reglage des temps [s] :', font=fn_chapter)
lb_TimeParameters.grid(row=CurrentRow, column=0, sticky='w', padx=10, pady=10)
CurrentRow += 1

# liste des labels et des valeurs par défaut des paramètre de temps
ls_timeParameters = (
    # Texte pour le label                       Paramètre de base
    ("Temps minimum pour relacher la pédale",    "0.2"),
    ("Temps minimum pour relacher une touche",   "0.1"),
    ("Temps minimum pour jouer une touche",      "0.05"),
    ("Temps maximum pour maintenir une touche",  "4")
)
ls_en_time = []
# Ajout des label et des entry box
for i in range(len(ls_timeParameters)):

    # Crée et place le text
    lb_tx = tk.Label(root, text=ls_timeParameters[i][0])
    lb_tx.grid(row=i+CurrentRow, column=0, sticky='w', padx=20)
    
    # Crée et place l'entry box
    eb_time = tk.Entry(root)
    eb_time.grid(row=i+CurrentRow, column=1)
    # Pré-remplir l'entry box avec la valeur par défaut
    eb_time.insert(0, ls_timeParameters[i][1])
    # Stockage des entry box
    ls_en_time.append(eb_time)
    

CurrentRow += len(ls_timeParameters)


# Création de la partie pour supprimer les pistes


# Ajout du sous-titre
lb_TimeParameters = tk.Label(root, text='Suppression de piste :', font=fn_chapter)
lb_TimeParameters.grid(row=CurrentRow, column=0, sticky='w', padx=10, pady=10)
CurrentRow += 1

# Label pour afficher l'utilisation des coches
check_label = tk.Label(root, text='Cochez les pistes que vous voulez supprimer.')
check_label.grid(row=CurrentRow, column=0, columnspan=2, sticky='w', padx=20)
CurrentRow += 1

# Lit le fichier midi et on extrait ses données
midiFile = mido.MidiFile(filePath)

# Extrait la liste des instruments dans les fichiers midi
with open('StructuralFunction\\ListeNomPisteMidi.json', 'r') as f:
    ls_NameInstrument = json.load(f)["listTrackName"]

# Affichage de la liste des pistes
NameInstrument = "Piste non instrumental ou définit sur une autre piste"
ls_cb_trackValue = []
for i, track in enumerate(midiFile.tracks):
    row = 0
    try:
        while not track[row].type == 'program_change':
            row += 1
        NameInstrument = ls_NameInstrument[track[row].program]
    except IndexError:
        pass

    ls_cb_trackValue.append(tk.BooleanVar())
    cb_track = tk.Checkbutton(root, text=NameInstrument, variable=ls_cb_trackValue[i])
    cb_track.grid(row=i+CurrentRow, column=0, columnspan=2, sticky='w', padx=30)

CurrentRow += len(ls_cb_trackValue)

"""
# Création de la partie pour ajouter la pédale

# Ajout du sous-titre
lb_TimeParameters = tk.Label(root, text='Ajout de la pédal :', font=fn_chapter)
lb_TimeParameters.grid(row=CurrentRow, column=0, sticky='w', padx=10, pady=10)
CurrentRow += 1

# détecte déjà s'il y a des messages de pédale
isFindPedal = False
for track in midiFile.tracks:
    if isFindPedal:
        break
    for msg in track:
        if msg.type == 'control_change':
            if msg.control == 64:
                isFindPedal = True
                break

# S'il y a déjà des messages de pédale alors on ne propose pas d'en rajouter
if isFindPedal:
    print("Pas Pedal")
    pass
else:
    # Coche pour ajouter oui ou non la pédale
    cb_pedalValue = tk.BooleanVar()
    cb_pedal = tk.Checkbutton(root, text='Ajouter les messages de pédal', variable=cb_pedalValue)
    cb_pedal.grid(row=CurrentRow, column=0, columnspan=2, sticky='w', padx=20)
    CurrentRow += 1
"""

# Bouton de validation
bt_confirm = tk.Button(root, text="Confirmer", command=submit)
bt_confirm.grid(row=CurrentRow, column=1, sticky='w', pady=10)
CurrentRow += 1

# Label pour afficher les erreurs
Error_label = tk.Label(root, text='')
Error_label.grid(row=CurrentRow, column=0, columnspan=2, sticky='w', padx=10)

# Affiche la fenêtre
root.mainloop()

