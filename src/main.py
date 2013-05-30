from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, request
from jinja2 import Template
import json

from datetime import datetime

class Constants:
    Version = '0.0.2'
    SupportedVersions = [ '0.0.1','0.0.2' ]

    @classmethod
    def toDict(cls):
        return {
            'Version':cls.Version,
            'SupportedVersions':cls.SupportedVersions
        }

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


###
###     Our REST API
###

# Just a base class, not terribly useful.
class REST:
    def render(self):
        return json.dumps({"Success":None}),204

class Success(REST):

    def __init__(self, data=None):
        if data: self.data = data

    def render(self):
        output = {"Success":True}
        if hasattr(self, 'data') and self.data:

            # Is it a single model?
            if isinstance(self.data, Model):
                output['Data'] =  self.data.toDict()
    
            # Does our data have a toDict() for us?
            if hasattr(self.data,'toDict'):
                output['Data'] = self.data.toDict()

            elif isinstance(self.data, list):
                output['Data'] = [ model.toDict() for model in self.data ] 

            else:
                output['Data'] = None

        return json.dumps(output),200

class NotFound(REST):
    def __init__(self,msg="The item was not found"):
        self.msg = msg

    def render(self):
        return json.dumps({
            'Success': False,
            'Msg':self.msg
        }),404


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
    return Success(Constants).render()


@app.route('/v1/busroutes', methods=['GET'])
def busroutes():
    routes = BusRoute.query.all()
    if (routes):
        return Success(routes).render()
    return NotFound().render()


@app.route('/v1/busroutes', methods=['POST'])
def busroutesPOST():
    route = BusRoute()
    route.fromDict(request.json)
    session.add(route)
    try:
        session.commit()
    finally:
        session.rollback()

    return Success(route).render()


@app.route('/v1/busroutes', methods=['PUT'])
def busroutesPUT():
    routeId = request.json.get('id')

    if routeId: 
        routeId = '%s'%routeId
        route = BusRoute.query.filter(BusRoute.id==routeId).all()

    else:
        route = False

    if not route: 
        return NotFound().render()
    
    route = route[0]

    route.fromDict(request.json)
    session.add(route)
    session.flush()

    return Success(route).render()
    

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
