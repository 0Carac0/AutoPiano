<!DOCTYPE html>
<html>
	<head>
		<title>AutoPiano Play</title>
	</head>
	<body>
		<p>Choisissez une musique et appuyez sur "Jouer" !</p>
		<div id="play">
			<form  method="POST" action="/music">
				<select name="select_music">
					{% for item in data %}
					
						<option value="{{ item }}">{{ item }}</option>
					{% endfor %}
				</select>
				<input type="submit" value="Jouer">
			</form>
		</div>
		
	</body>
</html>
