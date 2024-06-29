# General Imports
from fastapi import APIRouter

# Custom Imports
from . import weather_router

app_router = APIRouter(tags=["Weather App"])

# Including the Weather router
app_router.include_router(router=weather_router.router)