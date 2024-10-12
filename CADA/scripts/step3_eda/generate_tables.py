"""
"""
from typing import Callable
import pandas as pd
from utils import format_title
from collections import defaultdict


# Tables
def generate_relational_tables(*hues, **kwargs) -> defaultdict[str, pd.DataFrame]:
    """
    Generate descriptive statistics tables for variables x and y. 
    Optional argument: hues, allows for descriptive statistics per hue group.
    """
    tables = defaultdict()
    df, x, y = kwargs.get("df"), kwargs.get("x"), kwargs.get("y")
    
    table_name = format_title("rl.table", x, y)
    tables[table_name] = df[x, y].describe()
    
    for hue in hues:
        table_name = format_title("groupby.rl.table", x, y, hue)
        tables[table_name] = df[x, y, hue].groupby(hue).describe()

    return tables


def generate_distribution_tables(df: pd.DataFrame) -> defaultdict[str, pd.DataFrame]:
    tables = defaultdict()

    for x in df.columns:
        table_title = format_title("dist.table", x)
        tables[table_title] = df.describe().T
    return tables


def generate_categorical_tables(df: pd.DataFrame) -> pd.DataFrame:
    tables = defaultdict()

    for col in df.columns:
        table_title = "table.{col}_counts"
        tables[table_title] = df[col].value_counts().to_frame()
    # Possible to add hue-groupby
    return tables


def generate_plots_by_hues(func: Callable, *hues: tuple[str], **kwargs) -> defaultdict:
    plots = defaultdict()
    x, y = kwargs.get("x"), kwargs.get("y")

    for hue in hues:
        plot_title = format_title(func.__name__.strip().lower(), x, y, hue)
        plots[plot_title] = func(kwargs, hue)
    return plots
