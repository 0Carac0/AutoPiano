"""
Importations :
- flask pour le site web
- werkzeug pour l'importation de nouvelles musiques depuis le site
- requests pour les requêtes du client
- markupsafe pour assurer le bon fonctionnement de l'HTML
- os pour ouvrir les dossiers et récupérer les fichiers des musiques
- shutil pour déplacer les fichiers
- json pour la database
- PianoManager (programme python) pour activer les touches du piano
- convertisseur pour permettre à la pédale de se relacher
"""
from flask import Flask, flash, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename
import requests
from markupsafe import escape
import os
import shutil
import json
from PianoManager import PianoManager
from convertisseur import convert

"""Fonction qui permet d'afficher sur le terminal
ce qui est retourné par une fonction.
Est utilisée à la place du keyword 'return'."""
def preturn(arg) :
	print(arg)
	return(arg)

"""Petite fonction simple qui permet de comparer deux 
variables de types différents en les convertissant temporairement en 'str'"""
def same(var1, var2 = 1) :
	if str(var1) == str(var2) :
		return 1
	else :
		return 0

"""Fonction permettant de récupérer la liste des dossiers du fichier
'Musiques_midi'. Sert à pouvoir choisir dans quel dossier
upload ou déplacer des musiques.
La première valeur retournée est un "", ce qui représente
le dossier 'Musiques_midi' tout seul, sans aller creuser
dans les dossiers internes
"""
def lisDir(Type, path) :
	lisDirs = [""]
	for i in os.listdir(path) :
		item = path + "/" + i
		if os.path.isdir(item) :
			if Type == "folder" :
				lisDirs.append(i)
			try :
				for j in lisDir(Type, path + "/" + i) :
					if j != "" :
						lisDirs.append(i + "/" + j)
			except :
				pass
		elif (Type == 'file' and os.path.isfile(item)) :
			lisDirs.append(i)
	lisDirs.sort(key=str.lower)
	return lisDirs

""" digFolder : Explore un répertoire et retourne les fichiers '.mid' trouvés
Arguments :
'initialPath' - chemin du dossier principal dans lequel se trouve le
	dossier à explorer
'folderPath' - nom du dossier à explorer

Fonction récursive qui explore le dossier 'folderPath', puis ouvre 
chaque dossier interne et récupère chaque chemin de fichier de type '.mid'.
Les chemins des fichiers sont donnés à partir de 'initialPath'.
"""
def digFolder(initialPath, folderPath) :								# Arguments : 'initialPath' = le chemin du dossier 'Musique_midi' contenant les musiques | 'folderPath' = le chemin "supplémentaire" du dossier en cours d'analyse à partir de 'Musique_midi' - - - Cette fonction récursive ouvre un dossier, récupère les chemins des fichiers et ouvre tous les autres dossiers pour récupérer chaque fichier existant dans toute l'arborescence.
	totalPath = initialPath + "/" + folderPath
	#print(totalPath)
	listMusic = []
	for i in os.listdir(totalPath) :									# Boucle 'for' qui va consulter la liste des fichiers présents dans le dossier interne au dossier des musiques ; 'i' prend le nom de chacun de ces fichiers
		#print(i)												
		try :
			if os.path.isdir(totalPath + "/" + i) :						# Si 'i' est un dossier ...
				try :
					for j in digFolder(initialPath, folderPath + "/" + i) :	# ...cette fonction s'appelle elle-même (=on dit qu'elle est récursive) afin d'analyser le dossier en question : en extrait chaque fichier '.mid' et ouvre chaque dossier imbriqué...
						listMusic.append(j)								# ...puis ajoute chaque fichier à la liste. NOTE : chaque fichier est précédé par son répertoire relatif à partir du fichier des musiques, afin d'être plus facilement traitable par le programme
				except :
					print(f"Fichier {i} vide")
			elif i[-4:] == ".mid" :										# Si le nom du fichier est de type 'midi' (nom de fichier se terminant par '.mid')...
				listMusic.append(folderPath + "/" + i[:-4])				# ...l'ajoute à la liste 'listMusic', accompagné par son répertoire à partir du dossier 'Musique_midi''
		except :
			pass
	return listMusic													# Renvoie la liste des musiques trouvées par la fonction (et par chacune de ses itérations internes, s'il y en a eu)

