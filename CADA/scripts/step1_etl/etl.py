#!/usr/bin/python
import os
import re
import pandas as pd
import numpy as np


########################################################################################
# Overall Data Pipeline // Data Cleaning procedures
def start_pipeline(df):
    # Prevents overwriting data in the pipeline process
    return df.copy()


def clean_column_names(df):
    # Prepares column names for easier analysis
    clean_column_name = (lambda x: x.strip().lower()
                         .replace(" ", "_")
                         .replace("(", "").replace(")", ""))
    return df.rename(clean_column_name, axis = "columns")


def ensure_dataset_types(df):
    """Enforce proper datatype at this stage in data cleaning."""
    # Using either .assign() or .astype({"col": "type"})
    return df


def fill_null_values(df):
    """Use multiple imputation methods to address empty rows of data."""
    return df.assign()


def group_categorical_features(df):
    """Create more specific groupings for each of the categorical features (columns of data)."""
    return df.assign()


def generate_spatial_features(df):
    """Use existing spatial data to generate new spatial data columns."""
    return df.assign()


def calculate_totals(df):
    """Calculate totals based on columns"""
    # Using .assign() or creating new columns through variable declaration.
    return df


def drop_columns(df):
    """Dropping any columns no longer necessary for analysis."""
    return df.drop(
        columns=[
            "",
            "",
            "",
        ]
    )


def sort_data(df):
    """Sorts a dataset with the most recent dates at the top of the table."""
    return df.sort_values(by = ["acquisition_date"],
                          ascending = False,
                          axis = "rows")


########################################################################################
# Data Pipeline
def clean_data(file_path):
    analysis_columns = []
    data = pd.read_csv(file_path, usecols = analysis_columns)

    cleaned_data = (
        data.pipe(start_pipeline)
        .pipe(clean_column_names)
        .pipe(ensure_dataset_types)
        .pipe(fill_null_values)
        .pipe(sort_data)
        .pipe(group_categorical_features)
        .pipe(generate_spatial_features)
        .pipe(calculate_totals)
        # missing value (imputation) strategy -- unmodified
        .pipe(drop_columns)
    )

    return (cleaned_data)


if __name__ == "__main__":
    file_path = "./data/MoMA NYC artworks.csv"
    datasets = clean_data(file_path)
