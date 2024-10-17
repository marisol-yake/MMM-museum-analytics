#!/usr/bin/python
# A streamlined script of our comprehensive exploratory data visualization process
import os
from pathlib import Path
import numpy as np
import pandas as pd
import sys
from ..utils import format_title, load_dataset, remove_outliers, split_columns_by_type
from ..config import setup_logging
from ..ts_statistics import generate_ts_features
from .generate_tables import generate_eda_tables, save_table
from .generate_plots import generate_eda_plots

logger = setup_logging("eda")


def main(data_path: Path, export: bool = False) -> None:
    """
    Plots all planned exploratory visualizations and complementary tables.
    """
    try:
        logger.info("Beginning exploratory data analysis.")
        # Load in data
        analysis_columns = [
            "acquisition_date", "date", "object_number", "department",
            "width_ft", "height_ft", "depth_ft", "cubic_ft",
            "storage_group", "credit_group", "spatial_running_total",
            "adate_sum", "acc_gaps"
        ]
        dataset = load_dataset(data_path, usecols = analysis_columns).sample(100)
        categorical_cols, numerical_cols = split_columns_by_type(dataset)

        # specified categorical columns of interest
        # e.g. department, storage_group, etc.
        # these can include custom columns generated during data preprocessing.
        hue_categories = ["credit_group", "department", "storage_group"]

        dataset.loc[:, numerical_cols] = remove_outliers(dataset[numerical_cols])

        print("Preparing exploratory plots.")
        # Generate Plots - Plots are exported by default
        generate_eda_plots(dataset, hues = hue_categories)

        print("Preparing exploratory tables.")
        # Generate Tables
        tables = generate_eda_tables(dataset, hues = hue_categories)
        for title, table in tables.items():
            save_table(table, title, table_type = "excel")

    except Exception as e:
        logger.error("Encountered an error during exploratory data analysis: {}".format(e))
        raise Exception("Encountered an error during data analysis: {}".format(e))

    logger.info("Successfully performed exploratory analysis.")


if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), "NYC-MoMA-storage_group-fill.csv")
    main(data_path, export = True)