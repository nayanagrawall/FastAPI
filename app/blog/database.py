from sqlalchemy import create_engine  # Creating engine to make connection with our database
from sqlalchemy.ext.declarative import declarative_base  # this is used to declare a mapping
from sqlalchemy.orm import sessionmaker  # used for creating a session

SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=
{"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
