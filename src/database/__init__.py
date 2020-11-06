from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlengine = create_engine('sqlite:///data/database.sqlite')
Base = declarative_base()

from src.database import models  # noqa: F401, E402

Base.metadata.create_all(sqlengine)


Session = sessionmaker(bind=sqlengine)
sqlsession = Session()
