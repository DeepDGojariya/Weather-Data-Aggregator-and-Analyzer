# General Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define Database URL
DATABASE_URL = "sqlite:///./weather_db.db"

# Create Database Engine
engine = create_engine(DATABASE_URL)

# Create A Database Session
SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)
Base = declarative_base()


def get_db_connection():
    """Function to get DB Connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
