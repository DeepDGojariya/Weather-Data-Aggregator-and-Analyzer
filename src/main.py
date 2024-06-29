from fastapi import FastAPI, Request, status
from .database import Base, engine
from .routes import app_router


# Create all models as tables in the Database
Base.metadata.create_all(engine)

# Initialize Fast API Application
app = FastAPI(title="Weather App")

# Include App Router
app.include_router(app_router.app_router)