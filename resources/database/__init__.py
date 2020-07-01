from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlengine = create_engine('sqlite:///database.sqlite')
Base = declarative_base()

from resources.database import models

Base.metadata.create_all(sqlengine)


Session = sessionmaker(bind=sqlengine)
sqlsession = Session()