""" getPath : Cherche dans quel répertoire se trouve le programme
Arguments :
'number' - Permet d'obtenir uniquement le chemin qui nous intéresse ;
	1 pour le chemin du programme actuel,
	2 pour le chemin du dossier des musiques
	3 pour le chemin du fichier 'playing.json'
'debug' - si mis à 1, indiquera le chemin 
"""
def getPath(number = "all", debug = 0) :								# Arguments : 'number' à mettre à 1 / 2 / 3 pour obtenir respectivement le chemin du programme 'webMenu.py', celui du dossier 'Musique_midi' contenant les musiques ou celui du fichier 'playing.json' contenant le nom de la musique en train d'être jouée (renvoie les trois en même temps si on laisse la valeur par défaut) | 'debug' à mettre à 1 pour obtenir le chemin dans lequel devrait normalement se trouver le dossier des musiques
	initPath = os.path.dirname(__file__)								# Enregistre le chemin actuel du fichier
	folderPath = str(os.path.normpath(initPath + os.sep + os.pardir))	# Équivalent à 'initPath', mais avec un retour en arrière
	
	musicPath = 0
	for i in ("", " ", "_", "s", "s ", "s_") :								# Cherche un dossier appelé 'Musiques_midi' (accepte certaines variations telles que 'Musiques midi' ou 'Musiquemidi' grâce à la boucle 'for')
		#print (initPath + "/Musique" + i + "midi")
		if os.path.exists(initPath + "/Musique" + i + "midi") or debug :
			musicPath = initPath + "/Musique" + i + "midi"				# Enregistre le chemin du dossier des musiques (équivalent au chemin du programme actuel mais en remplaçant le dernier répertoire par 'Musique_midi')
			break
	print("musicPath =", musicPath)
		
	playingPath = initPath + '/playing.json'							# Enregistre le chemin où devrait normalement se trouver 'playing.json'
	if not os.path.exists(playingPath) :								# Si le fichier en question n'existe pas, ...
		with open(playingPath, "w") as f :								# ...il est créé...
			data = {}
			data["Currently playing"] = "0"
			json.dump(data, f, indent = 4)								# ...puis rempli avec la donnée 'Currently_playing'. 
			
			""" Note : On aurait également pu utiliser un bête fichier texte ('.txt' au lieu de '.json'), moins lourd et moins contraignant si l'on ne veut y écrire qu'une seule donnée.
			 On utilise ici un fichier 'json' car, dans le futur, si un apprenti veut rajouter une fonction de "liste des musiques en attente" ou de "playlist",
			 il lui sera plus simple de travailler en partant d'une base en 'json' qu'en partant sur une base en 'txt' """
			
			pass		
	paths = [initPath, musicPath, playingPath]
	if same(number, "all") :											# Si 'number' a gardé sa valeur par défaut (= "all") :
		return paths													# renvoie la liste des chemins obtenus
	else :																# Si 'number' a pris une autre valeur :
		try :
			return paths[int(number -1)]								# renvoie le chemin demandé (le "-1" est là parce que l'argument 'number' peut aller de 1 à 3, alors que l'indexation des valeurs de la liste va de 0 à 2)
		except :														# Si la valeur n'était pas un chiffre entre 1 et 3, cela génère une erreur qui affiche un message sur le terminal et retourne un zéro
			print(f"Mauvais argument spécifié pour la fonction 'getPath' : {number}")
			return 0

