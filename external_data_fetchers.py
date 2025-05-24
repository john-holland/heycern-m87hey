import requests
import os
from typing import Dict, Any, Optional

# --- SETI Data Fetcher ---
def fetch_seti_data(ra: float, dec: float, radius: float = 0.1, start_time: Optional[str] = None, end_time: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch radio telescope metadata from the Breakthrough Listen Open Data Archive (SETI).
    Args:
        ra (float): Right ascension of the target (degrees)
        dec (float): Declination of the target (degrees)
        radius (float): Search radius (degrees)
        start_time (str): Optional start time (ISO format)
        end_time (str): Optional end time (ISO format)
    Returns:
        dict: Metadata for the requested region/time
    """
    # The Breakthrough Listen Open Data Archive provides a metadata CSV:
    # https://seti.berkeley.edu/opendata/metadata.csv
    # For demonstration, we download and filter the metadata
    import pandas as pd
    metadata_url = "https://seti.berkeley.edu/opendata/metadata.csv"
    try:
        df = pd.read_csv(metadata_url)
        # Filter by RA/DEC (simple box filter for demo)
        filtered = df[(df['ra'] >= ra - radius) & (df['ra'] <= ra + radius) &
                      (df['dec'] >= dec - radius) & (df['dec'] <= dec + radius)]
        if start_time:
            filtered = filtered[filtered['utc'] >= start_time]
        if end_time:
            filtered = filtered[filtered['utc'] <= end_time]
        return filtered.to_dict(orient='records')
    except Exception as e:
        return {"error": str(e)}

# --- NOAA Data Fetcher ---
def fetch_noaa_atmospheric_data(lat: float, lon: float, start_date: str, end_date: str, token: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch atmospheric data from NOAA's Climate Data Online API.
    Args:
        lat (float): Latitude
        lon (float): Longitude
        start_date (str): Start date (YYYY-MM-DD)
        end_date (str): End date (YYYY-MM-DD)
        token (str): NOAA API token (register at https://www.ncdc.noaa.gov/cdo-web/token)
    Returns:
        dict: Atmospheric data for the location and date range
    """
    headers = {"token": token or os.getenv("NOAA_API_TOKEN", "")}
    endpoint = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    params = {
        "datasetid": "GHCND",
        "datatypeid": "TAVG",
        "startdate": start_date,
        "enddate": end_date,
        "units": "metric",
        "limit": 1000,
        "includemetadata": "false",
        "locationcategoryid": "CITY",
        # Note: NOAA API does not support direct lat/lon, so this is a simplification
    }
    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- NWS Data Fetcher ---
def fetch_nws_weather_data(lat: float, lon: float) -> Dict[str, Any]:
    """
    Fetch real-time and forecast weather data from the National Weather Service API.
    Args:
        lat (float): Latitude
        lon (float): Longitude
    Returns:
        dict: Weather data for the location
    """
    # Step 1: Get the forecast office and gridpoint
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    try:
        points_resp = requests.get(points_url, timeout=10)
        points_resp.raise_for_status()
        points_data = points_resp.json()
        forecast_url = points_data['properties']['forecast']
        # Step 2: Get the forecast
        forecast_resp = requests.get(forecast_url, timeout=10)
        forecast_resp.raise_for_status()
        forecast_data = forecast_resp.json()
        return forecast_data
    except Exception as e:
        return {"error": str(e)} 