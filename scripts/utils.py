#!/usr/bin/python
# A set of utility functions that are shared across analyses
import pandas as pd

def load_dataset(data_path):
    file_type = data_path.rsplit(".", 1)[1].strip().lower()
    match file_type:
        case "csv" | "tsv": dataset = pd.read_csv(data_path)
        case "excel" | "xlsx": dataset = pd.read_excel(data_path)
        case "json": dataset = pd.read_json(data_path)
    return dataset

def format_title(func: str, *args: str) -> str:
    """
    I don't know how I want to format yet.

    Example:
        args:
        input:
        output:
    """
    return "_".join("{}.".format(func.strip().lower()) + "-".join(args)).rsplit("-", 1)

def split_columns_by_type(df: pd.DataFrame) -> list[str]:
    """Columns are split into Categorical and Numerical groupings."""
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    num_cols = df.select_dtypes(exclude=["object", "category"]).columns
    return cat_cols, num_cols