def refreshData() :														# Synchronise la liste des musiques avec les fichiers réellement sauvegardés sur l'appareil
	initPath = getPath(1)
	musicPath = getPath(2)
	settingConv = [0]
	
	data = {}															# Crée une variable 'data' (qui va par la suite enregistrer le nom de tous les fichiers midi et les écrire dans le fichier 'list.json')
	listMusic = []														# Crée une variable 'listMusic' de type 'list'
	
	# Note : la grande différence pratique entre 'data' et 'listMusic' est que 'data' est un type de variable adapté aux fichiers 'json', alors que 'listMusic' est plus facile à utiliser dans un programme python basique.
	# C'est pourquoi le programme range initialement ses données dans 'listMusic' puis transfère le tout dans 'data'.
																		# Enregistre les noms des musiques (en ignorant ".mid") dans la mémoire 'listMusic' :
	try :
		if musicPath == 0 :
			raise Exception('Dossier des musiques introuvable')
		for i in os.listdir(musicPath) :								# Boucle 'for' qui va consulter la liste des fichiers présents dans le dossier des musiques ; 'i' prend le nom de chacun de ces fichiers														
			try :
				if os.path.isdir(musicPath + '/' + i) :					# Si un dossier est présent dans 'Musique_midi'...
					try :
						for j in digFolder(musicPath, i) :				# ...le programme appelle la fonction 'digFolder()', qui se charge d'ouvrir le dossier et de renvoyer une liste comprenant chaque nom de fichier 'midi' qu'elle y a trouvé.
							listMusic.append(j)							# Une fois que 'digFolder()' a fini son exploration et renvoyé la liste, cette dernière est ajoutée, un élément à la fois, dans la liste 'listMusic'
					except :
						print(f"Fichier {i} vide")
				elif i[-4:] == ".mid" :									# Si le nom du fichier est de type 'midi' (nom de fichier se terminant par '.mid')...
					listMusic.append(i[:-4])							# ...cette ligne enlève les 4 derniers caractères de son nom ('.mid') avant de l'ajouter à la liste 'listMusic'.
			except :
				pass
		listMusic.sort(key=str.lower)									# Range les musiques par ordre alphabétique
		data["listMusic"] = listMusic									# Une fois que chaque fichier a été contrôlé, transfère le contenu de 'listMusic' dans la mémoire 'data'.
		#print(initPath + "/" + "list.json", listMusic)
		with open(initPath + "/list.json", "r") as f :
			try :
				actualData = json.load(f)
				data["settings"] = actualData["settings"]
			except :
				data["settings"] = settingConv
			print(data["settings"][0])
		with open(initPath + "/list.json", "w") as f :
			print(data["settings"][0])
			json.dump(data, f, indent = 4)								# Écrit le contenu de 'data' dans le fichier 'list.json' (le fichier est écrasé s'il existait déjà)
		print("Data mise à jour")
		return 1														# Renvoie la valeur 1 si tout s'est bien passé
	except :
		print(f"Aucune musique détectée dans le répertoire {musicPath}")
		return 0														# S'il y a eu un problème (dossier mal nommé/inexistant ou absence de musiques dans ledit dossier), renvoie la valeur 0

