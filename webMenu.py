from flask import Flask, render_template, request
import requests
from markupsafe import escape
import os
import json
import PianoManager


def same(var1, var2 = 1) :												# Petite fonction simple qui permet de comparer deux variables de types différents en les convertissant temporairement en 'str'
	try :
		if str(var1) == str(var2) :
			return 1
		else :
			return 0
	except :
		return 0

def getPath(number = "all", debug = 0) :								# Arguments : 'number' à mettre à 1 / 2 / 3 pour obtenir respectivement le chemin du programme python en cours, celui du dossier contenant les musiques ou celui du fichier 'playing.json' (renvoie les deux dans un tuple par défaut) | 'debug' à mettre à 1 pour obtenir le chemin dans lequel devrait normalement se trouver le dossier des musiques
	initPath = os.path.dirname(__file__)								# Enregistre le chemin actuel du fichier
	folderPath = str(os.path.normpath(initPath + os.sep + os.pardir))	# Équivalent à 'initPath', mais avec un retour en arrière
	
	musicPath = 0
	for i in (" ", "_", "s ", "s_", "") :								# Cherche un dossier appelé 'Musique_midi' (accepte certaines variations telles que 'Musiques midi' ou 'Musiquemidi' grâce à la boucle 'for')
		print (initPath + "/Musique" + i + "midi")
		if os.path.exists(initPath + "/Musique" + i + "midi") or debug :
			musicPath = initPath + "/Musiques_midi"						# Enregistre le chemin du dossier des musiques (équivalent au chemin du programme actuel mais en remplaçant le dernier répertoire par 'Musique_midi')
			break
	print("MusicPath =", musicPath)
		
	playingPath = initPath + '/playing.json'
	if not os.path.exists(playingPath) :
		with open(playingPath, "x") as f :
			pass		
	
	paths = [initPath, musicPath, playingPath]
	
	if same(number, "all") :
		return initPath, musicPath, playingPath
	elif same(number, 1) :
		return initPath
	elif same(number, 2) :
		return musicPath
	elif same(number, 3) :
		return playingPath
	else :
		print(f"Mauvais argument spécifié pour la fonction 'getPath' : {number}")
		return 0

def refreshData() :														# Synchronise la liste des musiques avec les fichiers réellement sauvegardés sur l'appareil
	initPath = getPath(1)
	musicPath = getPath(2)

	
	data = {}															# Crée une variable 'data' (qui va par la suite enregistrer le nom de tous les fichiers midi et les écrire dans le fichier 'list.json')
	listMusic = []														# Crée une variable 'listMusic' de type 'list'
	
	# Note : la grande différence pratique entre 'data' et 'listMusic' est que 'data' est adaptée aux fichiers 'json', alors que 'listMusic' est plus facile à utiliser dans un programme python basique.
	# C'est pourquoi le programme range initialement ses données dans 'listMusic' puis transfère le tout dans 'data'.

																		# Enregistre les noms des musiques (en ignorant ".mid") dans la mémoire 'listMusic' :
	try :
		if musicPath == 0 :
			raise Exception('Dossier des musiques introuvable')
		for i in os.listdir(musicPath) :								# Boucle 'for' qui va consulter la liste des fichiers présents dans le dossier des musiques ; 'i' prend le nom de chacun de ces fichiers
			try :
				if i[-4:] == ".mid" :									# Si le nom du fichier est de type 'midi' (nom de fichier se terminant par '.mid')...
					listMusic.append(i[:-4])							# ...cette ligne enlève les 4 derniers caractères de son nom ('.mid') avant de l'ajouter à la liste 'listMusic'.
			except :
				pass
		data["listMusic"] = listMusic									# Une fois que chaque fichier a été contrôlé, transfère le contenu de 'listMusic' dans la mémoire 'data'.
		with open("list.json", "w") as f :
			json.dump(data, f, indent = 4)								# Écrit le contenu de 'data' dans le fichier 'list.json' (le fichier est écrasé s'il existait déjà)
		print("Data mise à jour")
		return 1														# Renvoie la valeur 1 si tout s'est bien passé
	except :
		print(f"Aucune musique détectée dans le répertoire {musicPath}")
		return 0														# S'il y a eu un problème (dossier mal nommé/inexistant ou absence de musiques dans ledit dossier), renvoie la valeur 0
		
