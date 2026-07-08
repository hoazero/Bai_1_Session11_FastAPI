from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "mysql+pymysql://root:123456@localhost:3306/parking_db"

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