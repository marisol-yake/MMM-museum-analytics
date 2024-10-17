#!/usr/bin/python
# A streamlined script of our comprehensive exploratory data visualization process
import os
from pathlib import Path
import pandas as pd
import sys
from ..utils import format_title, load_dataset
from ..config import setup_logging
from .generate_tables import generate_eda_tables, save_table
from .generate_plots import generate_eda_plots, save_plot


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

        # specified categorical columns of interest
        # e.g. department, storage_group, etc.
        # these can include custom columns generated during data preprocessing.
        hue_categories = ["credit", "department", "storage_group"]

        print("Preparing exploratory plots.")
        # Generate Plots
        plots = generate_eda_plots(dataset, hues = hue_categories)

        print("Preparing exploratory tables.")
        # Generate Tables
        tables = generate_eda_tables(dataset, hues = hue_categories)

        if export:
            logger.info("Saving plots and tables.")
            # Save Plots
            for title, plot in plots.items():
                save_plot(plot, title)

            # Save Tables
            for title, table in tables.items():
                save_table(table, title, table_type = "excel")

    except Exception as e:
        logger.error("Encountered an error during exploratory data analysis: {}".format(e))
        raise Exception("Encountered an error during data analysis: {}".format(e))

    logger.info("Successfully performed exploratory analysis.")


if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), "NYC-MoMA-storage_group-fill.csv")
    main(data_path, export = True)
