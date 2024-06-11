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
				Nom du fichier :<br>
				
				<!--  -->
				
				<input class="optionButton" type="text" name="folderName" value="Nom du fichier">
				
				</p>
			
			<!-- Les boutons suivants servent à sélectionner un fichier et à l'envoyer au programme python -->
			
			<p>
				Créer dans :<br>
				<select name="lisFolders">
					{% for item in lisFolders %}
						<option value="{{ item }}">{{ item }}</option>
					{% endfor %}
				</select>
			</p>
			<p>
				<input class="optionButton" type="submit" name="move" value="Créer un dossier">
			</p></h4>
		</form>
		<form class="boxButton" method="POST" action="/">
			<input class="optionButton" type="submit" name="menu" value="Menu">		
		</form>
	</body>
</html>
