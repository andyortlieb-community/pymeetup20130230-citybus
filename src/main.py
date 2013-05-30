from flask import Flask
from jinja2 import Template

from datetime import datetime

app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
	return Template(open('./templates/home.html', 'r').read()).render({
		'date': datetime.now(),
		'buscount': 32
	})

if __name__=='__main__':
	app.run()
