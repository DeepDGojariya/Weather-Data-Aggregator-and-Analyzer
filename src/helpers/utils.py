# General Imports
import requests

# Custom imports
from .constants import (
    WEATHER_API_URL, 
    LATITUDE_MUMBAI, 
    LONGITUDE_MUMBAI, 
    START_DATE, 
    END_DATE, 
    PARAMETERS
)


def call_weather_api():
    """Function to call weather API"""

    query_params = f"latitude={LATITUDE_MUMBAI}&longitude={LONGITUDE_MUMBAI}&start_date={START_DATE}&end_date={END_DATE}&hourly={PARAMETERS}"
    url = f"{WEATHER_API_URL}?{query_params}"
    
    response = requests.get(url)
    
    # Converting response to JSON
    response = response.json()
    data = response['hourly']
    
    return data
    

def to_array(data):
    """Function to convert Query response to array"""
    return [row._asdict() for row in data]
