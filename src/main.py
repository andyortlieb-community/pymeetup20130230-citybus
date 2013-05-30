from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, request
from jinja2 import Template
import json

from datetime import datetime

class Constants:
    Version = '0.0.2'
    SupportedVersions = [ '0.0.1','0.0.2' ]

###
###     The Database...
###

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///./citybus.db", convert_unicode=True)
session = scoped_session(sessionmaker( autocommit=False, autoflush=False, bind=engine))


Model = declarative_base()
def _model_fromDict(self,source):
        for col in self.__table__.columns:
            setattr(self, col.name, source.get(col.name))
        return self
Model.fromDict = _model_fromDict
Model.toDict = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}
Model.query = session.query_property()

###
### Database Models
###

class BusRoute(Model):
    __tablename__ = "bus_route"
    id = Column(String(5), primary_key=True)
    busses = Column(Integer)



####
####    The flask app ....
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
    routes = [ route.toDict() for route in BusRoute.query.all() ]
    return json.dumps({
        'Success':True,
        'Data': routes
    })

@app.route('/v1/busroutes', methods=['POST'])
def busroutesPOST():
    route = BusRoute()
    route.fromDict(request.json)
    session.add(route)
    try:
        session.commit()
    finally:
        session.rollback()

    return json.dumps({
        'Success':True,
        'Data': route.toDict()
    })

@app.route('/v1/busroutes', methods=['PUT'])
def busroutesPUT():
    routeId = request.json.get('id')

    if routeId: 
        routeId = '%s'%routeId
        route = BusRoute.query.filter(BusRoute.id==routeId).all()

    else:
        route = False

    from pprint import pprint
    pprint(route)

    if not route: 
        return json.dumps({
            "Success": False,
            "Msg":"The requested object does not exist"
        }), 404
    
    route = route[0]

    route.fromDict(request.json)
    session.add(route)
    session.flush()

    return json.dumps({
        "Success":True,
        "Data":route.toDict()
    })

    

def SetupDB():
    # Delete the db file
    import os
    try:
        os.unlink('citybus.db')
    except OSError:
        pass # It's okay if the file doesn't exist. 

    # Create our database, add the models, etc.
    Model.metadata.create_all(bind=engine) 

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
    session.commit()
    #session.flush()

if __name__=='__main__':
    SetupDB()
    
    # Start up the web app
    app.run()