""" 'getData()' : renvoie la liste des musiques
Arguments :
cursor - si définie, renvoie la valeur 'getData()[cursor]'
convOnly - ne renvoie que les musiques converties
refresh - si set à 0, ne met pas à jour l'affichage de la liste des musiques dans la dropdowm
"""
def getData(cursor = "all", convOnly = 0, refresh = 1) :				# Arguments : 'cursor' pour obtenir une variable spécifique au lieu de la liste complète / 'refresh' à mettre à zéro pour consulter la database sans la mettre à jour
	musicPath = getPath(2)
	databaseOK = 0
	if same(refresh, 0) :												# Si le programme veut uniquement lire le fichier 'list.json' (la liste des musiques) sans le réecrire...
		if os.path.exists(musicPath) :									# ...cette ligne vérifie que le fichier existe...
			databaseOK = 1												# ...et autorise le programme à continuer, le cas échéant.
	elif refreshData() :												# Si le programme n'a pas spécifié ne pas vouloir réécrire le fichier, cette ligne appelle la commande 'refreshData()'...
		databaseOK = 1													# ...et autorise le programme à continuer, si la commande 'refreshData()' s'est terminée sans erreur (=si elle a retourné 1).
	if databaseOK == 1 :												# Si le programme a reçu l'autorisation de continuer ;
		with open(getPath(1) + "/list.json", "r") as f :								# le fichier 'list.json' est ouvert en mode 'r' (=read, donc lecture seule)...
			data = json.load(f)											# ...et toutes les informations contenues dans le fichier 'list.json' sont chargées dans la variable 'data'.			
			listMusic = data["listMusic"]								# Ensuite, la variable 'listMusic' récupère la valeur de la rubrique 'listMusic' contenue dans 'data' (consulter le fichier 'list.json' pour y voir plus clair).
		
		
		"""
		Le morceau de programme suivant crée une version convertie de chaque musique qui ne l'est pas déjà.
		Ces versions sont séparées en deux listes distinctes :
		'listMusic', qui contient les musiques originales non-converties
		'listConv', qui contient les musiques converties
		Si elle a été appelée avec l'argument 'convOnly = 1', la fonction ne renverra que la liste des musiques converties.
		"""
		listConv = []
		i = 0
		while i < len(listMusic) :
			if len(listMusic[i]) > 5 :
				if listMusic[i][-5:] == '_Conv' :
					listConv.append(listMusic.pop(i))
				else :
					i += 1
		#print (listConv)
		for i in listMusic :
			
			if len(i) > 5 :
				if (i + "_Conv") not in listConv and i[-5:] != '_Conv' :
					convert_music = 1
				else :
					convert_music = 0
			elif len(i) > 0 :
				convert_music = 1
				
			if convert_music :
				musicPath = getPath(2)
				print(i)
				try :
					if convert(musicPath + "/" + i + ".mid") :
						listConv.append(i + "_Conv")
					else :
						print("Convert échoué")
						listConv.append(i)
				except :
					print("\nConvert échoué ET convertisseur non-sécurisé (retourne une erreur au lieu d'un 0)\n")
		if convOnly == 1 :
			listMusic = []
			listMusic = listConv
		
		
		if str(cursor) == "all" :										# Si la commande 'getData()' a été appelée avec l'argument 'cursor' par défaut...
			return listMusic											# ...elle renvoie toute la liste des musiques.
		else :															# Dans le cas contraire...
			try : 
				cursor = int(cursor)
				music = listMusic[cursor]				
				
				#print(music)
				return music											# ...elle revoie uniquement l'élément n°x, où x est la valeur du 'cursor'. (La fonction 'try' est là pour éviter au programme de crash si la valeur de 'cursor' n'était pas une valeur convenable)
			except : 
				print(f"Mauvais argument 'cursor' spécifié pour la fonction 'refreshData' : {cursor} ; max {len(listMusic) -1}")
				return 0
	else :
		return 0

"""
La fonction suivante analyse le nom de la musique.
Si le nom de la musique est trop long pour être affiché sur une seule ligne sans dépasser du cadre,
le programme découpe le nom de la musique afin de l'afficher sur plusieurs lignes.
Afin d'insérer des retours à la ligne de manière propre, le programme commence par chercher
des endroits où couper le nom de la musique, comme des espaces, underscores ou tirets.
'text' = Texte à analyser
'minLenght' = Nombre de carcatères à partir duquel le programme commence à essayer d'insérer proprement un retour à la ligne
'maxLenght' = Longueur maximale affichable sur une ligne. Quand une ligne atteint cette longueur, le programme force un retour à la ligne
"""
def textFormat(text, minLenght = 35, maxLenght = 50) :
	formatedText = ""
	for i in range(len(text)) :
		"""
		Les lignes suivantes ajoutent des retours à la ligne intelligents dans le nom de la musique si ce dernier est trop long pour être affiché correctement.
		Ainsi, au lieu d'écrire "Nom_vraiment_incroyablement_long_qui_ne_peut_pas_être_affiché_entièrement", le programme affichera par exemple :
		"Nom_vraiment_incroyablement_long ... <br> ... _qui_ne_peut_pas_être_affiché ... <br> ... _entièrement", ce qui, en HTML, correspond à :
			"Nom_vraiment_incroyablement_long ...
			... _qui_ne_peut_pas_être_affiché ...
			... _entièrement"
		Note : le placement exact des retours à la ligne dépend des valeurs de 'minLenght' et 'maxLenght'
		"""

		if (i >= maxLenght and not ">" in formatedText[-maxLenght:]) or (i > minLenght and text[i] in ("_", "-") and not ">" in formatedText[-minLenght:]) :
			print (f"> {formatedText[:i]} - {i} - {formatedText[i:]}")
			formatedText += " ... <br> ... "
		elif i > minLenght and text[i] in (" ", ":") and not ">" in formatedText[-minLenght:] :
			formatedText += "<br>"
		if text[i] in ("\\", "/") :
			formatedText += " : <br> "
		else :
			formatedText += text[i]
	return formatedText

