# General Imports
from sqlalchemy import func
from sqlalchemy.orm import Session

# Custom Imports
from ..helpers import utils
from ..models.models import Weather


def load_weather_data(db: Session, weather_data):
    """Query to add weather data in database"""

    records = []
    for row in weather_data:
        records.append(
            Weather(
                record_id =  row["record_id"],
                timestamp = row["timestamp"],
                temperature = row["temperature"],
                humidity =  row["humidity"],
                wind_speed = row["wind_speed"]
            )
        )
    
    db.add_all(records)
    
    # Flushing to the Database
    db.flush()

    return len(records)


def analyze_weather_data(db: Session, parameter: str, start_date: str, end_date: str, stat: str):
    """Query to fetch basic statistics for the provided parameter"""

    # Adding date filters for the given date range
    filters = []
    filters.append(Weather.timestamp>=start_date)
    filters.append(Weather.timestamp<end_date)

    # Selecting column to be queried based on parameter received
    if parameter=="temperature":
        column = Weather.temperature
    elif parameter=="humidity":
        column = Weather.humidity
    else:
        column = Weather.wind_speed

    # Selecting Aggregate function to be used based on the stat provided
    if stat=="min":
        query = func.min(column).label(f"{stat}_{parameter}")
    elif stat=="max":
        query = func.max(column).label(f"{stat}_{parameter}")
    else:
        query = func.avg(column).label(f"{stat}_{parameter}")
    
    # Quering the requested column
    data = (
        db.query(
            query
        )
        .filter(
            *filters
        )
        .all()
    )

    return utils.to_array(data)
        

def fetch_data_for_plots(db: Session, start_date: str, end_date: str, parameter: str):
    """Query to fetch data for plots"""

    # Adding date filters for the given date range
    filters = []
    filters.append(Weather.timestamp>=start_date)
    filters.append(Weather.timestamp<end_date)

    # Selecting column to be queried based on parameter received
    if parameter=="temperature":
        column = Weather.temperature
    elif parameter=="humidity":
        column = Weather.humidity
    else:
        column = Weather.wind_speed

    # Query for Maximum 
    max_bar_plot = (
        db.query(
            func.max(column).label(f'max_{parameter}'),
            func.date(Weather.timestamp).label('timestamp')
        )
        .filter(*filters)
        .group_by(func.date(Weather.timestamp))
        .all()
    )
    
    # Query for Minimum
    min_bar_plot = (
        db.query(
            func.min(column).label(f'min_{parameter}'),
            func.date(Weather.timestamp).label('timestamp')
        )
        .filter(*filters)
        .group_by(func.date(Weather.timestamp))
        .all()
    )

    # Query for Average
    avg_line_plot = (
        db.query(
            func.avg(column).label(f'avg_{parameter}'),
            func.date(Weather.timestamp).label('timestamp')
        )
        .filter(*filters)
        .group_by(func.date(Weather.timestamp))
        .all()
    )

    return utils.to_array(max_bar_plot), utils.to_array(min_bar_plot), utils.to_array(avg_line_plot)
