import pandas as pd
from pandas import DataFrame


def normalize_field(df: DataFrame, field: str) -> None:
    df[field] = df[field].str.lower().str.strip()
