"""
"""
import pandas as pd
from utils import format_title, split_columns_by_type
from collections import defaultdict
from itertools import permutations
from config import setup_logging


logger = setup_logging("generate_tables")


# Tables
def generate_relational_tables(*hues, **kwargs) -> defaultdict[str, pd.DataFrame]:
    """
    Generate descriptive statistics tables for variables x and y.
    Optional argument: hues, allows for descriptive statistics per hue group.
    """
    try:
        logger.info("Generating relational tables.")
        tables = defaultdict()
        df, x, y = kwargs.get("df"), kwargs.get("x"), kwargs.get("y")

        table_name = format_title("rl.table", x, y)
        tables[table_name] = df[x, y].describe()

        for hue in hues:
            table_name = format_title("groupby.rl.table", x, y, hue)
            tables[table_name] = df[x, y, hue].groupby(hue).describe()
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
        tables = defaultdict()

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
        tables = defaultdict()

        for col in df.columns:
            table_title = "table.{col}_counts"
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
        tables = defaultdict()
        categorical_cols, numerical_cols = split_columns_by_type(df)
        cat_subset = df[categorical_cols].copy()

        # NOTE: Currently produces 1-redundant permutation
        # Works for now for having both angles for data story telling.
        permutations = [list(perm) for perm in permutations(numerical_cols)]
        for permutation in permutations:
            # Splitting for easier readability
            x, y = permutation[0], permutation[1]

            # Relational Tables -- for each x-y permutation
            rel_tables = generate_relational_tables(df, x, y, hues)

        # Distribution Tables
        dist_tables = generate_distribution_tables(df, hues)

        # Categorical Tables
        cat_tables = generate_categorical_tables(cat_subset)

        # Update tables dictionary with all (unrendered) results.
        tables = tables | rel_tables | dist_tables | cat_tables

    except Exception as e:
        logger.error("Encountered an error while generating exploratory analysis tables: {}".format(e))
        raise Exception("Encountered an error while generating exploratory analysis tables: {}".format(e))

    logger.info("Successfully generated exploratory analysis tables.")
    return tables
