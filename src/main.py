from flask import Flask
from jinja2 import Template

app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
	return Template(open('./templates/home.html', 'r').read()).render()

if __name__=='__main__':
	app.run()
