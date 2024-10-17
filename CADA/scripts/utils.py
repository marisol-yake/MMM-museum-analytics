#!/usr/bin/python
# A set of utility functions that are shared across analyses
import numpy as np
import pandas as pd
from .config import setup_logging


logger = setup_logging("utils")


def load_dataset(data_path: str, **kwargs) -> pd.DataFrame:
    """
    Load a dataset into a pandas DataFrame using one of the many available functions.

    Parameters
    ----------
        data_path: str

    Returns
    -------
        dataset: pd.DataFrame
    """

    try:
        logger.info("Loading the dataset into a DataFrame.")
        file_type = data_path.rsplit(".", 1)[1].strip().lower()
        match file_type:
            case "csv" | "tsv": dataset = pd.read_csv(data_path, **kwargs)
            case "excel" | "xlsx": dataset = pd.read_excel(data_path, **kwargs)
            case "json": dataset = pd.read_json(data_path, **kwargs)

    except Exception as e:
        logger.error("Encountered an error while loading the dataset: {}".format(e))
        raise Exception("Encountered an error while loading the dataset: {}".format(e))

    logger.info("Successfully loaded the dataset into a DataFrame.")
    return dataset


def identical_dfs(x: pd.DataFrame, y: pd.DataFrame) -> bool:
    return x.equals(y)


def format_title(func: str, *args) -> str:
    """Formats plot titles."""
    try:
        logger.info("Formatting titles for organization and export.")
        if len(args) > 1:
            title = func.strip().lower() + "." + "-".join(str(arg) for arg in args)
        else:
            title = func.strip().lower() + "." + str(args[0])
        title = "_".join("{}".format(title).rsplit("-", 1))

    except Exception as e:
        logger.error("Encountered an error while formatting titles: {}".format(e))
        raise Exception("Encountered an error while formatting titles: {}".format(e))

    logger.info("Successfully formatted title: {}".format(title))
    return title


def split_columns_by_type(df: pd.DataFrame) -> list[str]:
    """Columns are split into Categorical and Numerical groupings."""
    try:
        logger.info("Splitting dataset into subsets based on datatype.")
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        num_cols = df.select_dtypes(exclude=["object", "category"]).columns

    except Exception as e:
        logger.error("Error occurred when trying to split pd.DataFrame columns by data type.")
        raise Exception("Error occurred when trying to split pd.DataFrame columns by data type: {}".format(e))

    logger.info("Successfully split pd.DataFrame columns by data type.")
    return cat_cols, num_cols


def calculate_confidence_intervals_95(df: pd.DataFrame, column: str) -> tuple[float, float]:
    # Calculate mean and 95% CI
    mean = df[column].mean()
    std_err = df[column].std() / np.sqrt(df.shape[0])  # Standard error calculation
    lower_bound, upper_bound = (mean - 1.96 * std_err, mean + 1.96 * std_err)  # CI calculation
    return lower_bound, upper_bound
