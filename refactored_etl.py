import logging
import sqlite3
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


def cronstruct_argparse():
    parser = argparse.ArgumentParser(description="Steam Random Game Sampler")

    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=10,
        help="Count of steam games to sample from dataset. Defaults to 10.",
    )
    parser.add_argument(
        "-t",
        "--table",
        type=str,
        default="api_data",
        help="Database Table to place output. defaults to 'api_data'",
    )

    parser.add_argument(
        "-s",
        "--source",
        required=True,
        type=str,
        help="Kaggle Dataset Source. Required.",
    )

    parser.add_argument(
        "-p",
        "--db-path",
        type=str,
        default="data.db",
        help="Output path for sqlite database. Defaults to 'data.db'",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display debug Information. Defaults to False",
    )

    return parser


def extract(source: str) -> DataFrame:
    logging.debug("Fetching File from remote. This may take a moment...")
    # Download latest version
    path = kagglehub.dataset_download(source)
    logging.debug("Reading csv file in to dataframe for transformations....")
    df = pd.read_csv(path + "/games.csv", index_col=None, header=0, names=COLS)
    return df


def transform(df: DataFrame, sample_size=10) -> DataFrame:
    logging.debug("Running Transforms.")
    # take a random amount of sample size n
    logging.debug("Taking sample of size %d", sample_size)
    df = df.sample(n=sample_size)
    # sort values by app id, since they are now all over the place after the random sample
    logging.debug("Sorting by App ID")
    df = df.sort_values("AppID")
    # then reset the index, so now the indicies are more ordered
    df = df.reset_index(drop=False)

    logging.debug("Normalizing column names")
    # Normalize col names
    df.columns = [camel_to_sql_valid_snake(col) for col in df.columns]

    logging.debug("Coming bad row with its original row")
    # combine the two that were causing csv issues:
    df["achievements"] = (
        df["achievements"].astype(str) + "," + df["bad_row"].astype(str)
    )

    logging.debug("Filtering bad rows")
    # Clear out unnecessary rows that we do not need
    df = df.drop(
        [
            "movies",
            "screenshots",
            "bad_row",
            "user_score",
            "supported_languages",
            "full_audio_languages",
            "header_image",
            "website",
            "support_url",
            "support_email",
            "score_rank",
            "notes",
        ],
        axis=1,
    )

    logging.debug("Dropping NSFW games")
    # filter NSFW games
    df_nonsfw = df[(df["tags"].str.contains("Nudity") == False)]

    logging.debug("Filtering games with no reviews")
    # drop games with no bad reviews and no good reviews
    df_noreview = df_nonsfw[
        ((df_nonsfw["positive"] != 0) | (df_nonsfw["negative"] != 0))
    ]

    # drop games with no metacritic score
    df_cleaned = df_noreview[(df_noreview["metacritic_score"] != 0)]

    if df.empty:
        logging.debug("DataFrame was Empty. Please run with a higher '-n' value.")

    logging.debug("Complete.")
    return df_cleaned


def load(clean_df: DataFrame, db_file: str, table_name: str) -> None:
    logging.debug("Loading file to database %s on table %s", db_file, table_name)
    """Connects to the database and loads the data."""
    # Loads the clean_df to SQLite using df.to_sql().
    with sqlite3.connect(db_file) as conn:
        clean_df.to_sql(name=table_name, con=conn, if_exists="replace", index=True)


def main():
    """Coordinates the ETL pipeline by calling extract -> transform -> load."""

    # make argparse and get args
    parser = cronstruct_argparse()
    args = parser.parse_args()

    # set logging

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logging.debug("Configuration: ")
    logging.debug("Count: %d", args.count)
    logging.debug("Source: %s", args.source)
    logging.debug("Database Path: %s", args.db_path)
    logging.debug("Database Table: %s", args.table)

    # ETL
    data = extract(source=args.source)
    clean_df = transform(data, args.count)
    # This doesnt cleanly print to logging. so I have to use .print()
    if args.verbose and not clean_df.empty:
        logging.debug("Preview:\n")
        print(clean_df.head())

    load(clean_df, args.db_path, args.table)  # type: ignore
    print("Pipeline Finished.")


if __name__ == "__main__":

    main()
