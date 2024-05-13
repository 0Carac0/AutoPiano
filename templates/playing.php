<!DOCTYPE html>
<html>
	<head>
		<title>AutoPiano Playing</title>
		<img src="/static/TitleAutoPiano.gif" alt="Logo AutoPiano" width=65px>
		<link href="{{ url_for('static', filename='css/dropDown.css') }}" rel="stylesheet" type="text/css">
	</head>
	<body>
		
		<form method="POST" action="/stop">
			<h3><p>Actuellement en train de jouer :</p></h3>
			<h2><p>{{data}}</p></h2>
			<input type="submit" name="stop_music" value="Retour">		
		</form>
	</body>
</html>
