#!/usr/bin/python
# A streamlined script of our comprehensive exploratory data visualization process
import pandas as pd
import os
from utils import format_title, load_dataset
from generate_tables import generate_eda_tables
from generate_plots import generate_eda_plots
from config import setup_logging


logger = setup_logging("eda")


def main(data_path: os.path.Path, export: bool = False) -> None:
    """
    Plots all planned exploratory visualizations and complementary tables.
    """
    try:
        logger.info("Beginning exploratory data analysis.")
        # Load in data
        dataset = load_dataset(data_path)

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
            logger.info("Saving all plots and tables.")
            # Save Plots

            # Save Tables

    except Exception as e:
        logger.error("Encountered an error during exploratory data analysis: {}".format(e))
        raise Exception("Encountered an error during data analysis: {}".format(e))

    logger.info("Successfully performed exploratory analysis.")


if __name__ == "__main__":
    data_path = ...
    main(data_path, export = False)
