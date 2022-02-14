from flask import Flask, render_template, request, redirect
from core import *
import requests as r
import sys

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/", methods = ['POST', 'GET'])
def index():
	return render_template('index.html')

@app.route('/results/', methods = ['POST', 'GET'])
@app.route('/results', methods = ['POST', 'GET'])
def data():
	form_data = request.form
	print(form_data)
	parola = request.form.get('parola')
	sinonimo = (request.form.get('sinonimo')) == "True"
	print(sinonimo)
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
