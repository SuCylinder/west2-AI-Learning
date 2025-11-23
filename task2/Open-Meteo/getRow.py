import requests
import pandas
from pathlib import Path
import json

api = "https://historical-forecast-api.open-meteo.com/v1/forecast"

params = {
	"latitude": 26.05942,
	"longitude": 119.198,
	"start_date": "2024-01-01",
	"end_date": "2024-12-31",
	"daily": ["temperature_2m_max", "temperature_2m_mean", "temperature_2m_min", "precipitation_sum", "sunshine_duration"],
	"hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "cloud_cover", "weather_code", "wind_speed_10m", "wind_direction_10m", "shortwave_radiation_instant", "is_day"],
}

response = requests.get(api,params=params)

a= response.json()

path = Path(__file__).parent / "data_row.json"

with open(path,"w") as f:
    json.dump(a,f)