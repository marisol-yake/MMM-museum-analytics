"""
"""
import os
from pathlib import Path
import pandas as pd
from scripts.utils import format_title, split_columns_by_type
from scripts.config import setup_logging
from collections import defaultdict
from itertools import pairwise, permutations



logger = setup_logging("generate_tables")


# Tables
def generate_relational_tables(dataset: pd.DataFrame, x: str, y: str, *hues) -> defaultdict[str, pd.DataFrame]:
    """
    Generate descriptive statistics tables for variables x and y.
    Optional argument: hues, allows for descriptive statistics per hue group.
    """
    try:
        logger.info("Generating relational tables.")
        tables = defaultdict(str)

        table_name = format_title("rl.table", x, y)
        tables[table_name] = dataset[[x, y]].describe()

        # TODO: Repair plotting by hue
        # for hue in hues:
        #     table_name = format_title("groupby.rl.table", x, y, hue)
        #     tables[table_name] = dataset[x, y, hue].groupby(hue).describe()

    except Exception as e:
        logger.error("Encountered an error while generating relational tables: {}".format(e))
        raise Exception("Encountered an error while generating relational tables: {}".format(e))

    logger.info("Successfully generated relational tables.")
    return tables


def generate_distribution_tables(df: pd.DataFrame) -> defaultdict[str, pd.DataFrame]:
    """
    Generates tables concisely describing distributions of data.
    """
    try:
        logger.info("Generating distribution tables.")
        tables = defaultdict(str)

        for x in df.columns:
            table_title = format_title("dist.table", x)
            tables[table_title] = df.describe().T

    except Exception as e:
        logger.error("Encountered an error while generating distribution tables: {}".format(e))
        raise Exception("Encountered an error while generating distribution tables: {}".format(e))

    logger.info("Successfully generated distribution tables.")
    return tables


def generate_categorical_tables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates tables for each column in the categorical subset of the dataframe.
    """
    try:
        logger.info("Generating categorical tables.")
        tables = defaultdict(str)

        for col in df.columns:
            logger.info("Generating counts")
            table_title = f"table.{col}_counts"
            tables[table_title] = df[col].value_counts().to_frame()
        # Possible to add hue-groupby

    except Exception as e:
        logger.error("Encountered an error while generating categorical tables: {}".format(e))

    logger.info("Successfully generated categorical tables.")
    return tables


def generate_eda_tables(df: pd.DataFrame, hues: list[str]) -> defaultdict[str, pd.DataFrame]:
    """Iteratively plots all numerical columns against one another."""
    try:
        logger.info("Generating exploratory analysis tables.")
        tables = defaultdict(str)
        categorical_cols, numerical_cols = split_columns_by_type(df)
        cat_subset = df[categorical_cols].copy()

        for pair in pairwise(numerical_cols):
            # Splitting for easier readability
            x, y = pair[0], pair[1]

            # Relational Tables -- for each x-y permutation
            tables |= generate_relational_tables(df, x, y, hues)

        # Distribution Tables
        tables |= generate_distribution_tables(df)

        # Categorical Tables
        tables |= generate_categorical_tables(cat_subset)

    except Exception as e:
        logger.error("Encountered an error while generating exploratory analysis tables: {}".format(e))
        raise Exception("Encountered an error while generating exploratory analysis tables: {}".format(e))

    logger.info("Successfully generated exploratory analysis tables.")
    return tables


def save_table(table: pd.DataFrame, table_title: str, table_type: str = "excel") -> None:
    logger.info("Saving an exploratory analysis tables.")
    try:
        match table_type:
            case "excel" | "xlsx":
                path = f"./out/tables/{table_title}.xlsx"
                table.to_excel(path)
            case "csv":
                path = f"./out/tables/{table_title}.csv"
                table.to_csv(path)
            case _:
                path = f"./out/tables/{table_title}.xlsx"
                table.to_excel(path)

    except Exception as e:
        logger.error("Encountered an error while saving all tables: {}".format(e))
        raise Exception("Encountered an error while saving all tables: {}".format(e))

    logger.info("Succesfully saved an exploratory analysis table.")
