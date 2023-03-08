from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listen

from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv('POSTGRES_URL',  ''))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def engine_on_connect(dbapi_con, connection_record):
    print("New DBAPI connection:", dbapi_con)
    print("Databased Connected")

def engine_on_close(dbapi_con, connection_record):
    print("New DBAPI connection:", dbapi_con)
    print("Databased Disconnected")

listen(engine, "connect", engine_on_connect)
listen(engine, "close", engine_on_close)

Base = declarative_base()