#########################################################################
#																		#
#		LAUNCHER DU PROGRAMME 'webMenu.py'								#
#																		#
#		Si le nom ou emplacement du dossier 'AutoPianoWebApp' ou		#
#		que le nom du fichier 'webMenu.py' est modifié, veillez			#
#		à bien reporter le(s) changement(s) dans ce programme			#
#		également, sans quoi le launcher deviendrait ineffectif.		#
#																		#
#		Pour désactiver ce programme, settez 'launcher' à 0.			#
#																		#
#########################################################################

launcher = 1														# Set à 0 pour désactiver le programme. Set à 1 pour usage fonctionnel
autoPianoFolder = "/home/pi/Desktop/AutoPianoWebApp"				# Chemin du dossier du piano
autoPianoWebPy = "webMenu.py"										# Nom du fichier



#########################################################################
#																		#
#	Le programme suivant est une version allégée d'un launcher que		#
#	j'ai fait à titre privé afin de lancer un bot discord.				#
#	Voici le chemin du launcher en question :							#
#	/home/pi/VTTFounwetLauncher.py										#
#																		#
#########################################################################

import os
import subprocess as sbpr
import threading as thr

webApp = autoPianoFolder + "/" + autoPianoWebPy

os.chdir(autoPianoFolder)

def run(filename) :
	sbpr.run(["python3", filename])

threadWebApp = thr.Thread(target = run, args = (webApp,))

if launcher :
	if os.path.exists(webApp) :
		threadWebApp.start()
	else :
		print(f"LE PROGRAMME '{webApp}' N'EXISTE PAS\n")
else :
	pass
