###
###     The Database...
###

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///./citybus.db", convert_unicode=True)
session = scoped_session(sessionmaker( autocommit=False, autoflush=False, bind=engine))


Model = declarative_base()
def _model_fromDict(self,source):
        for col in self.__table__.columns:
            setattr(self, col.name, source.get(col.name))
        return self
Model.fromDict = _model_fromDict

def _model_toDict(self):
        output = {}
        for col in self.__table__.columns:
            output[col.name] = getattr(self, col.name)
        return output

Model.toDict = _model_toDict
Model.query = session.query_property()