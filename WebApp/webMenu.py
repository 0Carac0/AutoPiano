from flask import Flask, render_template, request
from markupsafe import escape
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
		print(f"Mauvais argument spécifié pour la fonction 'getPath' : {number}")
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
		
def getData(cursor = "all", refresh = "1") :							# Arguments : 'cursor' pour obtenir une variable spécifique / 'refresh' à mettre à zéro pour ne pas mettre à jour la database
	musicPath = getPath(2)
	databaseOK = 0 
	if str(refresh) == "0" :
		if os.path.exists(musicPath) :
			databaseOK = 1
	elif refreshData() :
		databaseOK = 1
	if databaseOK == 1 :
		with open("list.json", "r") as f :
			data = json.load(f)
			listMusic = data["listMusic"]
		if str(cursor) == "all" :
			return listMusic
		else :
			try : 
				cursor = int(cursor)
				music = listMusic[cursor]
				return music
			except : 
				print(f"Mauvais argument 'cursor' spécifié pour la fonction 'refreshData' : {cursor} ; max {len(listMusic) -1}")
				return 0
	else :
		return 0



app = Flask(__name__)


@app.route('/')
def index():
	return render_template('xHtml_mainMenu.html')

@app.route('/play')
def bloup():
	return render_template('HTML_play.html', data = getData())

@app.route('/playing')
def HTML_playing():
	return render_template('HTML_playing.html', data = getData())
	
	
#render_template('HTML_playing.html')

"""
@app.route('/choice' method=['POST'])
def bouton() :
	if form.validate_on_submit() :
		if 'download' in request.form :
			print ('Bouton 1')
		elif 'watch' in request.form :
			print ('Bouton 2')

@app.route('/plays') #, methods=['GET', 'POST'])
def plays():
	listMusic = getData()
	return requests.form["select_music"]
"""


@app.route('/listedit')
def listedit():
	return "<p>Pouf pouf {}</p>"

@app.route('/howitworks')
def howitworks():
	return "<p>Pouf pouf tuto</p>"

if __name__ == '__main__' :
	app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=True)

