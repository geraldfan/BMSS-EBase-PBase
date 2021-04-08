# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:26:22 2020

@author: Gerald
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Change the file name if using a different database
engine = create_engine('sqlite:///EBase.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """Initializes the database"""
    import data
    import settings
    Base.metadata.create_all(bind=engine)