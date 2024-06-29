# General Imports
from sqlalchemy import String, Column, DateTime, Float

# Custom Imports
from ..database import Base

class Weather(Base):
    """Weather Model"""
    
    __tablename__ = "weather"
    
    record_id = Column(String(32), primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
