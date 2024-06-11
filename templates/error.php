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
		<h3>
		<p>{{ errType }}</p>
		</h3>
		<form class="boxButton" method="POST" action="/play">
			<input class="optionButton" type="submit" name="retour" value="Retour">		
		</form>
		<form class="boxButton" method="POST" action="/">
			<input class="optionButton" type="submit" name="menu" value="Menu">		
		</form>
		
	</body>
</html>
