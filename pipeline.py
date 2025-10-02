from dotenv import load_dotenv
import os
from pandas import DataFrame
import requests

from utils.json import VALID_JSON_TYPES, to_json, read_json

# from utils import to_json
from datetime import datetime, timedelta


def load_env_vars() -> dict[str, str]:

    env_vars = {
        "api_url": os.getenv("API_URL"),
        "db_path": os.getenv("DATABASE_PATH"),
        "api_key": os.getenv("API_KEY"),
    }

    for key, val in env_vars.items():
        if val == None or val == "":
            msg = f"Error: Missing environment variable {key}"
            raise EnvironmentError(msg)

    return env_vars  # type: ignore


def extract(source: str, key: str, num_days=7) -> VALID_JSON_TYPES:
    """Fetches data from the API and returns the raw data (JSON/list)."""
    # Put API requests and initial JSON loading here.
    data = {}
    data["daily_summary"] = []
    for i in range(1, num_days + 1):
        current = datetime.today() - timedelta(days=i)

        querystring = {
            "lat": 32.9552598,
            "lon": -97.0155703,
            "date": current.strftime("%Y-%m-%d"),
            "units": "imperial",
            "appid": key,
        }

        response = requests.get(source, params=querystring)
        response.raise_for_status()
        data["daily_summary"].append(response.json())

    data["count_days"] = num_days
    return data


def transform(raw_data: VALID_JSON_TYPES) -> DataFrame:
    """Performs all necessary cleaning and processing on the data."""
    # Returns the clean DataFrame.
    print(raw_data)
    pass


def load(clean_df: DataFrame, db_file: str, table_name: str) -> None:
    """Connects to the database and loads the data."""
    # Loads the clean_df to SQLite using df.to_sql().
    print("Load")
    pass


def main():
    """Coordinates the ETL pipeline by calling extract -> transform -> load."""
    env_vars = load_env_vars()

    # data = extract(env_vars["api_url"], env_vars["api_key"])
    data = read_json("response.json")
    df = transform(data)
    load(df, env_vars["db_path"], "weather_sevendays")


if __name__ == "__main__":
    load_dotenv()
    main()
