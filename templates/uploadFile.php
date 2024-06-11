<!DOCTYPE html>
<html>
	<head>
		<title>AutoPiano AddMusic</title>
		<div class="bandeau">
			<img class="logo" src="/static/ETML_white.png" alt="ETML">
			<img class="logo" src="/static/TitleAutoPiano.gif" alt="Logo AutoPiano">
		</div>
		<link href="{{ url_for('static', filename='css/dropDown.css') }}" rel="stylesheet" type="text/css">
	</head>
	<body>
		
		<h3><p>Ajout de musique</p></h3>
		
		<form method="POST" action="/upload" enctype="multipart/form-data">
			<h4><p>
				Dossier d'enregistrement :<br>
				
				<!-- Le 'select' ci-après sert à sélectionner, parmi les dossiers existants, l'emplacement dans lequel enregistrer la musique -->
				
				<select name="uploadFolder">
					{% for item in data %}
						<option value="{{ item }}">{{ item }}</option>
					{% endfor %}
				</select>
			</p>
			
			<!-- Les boutons suivants servent à sélectionner un fichier et à l'envoyer au programme python -->
			
			<p>
				Fichier à ajouter (format '.mid' uniquement) :<br>
				<input class="optionButton" type="file" action="" name="file">
			</p>
			<p>
				<input class="optionButton" type="submit" value="Ajouter la musique">
			</p></h4>
		</form>
		<form class="boxButton" method="POST" action="/">
			<input class="optionButton" type="submit" name="menu" value="Menu">		
		</form>
	</body>
</html>
