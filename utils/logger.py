import logging
from pandas import DataFrame


def log_row_diffs(df1: DataFrame, df2: DataFrame, label: str = "") -> None:

    diff = df1.shape[0] - df2.shape[0]

    if diff == 0:
        logging.warning("No change in rows for activity %s", label)
        return

    logging.debug("Row Difference Count for label %s: %d", label, diff)


def log_if_empty(df: DataFrame) -> None:
    if df.empty:
        logging.warning("Error. Dataframe is empty. Please use a larger sample size.")
