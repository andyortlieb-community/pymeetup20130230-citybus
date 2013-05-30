from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from jinja2 import Template
import json

from datetime import datetime

class Constants:
	Version = '0.0.2'
	SupportedVersions = [ '0.0.1','0.0.2' ]

###
### 	The Database...
###

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./citybus.db")
#engine = create_engine("sqlite:///:memory:")
metadata = MetaData()
Model = declarative_base(metadata=metadata)
Model.toDict = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}
session = sessionmaker()
session.configure(bind=engine)
session = session()

###
###	Database Models
###

class BusRoute(Model):
	__tablename__ = "bus_route"
	id = Column(String(5), primary_key=True)
	busses = Column(Integer)



####
####	The flask app ....
####

app = Flask(__name__)
app.debug = True

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

@app.route('/v1/busroutes', methods=['GET'])
def busroutes():
	routes = [ route.toDict() for route in session.query(BusRoute).all() ]
	return json.dumps({
		'Success':True,
		'Data': routes
	})

def SetupDB():
	# Delete the db file
	import os
	try:
		os.unlink('citybus.db')
	except OSError:
		pass # It's okay if the file doesn't exist. 

	# Create our database, add the models, etc.
 	metadata.create_all(engine)		

	# Add a couple bus routes
	bus201 = BusRoute()
	bus201.id = '201'
	bus201.busses = 17

	bus211 = BusRoute()
	bus211.id = '221'
	bus211.busses = 30

	bus315 = BusRoute()
	bus315.id = '315'
	bus315.busses = 12
	
	session.add(bus201)
	session.add(bus211)
	session.add(bus315)
	#session.commit()

if __name__=='__main__':
	SetupDB()
	
	# Start up the web app
	app.run()
