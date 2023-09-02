from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#For Sqlite3
#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
#check_same_thread:
# If True (default), ProgrammingError will be raised if the database connection is used by
# a thread other than the one that created it. 
# If False, the connection may be accessed in multiple threads; 
# write operations may need to be serialized by the user to avoid data corruptio
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

#For PostgreSQL
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:thesuperfancypass@localhost/TodoApplicationDatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URL)



#To avoid database transactions doing things automatically
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()