"""
Définit quelques paramètres importants pour le fonctionnement de certaines fonctionnalités
'app.config' permet de fixer les paramètres (ou règles) de l'enregistrement, comme la taille max ou le dossier
"""
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = getPath(2)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1000							# Taille max en bytes des fichiers importés : 100 * 1000 = 100kB

print(" >", app, "on path", "'" + getPath(1) + "'")

pianoManager = PianoManager()


# Affiche la page web "de base", pour l'URL 'http://<IP>/'
@app.route('/', methods = ["POST", "GET"])															
def main_menu():
	refreshData()
	return render_template('mainMenu.php', menuText = "Bienvenue sur le programme du piano d'atelier API !")

@app.route('/play', methods = ["POST", "GET"])
def drop_down():
	with open(getPath(1) + "/list.json", "r") as f :
		data = json.load(f)
		#try :
		settingConv = data["settings"][0]
		#print(f"\n\nSETTING_CONV = {settingConv}\n\n")
	
	if settingConv :
		modeText = "converties"
		buttonText = "non-converties"
	else :
		modeText = "non-converties"
		buttonText = "converties"
		
	musicData = getData(convOnly = settingConv)
	
	if same(musicData, 0) :
		return f"<p>Musiques introuvable.</p><p>Essayez d'enregistrer des fichiers MIDI sous le répertoire {getPath(2, debug = 1)}</p>"
	else :
		#print(musicData)
		
		"""Affiche le fichier 'dropDown.php', qui est écrit en HTML (partie texte) avec quelques intégrations PHP (partie dynamique)
		en lui envoyant la liste des musiques mise à jour (via 'getData()') en tant qu'argument"""
		return render_template('dropDown.php', imgPath = getPath(1) + "/", data = musicData, modeTxt = modeText, buttonTxt = buttonText)

# Récupère le choix selectionné sur le site web une fois que la page 'http://<IP>/music' s'ouvre
@app.route('/music', methods = ["POST", "GET"])
def music():
	if request.method == "POST" :
		musicToPlay = request.form['select_music']						# Récupère l'information en provenance de 'dropDown.php'
		playlist = {}
		playing = getPath(3)
		
		# Utile dans le futur pour une playlist. Actuellement sans aucun effet.
		with open(playing, 'w+') as f :
			try :
				data = json.load(f)
			except :
				pass
				
		print (musicToPlay)
		
		musicToDisplay = textFormat(musicToPlay, 35, 50)
		
		try :
			pianoManager.play(preturn(getPath(2) + "/" + musicToPlay + ".mid"))
			return render_template('playing.php', data = musicToDisplay)
		except :
			return render_template('error.php', errType = f"La musique '{musicToPlay}' n'est pas jouable.")	
	else :
		return "Échec de la méthode"

# Arrête la musique
@app.route('/stop', methods = ["POST", "GET"])
def stop_music():
	if request.method == "POST" :
		try :
			musicToPlay = request.form['stop_music']
			pianoManager.stop()
		except :
			pass
	else :
		print ("Échec de la méthode")
	return redirect("/play")

"""
Change le mode affiché (versions converties / non-converties)
Ce mode est un réglage contenu dans 'list.json', sous la forme de la valeur ["settings"] qui peut prendre 0 ou 1
"""
@app.route('/settings', methods = ["POST", "GET"])
def settings():
	if request.method == "POST" :
		musicToPlay = request.form['setConv']
		with open(getPath(1) + "/list.json", "r") as f :
			data = json.load(f)
			
		print(data["settings"][0])
		if data["settings"][0] == 1 :
			data["settings"][0] = 0
		else :
			data["settings"][0] = 1
		print(data["settings"][0])
		
		with open(getPath(1) + "/list.json", "w") as f :
			json.dump(data, f, indent = 4)
	else :
		print("Erreur")
	return redirect("/play")

# Affiche la page d'ajout de musique
@app.route('/addMusic', methods = ["POST", "GET"])
def listedit():
	return render_template('uploadFile.php', data = lisDir("folder", getPath(2)))	

