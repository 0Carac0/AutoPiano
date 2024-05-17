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
		
		<h3><p>File upload</p></h3>
		<h2><p>{{data}}</p></h2>
		<form method="POST" action="/upload" enctype="multipart/form-data">
			<p>
				<input class="optionButton" type="file" action="" name="file">
				<input class="optionButton" type="submit" value="Submit">
			</p>
		</form>
		<form class="boxButton" method="POST" action="/">
			<input class="optionButton" type="submit" name="menu" value="Menu">		
		</form>
	</body>
</html>
