<!DOCTYPE html>
<html>
	<head>
		<title>AutoPiano Music</title>
		<div class="bandeau">
			<img class="logo" src="/static/ETML_white.png" alt="ETML">
			<img class="logo" src="/static/TitleAutoPiano.gif" alt="Logo AutoPiano">
		</div>
		
	</head>
	
	<body>
		
		<link href="{{ url_for('static', filename='css/dropDown.css') }}" rel="stylesheet" type="text/css">
		 
		<!-- La ligne ci-dessus sert à demander au fichier CSS de "remodeler" l'affichage de notre page web -->
		<h3><p> {{ menuText }} </p></h3>
		
		<form class="boxButton" method="POST" action="/play">
			<input class="optionButton" type="submit" value="Jouer une musique">		
		</form>
		<form class="boxButton" method="POST" action="/addMusic">
			<input class="optionButton" type="submit" value="Ajouter une musique">		
		</form>
		<form class="boxButton" method="POST" action="/editMusicList">
			<input class="optionButton" type="submit" value="Réorganiser les fichiers">		
		</form>
		<form class="boxButton" method="POST" action="/createFolder">
			<input class="optionButton" type="submit" value="Créer un dossier de rangement">		
		</form>
	</body>
</html>
