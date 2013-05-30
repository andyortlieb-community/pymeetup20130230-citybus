from db import Model
from sqlalchemy import Column,Integer,String


###
### Database Models
###

class BusRoute(Model):
    __tablename__ = "bus_route"
    id = Column(String(5), primary_key=True)
    busses = Column(Integer)

