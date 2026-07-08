from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import urllib.parse

password = urllib.parse.quote_plus("minhduy@3304")

DB_URL = f"mysql+pymysql://root:{password}@localhost:3306/parking_db"

engine = create_engine(DB_URL)

Base = declarative_base()

LocalSesssion = sessionmaker(
    autoflush= False,
    bind= engine,
    expire_on_commit= False
)

def get_db():
    db = LocalSesssion()
    try:
        yield db
    finally:
        db.close()