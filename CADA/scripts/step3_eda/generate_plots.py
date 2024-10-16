"""
"""
from typing import Callable
from collections import defaultdict

from matplotlib import pyplot as plt
import numpy as np
from utils import format_title, split_columns_by_type
from itertools import permutations
import pandas as pd
import seaborn as sns
from config import setup_logging


logger = setup_logging("generate_plots")


def generate_plots_by_hues(func: Callable, *hues: tuple[str], **kwargs) -> defaultdict:
    """
    Generates plots, by accepting plot calls for each hue in hues. 
    """
    try:
        logger.info("Generating plots for each hue in hues.")
        plots = defaultdict()
        x, y = kwargs.get("x"), kwargs.get("y")

        for hue in hues:
            plot_title = format_title(func.__name__.strip().lower(), x, y, hue)
            plots[plot_title] = func(kwargs, hue)

    except Exception as e:
        logger.error("Encountered an error while generating plots for each hue in hues: {}".format(e))
        raise Exception("Encountered an error while generating plots for each hue in hues: {}".format(e))

    logger.info("Successfully generates plots by hue.")
    return plots


def generate_relational_plots(df: pd.DataFrame, x: str, y: str, hues: list[str]) -> defaultdict[str, sns.object.Plot]:
    """
    Plot the relationship of each pair of columns using a linear regression fit to the jointplot.
    Optional hues argument allows for visualizing data along specific columns.
    """
    try:
        logger.info("Generating plots of pair-wise relationships.")
        plots = defaultdict()

        # Jointplot: No split on hue -- Overall view
        plot_name = format_title("jointplot.", x, y)
        plots[plot_name] = sns.jointplot(data = df, x = x, y = y, kind = "reg")

        # Jointplot: Split on hue -- Comparative view
        # concat each new set of plots using python dictionary update operation
        plots |= generate_plots_by_hues(sns.jointplot, hues = hues, data = df, x = x, y = y, kind = "reg")

    except Exception as e:
        logger.error("Encountered an error while generating plots of pair-wise relationships: {}".format(e))
        raise Exception("Encountered an error while generating plots of pair-wise relationships: {}".format(e))

    logger.info("Succesfully generated plots of pair-wise relationships.")
    return plots


def generate_distribution_plots(df: pd.DataFrame, *hues: tuple[str]) -> defaultdict[str, sns.objects.Plot]:
    """Plots univariate distributions and saves them in a dictionary."""
    try:
        logger.info("Generating plots for univariate distributions.")
        plots = defaultdict()

        for x in df.columns:
            logger.info("Generating plots for column: {}".format(x))
            # Histogram: No split on hue -- Overall view
            plot_name = format_title("hist.", x)
            histplot = sns.displot(data = df, x = x, kind = "hist")
            plt.axvline(histplot, np.mean(df[x]), color="red")
            plt.axvline(histplot, np.mean(df[x]), color="red")
            plt.axvline(histplot, np.mean(df[x]), color="red")
            plots[plot_name] = histplot

            # ECDF: No split on hue -- Overall view
            plot_name = + format_title("ecdf.", x)
            plots[plot_name] = sns.displot(data = df, x = x, kind = "ecdf")

            for hue in hues:
                logger.info("Generating plots for column: {}, colored by hue and stacked.".format(x))
                # Histogram: Colored by hue & Stacked
                plot_name = format_title("hist.stacked", x, y)
                plots[plot_name] = sns.displot(data = df, x = x, hue = hue, multiple = "stack", kind = "hist")

                logger.info("Generating plots for column: {}, row-wise or column-wise.".format(x))
                # Histogram: Subplotted by color
                # Subplot by row if there are too many plots to do by column.
                plot_name = format_title("hist.subplots", x, hue)
                if df.shape[1] > 5:
                    plots[plot_name] = sns.displot(data = df, x = x, hue = hue, col = hue, kind = "hist")
                else:
                    plots[plot_name] = sns.displot(data = df, x = x, hue = hue, row = hue, kind = "hist")

    except Exception as e:
        logger.error("Encountered an error while generating plots for univariate distributions: {}".format(e))
        raise Exception("Encountered an error while generating plots for univariate distributions: {}".format(e))

    logger.info("Successfully generated plots for univariate distributions.")
    return plots


def generate_categorical_plots(df: pd.DataFrame, *hues: tuple[str]) -> defaultdict[str, sns.objects.Plot]:
    """
    Generates countplots for each categorical (non-numerical) column in the specifed DataFrame.
    If a list of categorical columns is provided, in *hues, a countplot is produced for each hue.
    """
    try:
        logger.info("Generating categorical plots.")
        plots = defaultdict()

        for x in df.columns:
            logger.info("Generating plots for column: {}".format(x))
            # Countplot: No split on hue -- Overall view
            plot_name = format_title("countplot.", x)
            plots[plot_name] = sns.countplot(data = df, x = x)

            for hue in hues:
                # Countplot: Stacked & colored
                logger.info("Generating plots for column: {}, colored by hue and stacked.".format(x))
                plot_name = format_title("countplot.stacked", x, hue)
                plots[plot_name] = sns.countplot(data = df, x = x, hue = hue, multiple = "stack", kind = "hist")

                # Histogram: Subplotted by color
                # Subplot by row if there are too many plots to do by column.
                logger.info("Generating plots for column: {}, row-wise or column-wise.".format(x))
                plot_name = format_title("countplot.subplots", x, hue)
                if df.shape[1] > 5:
                    plots[plot_name] = sns.displot(data = df, x = x, hue = hue, col = hue, kind = "hist")
                else:
                    plots[plot_name] = sns.displot(data = df, x = x, hue = hue, row = hue, kind = "hist")

    except Exception as e:
        logger.error("Encountered an error while generating categorical plots: {}".format(e))
        raise Exception("Encountered an error while generating categorical plots: {}".format(e))

    logger.info("Successfully generated categorical plots.")
    return plots


# Conductors -- High level functions
def generate_eda_plots(df: pd.DataFrame, hues: list[str]) -> defaultdict[str, sns.objects.Plot]:
    """Iteratively plots all numerical columns against one another."""
    try:
        logger.info("Generating exploratory analysis plots.")
        plots = defaultdict()
        categorical_cols, numerical_cols = split_columns_by_type(df)
        cat_subset = df[categorical_cols].copy()

        # NOTE: Currently produces 1-redundant permutation
        # Works for now for having both angles for data story telling.
        permutations = [list(perm) for perm in permutations(numerical_cols)]
        for permutation in permutations:
            # Splitting for easier readability
            x, y = permutation[0], permutation[1]

            # Relational Plots -- for each x-y permutation
            rel_plots = generate_relational_plots(df, x, y, hues)

        # Distribution Plots
        dist_plots = generate_distribution_plots(df, hues)

        # Categorical Plots
        cat_plots = generate_categorical_plots(cat_subset, hues)

        # Update plots dictionary with all (unrendered) results.
        plots = plots | rel_plots | dist_plots | cat_plots

    except Exception as e:
        logger.error("Encountered an error while generating exploratory analysis plots: {}".format(e))
        raise Exception("Encountered an error while generating exploratory analysis plots: {}".format(e))

    logger.info("Successfully generated exploratory analysis plots.")
    return plots
