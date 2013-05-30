from flask import Flask
from jinja2 import Template
import json

from datetime import datetime

app = Flask(__name__)
app.debug = True

class Constants:
	Version = '0.0.2'
	SupportedVersions = [ '0.0.1','0.0.2' ]


@app.route('/')
def home():
	return Template(open('./templates/home.html', 'r').read()).render({
		'date': datetime.now(),
		'buscount': 32
	})

@app.route('/version/')
def version():
	return json.dumps({ 
		'Success':True,
		'Data': {
			'Version':Constants.Version,
			'SupportedVersions':Constants.SupportedVersions
		}
	})

if __name__=='__main__':
	app.run()
