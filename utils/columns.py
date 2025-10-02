import pandas as pd
from pandas import DataFrame


def change_col_to_date_type(df: DataFrame, col_name: str):
    df[col_name] = pd.to_datetime(df[col_name], errors="coerce")
