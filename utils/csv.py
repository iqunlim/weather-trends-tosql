import pandas as pd
from pandas import DataFrame


def load_csv(path: str, na_values_list: list[str] = []) -> DataFrame:
    print(f"Loading csv from {path}...")
    if len(na_values_list) > 0:
        return pd.read_csv(path, na_values=na_values_list)
    return pd.read_csv(path)


def save_csv(path: str, df: DataFrame) -> None:
    print(f"Saving csv to {path}...")
    df.to_csv(path, index=False, encoding="utf-8")
