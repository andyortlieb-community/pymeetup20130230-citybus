from jinja2 import Template
from datetime import datetime
from app import app

@app.route('/')
def home():
    return Template(open('./templates/home.html', 'r').read()).render({
        'date': datetime.now(),
        'buscount': 32
    })

