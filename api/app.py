from flask import Flask, render_template, request, redirect
from core import *
import requests as r
import sys

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/", methods = ['POST', 'GET'])
def index():
	return render_template('index.html')

@app.route('/sininomiecontrari/', methods = ['POST', 'GET'])
@app.route('/sinonimiecontrari', methods = ['POST', 'GET'])
def sinecon():
	form_data = request.form
	print(form_data)
	parola = request.form.get('parola')
	sinonimo = (request.form.get('sinonimo')) == "True"
	livello = int(request.form.get('level'))
	if parola == '':
		return render_template('error.html', e="Non hai inserito una parola")
	try:
		w = getWords([], parola, 0, livello, sinonimo)
	except Exception as e:
		return render_template('error.html', e=e)
	try:
		return render_template('results.html', words=w, livello=livello)
	except Exception as e:
		return render_template('error.html', e=e)

@app.route('/intersezione/', methods = ['POST', 'GET'])
@app.route('/intersezione', methods = ['POST', 'GET'])
def intersection():
	form_data = request.form
	print(form_data)

	parole = request.form.get('parole')
	estendere = (request.form.get('estendi')) == "on"
	livello = int(request.form.get('level'))
	precisione = int(request.form.get('precisione'))
	
	if parole == '':
		return render_template('error.html', e="Non hai inserito una parola")
	try:
		i = findIntersection(parole, precisione, livello)
		if estendere:
			estensione = int(request.form.get('estensione'))
			for w in i:		
				i = getWords(i, w[0], w[1], estensione, True)
				print("Extending")


	except Exception as e:
		return render_template('error.html', e=e)
	try:
		return render_template('results.html', words=i, livello=livello)
	except Exception as e:
		print(i)
		if not len(i):
			return render_template('warning.html', e=e)
		else:
			return render_template('error.html', e=e)



if __name__ == "__main__":
    if '--secure' in sys.argv:
        app.config['TESTING'] = False
        app.config['PREFERRED_URL_SCHEME'] = 'https'
        @app.before_request
        def before_request():
            if not request.is_secure:
                url = request.url.replace('http://', 'https://', 1)
                code = 301
                return redirect(url, code=code)
        app.run(host="0.0.0.0", ssl_context=('certificates/fullchain1.pem', 'certificates/privkey1.pem'))
    else:
        print("Running Locally")
        app.run(host="0.0.0.0")
