from flask import Flask, render_template
from markupsafe import escape
from flask import request
import os
import json

def getPath(number = 0) :
	try :
		number = int(number)
	except :
		number = -1
	initPath = os.path.dirname(__file__)								# Enregistre le chemin actuel du fichier
	folderPath = str(os.path.normpath(initPath + os.sep + os.pardir))
	musicPath = folderPath + "/Musique_midi"							# Enregistre le chemin du dossier des musiques (équivalent au chemin du programme actuel mais en remplaçant le dernier répertoire par 'Musique_midi')
	if number == 0 :
		return initPath, musicPath
	elif number == 1 :
		return initPath
	elif number == 2 :
		return musicPath
	else :
		print(f"Mauvais argument spécifié pour la fonction 'getPath'.")
		return 0

def refreshData() :
	initPath = getPath(1)
	musicPath = getPath(2)
	data = {}															# Crée une mémoire 'data' qui va par la suite enregistrer le nom de tous les fichiers midi et les écrire dans le fichier 'list.json'
	listMusic = []
	if os.path.exists(musicPath) :
		print("Data mise à jour")
		for i in os.listdir(musicPath) :								# Enregistre les noms des musiques (en ignorant ".mid") dans la mémoire 'listMusic'
			listMusic.append(i[:-4])
		data["listMusic"] = listMusic									# Transfère le contenu de 'listMusic' dans la mémoire 'data', dans un format approprié aux fichiers json
		with open("list.json", "w") as f :
			json.dump(data, f, indent = 4)								# Écrit le contenu de 'data' dans le fichier 'list.json' (le fichier est écrasé)
		return 1
	else :
		print(f"Aucune musique détectée sous le répertoire {musicPath}")
		return 0
		
def getData() :
	if refreshData() :
		with open("list.json", "r") as f :
			data = json.load(f)
		listMusic = data["listMusic"]
		return listMusic
	else :
		return 0



app = Flask(__name__)


@app.route('/')
def index():
	return render_template('xHtml_mainMenu.html')

@app.route('/play')
def play():
	listMusic = getData()
	return "<h3><p>Liste des titres :</p></h3> <p>{liste}</p>".format(liste = listMusic)

@app.route('/listedit')
def listedit():
	return "<p>Pouf pouf {}</p>"

@app.route('/howitworks')
def howitworks():
	return "<p>Pouf pouf tuto</p>"

if __name__ == '__main__' :
	app.run(debug=True, use_reloader=True)

