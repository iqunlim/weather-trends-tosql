from dotenv import load_dotenv
import os
import requests

from utils.json import VALID_JSON_TYPES

# from utils import to_json


def extract(source: str, query_params: dict[str, str]):
    """Fetches data from the API and returns the raw data (JSON/list)."""
    # Put API requests and initial JSON loading here.
    querystring = {}
    pass


def transform(raw_data: dict[str, VALID_JSON_TYPES]):
    """Performs all necessary cleaning and processing on the data."""
    # Returns the clean DataFrame.
    print("Transform")
    pass


def load(clean_df, db_file, table_name):
    """Connects to the database and loads the data."""
    # Loads the clean_df to SQLite using df.to_sql().
    print("Load")
    pass


def main():
    """Coordinates the ETL pipeline by calling extract -> transform -> load."""

    data = extract(os.getenv("API_URL"))
    df = transform(data)
    load(df, os.getenv("DATABASE_PATH"), "weather_sevendays")


if __name__ == "__main__":
    load_dotenv()
    main()
