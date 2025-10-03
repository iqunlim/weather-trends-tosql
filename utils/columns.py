import re
import numpy as np
import pandas as pd
from pandas import DataFrame


def change_col_to_date_type(df: DataFrame, col_name: str):
    df[col_name] = pd.to_datetime(df[col_name], errors="coerce")


COMPASS_DIR = [
    "North",
    "North-Northeast",
    "Northeast",
    "East-Northeast",
    "East",
    "East-Southeast",
    "Southeast",
    "South-Southeast",
    "South",
    "South-Southwest",
    "Southwest",
    "West-Southwest",
    "West",
    "West Northwest",
    "Northwest",
    "North-Northwest",
]


# https://www.campbellsci.com/blog/convert-wind-directions
# extremely helpful blog post, translating degrees to array indicies
def transform_wind_angle_to_direction(dir: float):

    # Normalize degrees
    degree = dir % 360
    # 16 directions = 360 / 16 to get each point
    compass_angle = 360.0 / 16

    arr_index = (
        int((degree + compass_angle / 2) // compass_angle) % 16
    )  # 16 == compass directions

    return COMPASS_DIR[arr_index]


def camel_to_sql_valid_snake(name: str) -> str:
    # Strip leading and trailing
    # Lowercase it all
    name = name.strip().lower()
    # Sub out all characters that are disallowed to be in column names
    # which is pretty much all of them that arent "_"
    name = re.sub(r"[^a-z0-9]+", "_", name)
    # Remove leading digits, as SQL does not allow them either
    name = re.sub(r"^[0-9]+", "", name)
    return name