"""
Récupère le fichier '.mid' que le client essaie d'ajouter
En teste certains attributs (nom, taille) et l'enregistre si
les conditions sont remplies.
"""
@app.route('/upload',  methods = ["POST", "GET"])
def addMusic() :
	uploadFolder = request.form['uploadFolder']
	print(uploadFolder)
	if uploadFolder == "" :
		uploadPath = app.config['UPLOAD_FOLDER']
	else :
		uploadPath = getPath(2) + "/" + uploadFolder
	try :
		uploadMusic = request.files['file']
		print(">", uploadMusic.filename)
		if uploadMusic.filename != '' :
			if uploadMusic.filename[-4] == '.' :
				uploadMusic.filename = uploadMusic.filename[:-3] + uploadMusic.filename[-3:].lower()
				print (uploadMusic.filename)
				if uploadMusic.filename[-4:] == '.mid' :
					if not ">" in uploadMusic.filename :
						uploadMusic.save(os.path.join(uploadPath, uploadMusic.filename))
						return render_template('mainMenu.php', menuText = f"Musique ajoutée dans<br>3{uploadFolder} !")
					else :
						return render_template('mainMenu.php', menuText = "Merci de ne pas inclure le caractère '>' dans un nom de musique")
				else : 
					return render_template('mainMenu.php', menuText = "Mauvais format de musique. '.mid' requis")
		else :
			raise Exception
	except :
		return render_template('mainMenu.php', menuText = "Fichier trop lourd ou inexistant. Ajout échoué.")
	return render_template('mainMenu.php', menuText = "Fichier non-conforme. Ajout échoué.")

# Affiche la page d'ajout de musique
@app.route('/editMusicList', methods = ["POST", "GET"])
def editList():
	return render_template('editMusicList.php', lisMusic = getData(), lisFolders = lisDir("folder", getPath(2)))

"""
Déplace le fichier dans la destination-cible choisie par l'utilisateur.
Permet de supprimer des fichiers
"""
@app.route('/edited',  methods = ["POST", "GET"])
def edited() :
	pathToEdit = request.form['lisMusic'] + '.mid'
	pathToEdit_Conv = request.form['lisMusic'] + "_Conv.mid"
	targetFolder = request.form['lisFolders']
	print(f"> Action : {targetFolder}")
	if os.path.exists(preturn(getPath(2) + "/" + pathToEdit)) :
		if targetFolder == "SUPPRIMER_LE_FICHIER" :
			
			return render_template('mainMenu.php', menuText = preturn(textFormat(f"Fichier : <br> '{pathToEdit}' <p> supprimé (fonction non-disponible, en attente d'une sécurité)")))
		else :
			fileToMove = getPath(2) + "/" + pathToEdit
			fileToMove_Conv = getPath(2) + "/" + pathToEdit_Conv
			targetPath = getPath(2) + "/" + targetFolder
			shutil.move(preturn(fileToMove), preturn(targetPath))		# Déplace le fichier dans la destination voulue
			if os.path.exists(fileToMove_Conv) :
				shutil.move(preturn(fileToMove_Conv), preturn(targetPath))	# Déplace le fichier converti correspondant au fichier déplacé
				
			return render_template('mainMenu.php', menuText = preturn(textFormat(f"Fichier : <br> '{pathToEdit}' <p> Déplacé dans {getPath(2) + '/' + targetFolder}")))
	else :
		return render_template('mainMenu.php', menuText = preturn(textFormat(f"Le fichier '{pathToEdit}' a été déplacé avant que vous ne le fassiez.")))



# Affiche la page de création de dossier
@app.route('/createFolder', methods = ["POST", "GET"])
def createFolder():
	return render_template('createFolder.php', lisFolders = lisDir("folder", getPath(2)))	

"""
# Crée un dossier avec le nom indiqué par l'utilisateur
@app.route('/createFolder', methods = ["POST", "GET"])
def createFolder():
	return render_template('createFolder.php', lisFolders = lisDir("folder", getPath(2)))
"""

"""
Lance l'application 'app' sur le port 8000
"""
if __name__ == '__main__' :
	app.run(host="0.0.0.0", port=8000)	# Met le site en ligne
