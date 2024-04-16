from flask import Flask, render_template
from markupsafe import escape
from flask import request
from os import *

muspathMIDI = str(path.normpath(getcwd() + sep + pardir)) + "/Musique_midi"
print (muspathMIDI)
#templatePath = str(getcwd()) + "/templates"
#print (templatePath)

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('xHtml_mainMenu.html')


@app.route('/play')
def play():
	return "<p>Pouf pouf playing thing</p>"

@app.route('/listedit')
def listedit():
	return "<p>Pouf pouf liste des musiques</p>"

@app.route('/howitworks')
def howitworks():
	return "<p>Pouf pouf tuto</p>"

if __name__ == '__main__' :
	app.run(debug=True, use_reloader=True)

