# General Imports
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, Depends


# Custom Imports
from ..database import get_db_connection
from ..controllers import weather_controller
from ..validators.validators import AnalyticsParams, VisualParams


router = APIRouter()


@router.post("/weather-data")
def load_weather_data(
    res: Response,
    db: Session = Depends(get_db_connection)
):
    """Route to ingest historical weather data"""
    return weather_controller.load_weather_data(res, db)


@router.get("/analytics")
def analyze_weather_data(
    res: Response,
    params: AnalyticsParams = Depends(AnalyticsParams),
    db: Session = Depends(get_db_connection)
):
    """Route to fetch statistical analysis of the weather data"""
    return weather_controller.analyze_weather_data(res, params, db)


@router.get("/visualization")
def visualize_weather_data(
    res: Response,
    params: VisualParams = Depends(VisualParams),
    db: Session = Depends(get_db_connection)
):
    """Route to plot visualizations of weather data"""
    return weather_controller.visualize_weather_data(res, params, db)
