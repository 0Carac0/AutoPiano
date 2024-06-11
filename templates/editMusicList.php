<!DOCTYPE html>
<html>
	<head>
		<title>AutoPiano EditMusicList</title>
		<div class="bandeau">
			<img class="logo" src="/static/ETML_white.png" alt="ETML">
			<img class="logo" src="/static/TitleAutoPiano.gif" alt="Logo AutoPiano">
		</div>
		<link href="{{ url_for('static', filename='css/dropDown.css') }}" rel="stylesheet" type="text/css">
	</head>
	<body>
		
		<h3><p>Rangement des musiques</p></h3>
		
		<form method="POST" action="/edited" enctype="multipart/form-data">
			<h4><p>
				Fichier à déplacer :<br>
				
				<!-- Le 'select' ci-après sert à sélectionner, parmi les fichiers '.mid.', la musique à déplacer -->
				
				<select name="lisMusic">
					{% for item in lisMusic %}
						<option value="{{ item }}">{{ item }}</option>
					{% endfor %}
				</select>
			</p>
			
			<!-- Les boutons suivants servent à sélectionner un fichier et à l'envoyer au programme python -->
			
			<p>
				Destination :<br>
				<select name="lisFolders">
					{% for item in lisFolders %}
						<option value="{{ item }}">{{ item }}</option>
					{% endfor %}
					<option value="SUPPRIMER_LE_FICHIER">Corbeille (SUPPRIMER LE FICHIER)</option>
				</select>
			</p>
			<p>
				<input class="optionButton" type="submit" name="move" value="Déplacer le fichier">
			</p></h4>
		</form>
		<form class="boxButton" method="POST" action="/">
			<input class="optionButton" type="submit" name="menu" value="Menu">		
		</form>
	</body>
</html>
