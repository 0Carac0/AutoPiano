<!DOCTYPE html>
<html>
	<head>
		<title>AutoPiano Music</title>
		<img src="/static/TitleAutoPiano.gif" alt="Logo AutoPiano" width=65px>
		
	</head>
	
	<body>
		
		<link href="{{ url_for('static', filename='css/dropDown.css') }}" rel="stylesheet" type="text/css">
		 
		<!-- La ligne ci-dessus sert à demander au fichier CSS de "remodeler" l'affichage de notre page web -->
		
		<p class="">Choisissez une musique et appuyez sur "Jouer" !</p>
		<p>Les musiques sont actuellement {{ modeTxt }}.</p>
		<div id="play">
			
			<!-- En substance, la ligne ci-dessous dit "Dans mon bloc 'form', je vais renvoyer une information tout en redirigeant sur la page '.../music' quand l'utilisateur aura interagi" -->
			
			<form  method="POST" action="/music">
				<select name="select_music">
					
					<!-- Ci-dessous, nous ouvrons la porte au PHP avec les symboles '{' et '%', afin d'utiliser une boucle 'for' directement intégrée dans l'HTML
					Cette boucle sert à parcourir la variable 'data', que le fichier 'webMenu.py' nous a envoyée, afin d'ajouter chaque élément de cette variable à une liste déroulante
					(Ce type de liste est aussi appelé "drop down", d'où le nom du présent fichier) -->
					
					{% for item in data %}
						<option value="{{ item }}">{{ item }}</option>
					{% endfor %}
				</select>
				
				<!-- Maintenant que notre drop down contient chaque élément de 'data', nous allons ci-dessous créer un bouton qui permet de valider le choix fait par l'utilisateur
				et qui sera capable de renvoyer ce choix dans le programme 'webMenu.py' -->
				
				<input type="submit" value="Jouer">
			</form>
			
			<form method="POST" action="/settings">
				<input type="submit" name="setConv" value="Afficher les versions {{ buttonTxt }}">
			</form>
				
			
			<form method="POST" action="/">
				<input type="submit" name="menu" value="Menu">		
			</form>
			
		</div>
	</body>
</html>
