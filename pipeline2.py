import os
import sqlite3
from dotenv import load_dotenv
import pandas as pd
import kagglehub
from pandas import DataFrame

from utils.columns import camel_to_sql_valid_snake
import argparse

COLS = [
    "AppID",
    "Name",
    "Release date",
    "Estimated owners",
    "Peak CCU",
    "Required age",
    "Price",
    "BAD_ROW",
    "DiscountDLC count",
    "About the game",
    "Supported languages",
    "Full audio languages",
    "Reviews",
    "Header image",
    "Website",
    "Support url",
    "Support email",
    "Windows",
    "Mac",
    "Linux",
    "Metacritic score",
    "Metacritic url",
    "User score",
    "Positive",
    "Negative",
    "Score rank",
    "Achievements",
    "Recommendations",
    "Notes",
    "Average playtime forever",
    "Average playtime two weeks",
    "Median playtime forever",
    "Median playtime two weeks",
    "Developers",
    "Publishers",
    "Categories",
    "Genres",
    "Tags",
    "Screenshots",
    "Movies",
]


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
        "-n",
        "--count",
        type=int,
        default=10,
        help="Count of steam games to sample from dataset. Defaults to 10.",
    )

    return parser


def extract() -> DataFrame:

    # Download latest version
    path = kagglehub.dataset_download("fronkongames/steam-games-dataset")
    df = pd.read_csv(path + "/games.csv", index_col=None, header=0, names=COLS)
    print(df.columns)
    return df


def transform(df: DataFrame, sample_size=10) -> DataFrame:

    # take a random amount of sample size n
    df = df.sample(n=sample_size)
    # sort values by app id, since they are now all over the place after the random sample
    df = df.sort_values("AppID")
    # then reset the index, so now the indicies are more ordered
    df = df.reset_index(drop=True)

    # Normalize col names
    df.columns = [camel_to_sql_valid_snake(col) for col in df.columns]

    # combine the two that were causing csv issues:
    df["achievements"] = df["achievements"] + "," + df["bad_row"]

    # Clear out unnecessary rows that we do not need
    df = df.drop(["movies", "screenshots", "bad_row", "user_score"], axis=1)

    # filter adult games
    # the ~ is a bitwise reverse operator, flipping it from 1 to 0
    df = df[~(df["tags"].str.contains("Nudity"))]

    # drop games with no bad reviews and no good reviews
    df = df[(df["positive"] != 0) | (df["negative"] != 0)]

    # ...etc
    return df


def load(clean_df: DataFrame, db_file: str, table_name: str) -> None:
    """Connects to the database and loads the data."""
    # Loads the clean_df to SQLite using df.to_sql().
    with sqlite3.connect(db_file) as conn:
        clean_df.to_sql(name=table_name, con=conn, if_exists="replace", index=True)


def main(n: int):
    """Coordinates the ETL pipeline by calling extract -> transform -> load."""
    env_vars = load_env_vars()
    data = extract()
    clean_df = transform(data, n)
    print(clean_df.head())
    # load(clean_df, env_vars["db_path"], "games_sample")


if __name__ == "__main__":

    load_dotenv()
    parser = cronstruct_argparse()
    args = parser.parse_args()
    main(n=args.count)