def getData(cursor = "all", refresh = 1) :								# Arguments : 'cursor' pour obtenir une variable spécifique au lieu de la liste complète / 'refresh' à mettre à zéro pour consulter la database sans la mettre à jour
	musicPath = getPath(2)
	databaseOK = 0
	if same(refresh, 0) :												# Si le programme veut uniquement lire le fichier 'list.json' (la liste des musiques) sans le réecrire...
		if os.path.exists(musicPath) :									# ...cette ligne vérifie que le fichier existe...
			databaseOK = 1												# ...et autorise le programme à continuer, le cas échéant.
	elif refreshData() :												# Si le programme n'a pas spécifié ne pas vouloir réécrire le fichier, cette ligne appelle la commande 'refreshData()'...
		databaseOK = 1													# ...et autorise le programme à continuer, si la commande 'refreshData()' s'est terminée sans erreur (=si elle a retourné 1).
	if databaseOK == 1 :												# Si le programme a reçu l'autorisation de continuer ;
		with open("list.json", "r") as f :								# le fichier 'list.json' est ouvert en mode 'r' (=read, donc lecture seule)...
			data = json.load(f)											# ...et toutes les informations contenues dans le fichier 'list.json' sont chargées dans la variable 'data'.
			listMusic = data["listMusic"]								# Ensuite, la variable 'listMusic' récupère la valeur de la rubrique 'listMusic' contenue dans 'data' (consulter le fichier 'list.json' pour y voir plus clair).
		if str(cursor) == "all" :										# Si la commande 'getData()' a été appelée avec l'argument 'cursor' par défaut...
			return listMusic											# ...elle renvoie toute la liste des musiques.
		else :															# Dans le cas contraire...
			try : 
				cursor = int(cursor)
				music = listMusic[cursor]
				print(music)
				return music											# ...elle revoie uniquement l'élément n°x, où x est la valeur du 'cursor'. (La fonction 'try' est là pour éviter au programme de crash si la valeur de 'cursor' n'était pas une valeur convenable)
			except : 
				print(f"Mauvais argument 'cursor' spécifié pour la fonction 'refreshData' : {cursor} ; max {len(listMusic) -1}")
				return 0
	else :
		return 0



app = Flask(__name__)
print(" >", app, "on path", "'" + getPath(1) + "'")

# Affiche la page web "de base", pour l'URL 'http://<IP>/'
@app.route('/')															
def index():
	musicData = getData()
	if same(musicData, 0) :
		return f"<p>Dossier des musiques introuvable.</p><p>Essayez d'enregistrer des fichiers MIDI sous le répertoire {getPath(2, debug = 1)}</p>"
	else :
		return render_template('dropDown.php', data = musicData)		# Affiche le fichier 'dropDown.php', qui est écrit en HTML (partie texte) avec quelques intégrations PHP (partie dynamique), en lui envoyant la liste des musiques mise à jour (via 'getData()') en tant qu'argument


# Récupère le choix selectionné sur le site web une fois que la page 'http://<IP>/music/' s'ouvre
@app.route('/music', methods = ["POST", "GET"])
def music():
	if request.method == "POST" :
		musicToPlay = request.form['select_music']						# Récupère l'info en provenance de 'dropDown.php'
		playlist = {}
		playing = getPath(3)
		
		with open(playing, 'w+') as f :
			try :
				data = json.load(f)
			except :
				pass
				
		print (musicToPlay)
		return musicToPlay
	else :
		return "Échec de la méthode"

@app.route('/listedit')
def listedit():
	return "<p>Pouf pouf {}</p>"

@app.route('/howitworks')
def howitworks():
	return "<p>Pouf pouf tuto</p>"

if __name__ == '__main__' :
	app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=True)

