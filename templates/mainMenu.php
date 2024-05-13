<!DOCTYPE html>
<html>
	<head>
		<title>AutoPiano Music</title>
		<img src="/static/TitleAutoPiano.gif" alt="Logo AutoPiano" width=65px> 
		
	</head>
	
	<body>
		
		<link href="{{ url_for('static', filename='css/dropDown.css') }}" rel="stylesheet" type="text/css">
		 
		<!-- La ligne ci-dessus sert à demander au fichier CSS de "remodeler" l'affichage de notre page web -->
		
		<form method="POST" action="/play">
			<input type="submit" name="play" value="Jouer une musique">		
		</form>
		<form method="POST" action="/add">
			<input type="submit" name="add" value="Ajouter une musique">		
		</form>
		<form method="POST" action="/">
			<input type="submit" name="3th" value="Option3">		
		</form>
		<form method="POST" action="/">
			<input type="submit" name="4th" value="Option4">		
		</form>
	</body>
</html>
