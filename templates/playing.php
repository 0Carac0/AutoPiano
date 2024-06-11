<!DOCTYPE html>
<html>
	<head>
		<title>AutoPiano Playing</title>
		<div class="bandeau">
			<img class="logo" src="/static/ETML_white.png" alt="ETML">
			<img class="logo" src="/static/TitleAutoPiano.gif" alt="Logo AutoPiano">
		</div>
		<link href="{{ url_for('static', filename='css/dropDown.css') }}" rel="stylesheet" type="text/css">
	</head>
	<body>
		
		<h3><p>Actuellement en train de jouer :</p>
		<p>{{data}}</p></h3>
		<form class="boxButton" method="POST" action="/stop">
			<input class="optionButton" type="submit" name="stop_music" value="Retour">		
		</form>
	</body>
</html>
