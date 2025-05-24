import json
import os
from datetime import datetime, timedelta
from external_data_fetchers import fetch_seti_data, fetch_noaa_atmospheric_data, fetch_nws_weather_data

# Example target: M87 (RA/DEC)
m87_ra = 187.70593075
m87_dec = 12.3911231

# Example observatory location (San Francisco, CA)
lat, lon = 37.7749, -122.4194

# Date range for atmospheric data (last 24 hours)
end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=1)

# NOAA API token (set as env var or paste here)
NOAA_API_TOKEN = os.getenv("NOAA_API_TOKEN", "")

# Output directory
output_dir = "external_data"
os.makedirs(output_dir, exist_ok=True)

def main():
    print("Extracting SETI data...")
    seti_data = fetch_seti_data(m87_ra, m87_dec, radius=0.2)
    with open(os.path.join(output_dir, "seti_data.json"), "w") as f:
        json.dump(seti_data, f, indent=2)
    print("SETI data saved.")

    print("Extracting NOAA atmospheric data...")
    noaa_data = fetch_noaa_atmospheric_data(
        lat, lon, start_date=start_date.isoformat(), end_date=end_date.isoformat(), token=NOAA_API_TOKEN)
    with open(os.path.join(output_dir, "noaa_data.json"), "w") as f:
        json.dump(noaa_data, f, indent=2)
    print("NOAA data saved.")

    print("Extracting NWS weather data...")
    nws_data = fetch_nws_weather_data(lat, lon)
    with open(os.path.join(output_dir, "nws_data.json"), "w") as f:
        json.dump(nws_data, f, indent=2)
    print("NWS data saved.")

    print("ETL complete! Data available in the 'external_data' directory.")

if __name__ == "__main__":
    main() 