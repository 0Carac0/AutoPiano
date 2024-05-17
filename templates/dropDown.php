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
		<p>Choisissez une musique et appuyez sur "Jouer" !</p>
		</h3>
		<p>Les musiques sont actuellement {{ modeTxt }}.</p>
		<div id="play">
			
			<!-- En substance, la ligne ci-dessous dit "Dans mon bloc 'form', je vais renvoyer une information tout en redirigeant sur la page '.../music' quand l'utilisateur aura interagi" -->
			
			<form  method="POST" action="/music">
				<p>
					<select name="select_music">
						
						<!-- Ci-dessous, nous ouvrons la porte au PHP avec les symboles '{' et '%', afin d'utiliser une boucle 'for' directement intégrée dans l'HTML
						Cette boucle sert à parcourir la variable 'data', que le fichier 'webMenu.py' nous a envoyée, afin d'ajouter chaque élément de cette variable à une liste déroulante
						(Ce type de liste est aussi appelé "drop down", d'où le nom du présent fichier) -->
						
						{% for item in data %}
							<option value="{{ item }}">{{ item }}</option>
						{% endfor %}
					</select>
				</p>
				
				<!-- Maintenant que notre drop down contient chaque élément de 'data', nous allons ci-dessous créer un bouton qui permet de valider le choix fait par l'utilisateur
				et qui sera capable de renvoyer ce choix dans le programme 'webMenu.py' -->
				
				<p>
					<input class="optionButton" type="submit" value="Jouer">
				</p>
			</form>
			
		</div>
		
		<form class="boxButton" method="POST" action="/settings">
			<input class="optionButton" type="submit" name="setConv" value="Afficher les versions {{ buttonTxt }}">
		</form>
			
		
		<form class="boxButton" method="POST" action="/">
			<input class="optionButton" type="submit" name="menu" value="Menu">		
		</form>
		
	</body>
</html>
