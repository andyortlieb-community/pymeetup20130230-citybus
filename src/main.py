from db import Model, engine, session
from models import BusRoute
import app
import endpoints
import views

__all__=['endpoints','views']

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
    app.app.run()
