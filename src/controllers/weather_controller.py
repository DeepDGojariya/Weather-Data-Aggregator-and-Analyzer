import io
import uuid
import zipfile
import pandas as pd
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
from fastapi import status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session


from ..models.models import Weather
from ..validators.validators import AnalyticsParams, VisualParams
from ..helpers import utils, constants
from ..managers import weather_manager


def draw_barplot(x_axis, y_axis, data):
    """Function to draw a barplot"""
    buf = io.BytesIO()
    plt.figure(figsize=(10,12))
    sns.barplot(x=x_axis, y=y_axis, data=data)
    plt.xticks(rotation=90)
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf


def draw_lineplot(x_axis, y_axis, data):
    """Function to draw a lineplot"""
    buf = io.BytesIO()
    plt.figure(figsize=(10,12))
    sns.lineplot(x=x_axis, y=y_axis, data=data, marker='o')
    plt.xticks(rotation=90)
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf


def load_weather_data(res: Response, db: Session):
    """Loads Historical Weather data of a location into the database."""
    try:
        # Calling the Weather API
        data = utils.call_weather_api()

        # Converting the response into a pandas Dataframe
        df = pd.DataFrame(data)

        weather_records = []
        
        # Iterating over Rows of the dataframe to prepare rows for batch insertion
        for _,row in df.iterrows():
            weather_records.append({
                "record_id":  f"WDT-{uuid.uuid4().hex[:constants.REM_UUID_LENGTH]}".upper(),
                "timestamp": datetime.fromisoformat(row["time"]),
                "temperature": row["temperature_2m"],
                "humidity":  row["relative_humidity_2m"],
                "wind_speed": row["wind_speed_10m"]
            })

        # Calling batch insert function
        row_count = weather_manager.load_weather_data(db, weather_records)
        
        # Committing the DB
        db.commit()
        print(f"{row_count} Rows Inserted into the Weather Table")
        
        # Setting status code for resonse
        res.status_code = status.HTTP_201_CREATED

        return "Successfully Ingested Weather Data"

    except Exception as e:
        db.rollback()
        print(f"Exception Occured: {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def analyze_weather_data(res: Response, params: AnalyticsParams, db: Session):
    """Function to fetch analysis of weather data based on certain params"""
    try:
        # Fetching all query parameters
        start_date = params.start_date
        end_date = params.end_date
        parameter = params.parameter
        stat = params.stat

        # Calling the database for fetching statistics
        weather_data_stats = weather_manager.analyze_weather_data(db, parameter, start_date, end_date, stat)
        
        # Creating the response object
        response_object = {}
        for row in weather_data_stats:
            response_object["start_date"] = start_date
            response_object["end_date"] = end_date
            response_object[f"{stat}_{parameter}"] = row[f"{stat}_{parameter}"]

        return response_object

    except Exception as e:
        print(f"Exception has occurred: {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def visualize_weather_data(res: Response, params: VisualParams, db: Session):
    """Function to create plots and send them across to client as a zip file."""
    try:
        zip_buf  = io.BytesIO()

        # Fetching all query parameters
        start_date = params.start_date
        end_date = params.end_date
        parameter = params.parameter
        
        # Fetching data required for plotting 
        max_plot_data, min_plot_data, avg_plot_data = weather_manager.fetch_data_for_plots(db, start_date, end_date, parameter)

        # Converting data received to dataframes
        df_max_plot = pd.DataFrame(max_plot_data)
        df_min_plot = pd.DataFrame(min_plot_data)
        df_avg_plot = pd.DataFrame(avg_plot_data)
        
        
        with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Create and Add each plot to a zip file
            zip_file.writestr(f'maximum_{parameter}.png', draw_barplot("timestamp", f"max_{parameter}", df_max_plot).getvalue())
            zip_file.writestr(f'minimum_{parameter}.png', draw_barplot("timestamp", f"min_{parameter}", df_min_plot).getvalue())
            zip_file.writestr(f'average_{parameter}.png', draw_lineplot("timestamp", f"avg_{parameter}", df_avg_plot).getvalue())
        
        zip_buf.seek(0)
        

        def iterfile():
            """Generator to yield bytes from the in-memory zip buffer"""
            yield from zip_buf
            zip_buf.close()
        
        return StreamingResponse(
            iterfile(),
            media_type='application/zip', 
            headers={'Content-Disposition': 'attachment; filename="plots.zip"'}
        )  

    except Exception as e:
        print(f"Exception has occurred: {e}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR
