# General Imports
from datetime import datetime
from enum import Enum
from typing import Optional


class ParameterType(str, Enum):
    """Enum for Parameter Type"""
    temperature = "temperature"
    humidity = "humidity"
    wind_speed = "wind_speed"

class StatType(str, Enum):
    """Enum for Statistic Type"""
    average = "avg"
    minimum = "min"
    maximum = "max"

class AnalyticsParams():
    """Class for Analytics API Query Params"""
    def __init__(
            self, 
            start_date: str, 
            parameter: ParameterType, 
            stat: StatType, 
            end_date: Optional[str] = datetime.utcnow().strftime("%Y-%m-%d")
        ):
        
        self.start_date = start_date
        self.parameter = parameter
        self.stat = stat
        self.end_date = end_date
        

class VisualParams():
    """Class for Visualization API Query Params"""
    def __init__(
            self, 
            start_date: str, 
            parameter: ParameterType, 
            end_date: Optional[str] = datetime.utcnow().strftime("%Y-%m-%d")
        ):

        self.start_date = start_date
        self.parameter = parameter
        self.end_date = end_date
        