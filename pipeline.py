import argparse
import sqlite3
from dotenv import load_dotenv
import os
from pandas import DataFrame
import pandas as pd
import requests
from tqdm import tqdm

from utils.json import VALID_JSON_TYPES, read_json
from utils.columns import (
    camel_to_sql_valid_snake,
    transform_wind_angle_to_direction,
)

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


def cronstruct_argparse():
    parser = argparse.ArgumentParser(description="Steam Random Game Sampler")

    parser.add_argument(
        "-t",
        "--temp",
        type=int,
        default=90,
        help="Pull data with a high of {temperature}. Defaults to 90.",
    )

    parser.add_argument(
        "-d",
        "--days",
        type=int,
        default=30,
        help="Pull # of previous days. Defaults to 30 days.",
    )

    return parser


def extract(source: str, key: str, num_days) -> VALID_JSON_TYPES:
    """Fetches data from the API and returns the raw data (JSON/list)."""
    # Put API requests and initial JSON loading here.
    data = {}
    data["daily_summary"] = []

    print("Loading Data from API...")
    for i in tqdm(range(1, num_days + 1)):
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

    return data


def transform(raw_data, min_temp=90) -> DataFrame:
    print("Transforming data. See Readme for details...")
    """Performs all necessary cleaning and processing on the data."""
    # Returns the clean DataFramedef extract(source: str, key: str, num_days=7) -> VALID_JSON_TYPES:
    """Fetches data from the API and returns the raw data (JSON/list)."""
    # Put API requests and initial JSON loading here.
    data = {}
    data["daily_summary"] = []

    df = pd.json_normalize(raw_data, record_path="daily_summary", sep="_")
    # normalize col names
    df.columns = [camel_to_sql_valid_snake(col) for col in df.columns]
    # Clear out unneeded fields
    df = df.drop(["units", "lat", "lon", "tz"], axis=1)
    mapper = {"wind_max_direction": "wind_direction", "wind_max_speed": "wind_speed"}

    df = df.rename(columns=mapper)

    # sort by date ascending
    df = df.sort_values(by="date", ascending=True)

    # bind it to the minimum temperature, we only want whats above
    df = df[df["temperature_max"] > min_temp]

    # convert wind by degrees to an actual direction
    df["wind_direction"] = df["wind_direction"].apply(
        lambda x: transform_wind_angle_to_direction(x)
    )

    return df


def load(clean_df: DataFrame, db_file: str, table_name: str) -> None:
    """Connects to the database and loads the data."""
    # Loads the clean_df to SQLite using df.to_sql().
    print("Loading Data to Database...")
    with sqlite3.connect(db_file) as conn:
        clean_df.to_sql(name=table_name, con=conn, if_exists="replace", index=False)


def main():
    parser = cronstruct_argparse()
    args = parser.parse_args()
    """Coordinates the ETL pipeline by calling extract -> transform -> load."""
    env_vars = load_env_vars()
    data = extract(env_vars["api_url"], env_vars["api_key"], num_days=args.days)
    df = transform(data, min_temp=args.temp)
    load(df, env_vars["db_path"], "weather_sevendays")


if __name__ == "__main__":
    print("Weather Data Loading Script")
    load_dotenv()
    main()
