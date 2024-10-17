"""
"""
from typing import Callable
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from scripts.utils import calculate_confidence_intervals_95, format_title, split_columns_by_type
from scripts.config import setup_logging
from itertools import pairwise
import pandas as pd
import seaborn as sns


logger = setup_logging("generate_plots")


def generate_plots_by_hues(func: Callable, *hues: tuple[str], **kwargs) -> defaultdict:
    """
    Generates plots, by accepting plot calls for each hue in hues.
    """
    try:
        plots = defaultdict()
        x, y = kwargs.get("x"), kwargs.get("y")

        for hue in hues:
            logger.info("Generating plots by color.".format(func.__name__.strip().lower()))
            plot_title = format_title(func.__name__.strip().lower(), x, y, hue)
            plots[plot_title] = func(kwargs, hue)

    except Exception as e:
        logger.error("Encountered an error while generating plots by hues: {}".format(e))
        raise Exception("Encountered an error while generating plots by hues: {}".format(e))

    logger.info("Successfully generated {} plots by color.".format(func.__name__.strip().lower()))
    return plots


def generate_relational_plots(df: pd.DataFrame, x: str, y: str, hues: list[str]) -> defaultdict:
    """
    Plot the relationship of each pair of columns using a linear regression fit to the jointplot.
    Optional hues argument allows for visualizing data along specific columns.
    """
    try:
        logger.info("Generating plots of pair-wise relationships".format(x, y))
        plots = defaultdict()

        # Jointplot: No split on hue -- Overall view
        logger.info("Generating relational plots.")
        plot_name = format_title("jointplot", x, y)
        plots[plot_name] = sns.jointplot(data = df, x = x, y = y, kind = "reg")

        # Jointplot: Split on hue -- Comparative view
        # concat each new set of plots using python dictionary update operation
        plots |= generate_plots_by_hues(sns.jointplot, hues = hues, data = df, x = x, y = y, kind = "reg")

    except Exception as e:
        logger.error("Encountered an error while generating plots of pair-wise relationships: {}".format(e))
        raise Exception("Encountered an error while generating plots of pair-wise relationships: {}".format(e))

    logger.info("Succesfully generated plots of pair-wise relationships.")
    return plots


def generate_distribution_plots(df: pd.DataFrame, *hues: tuple[str]) -> defaultdict:
    """Plots univariate distributions and saves them in a dictionary."""
    try:
        logger.info("Generating plots for univariate distributions.")
        _, numerical_columns = split_columns_by_type(df)
        plots = defaultdict()

        for x in df.columns:
            if "date" not in x and x in numerical_columns:
                logger.info("Generating plots for column: {}".format(x))
                ci = calculate_confidence_intervals_95(df, x)

                # Histogram: No split on hue -- Overall view
                plot_name = format_title("hist", x)
                histplot = sns.displot(data = df, x = x, kind = "hist")
                plt.axvline(np.mean(df[x]), color="red")
                plt.axvline(ci[0], color="gray", linestyle = "--")
                plt.axvline(ci[1], color="gray", linestyle = "--")
                plots[plot_name] = histplot

                # ECDF: No split on hue -- Overall view
                plot_name = format_title("ecdf", x)
                plots[plot_name] = sns.displot(data = df, x = x, kind = "ecdf")

                # TODO: Load in categorical column types as 'categorical' datatype.
                # for hue in hues:
                #     logger.info("Generating plots for column: {}, colored and stacked.".format(x, hue))
                #     # Histogram: Colored by hue & Stacked
                #     # TODO: Figure out:: Length of list vectors must match length of `data` when both are used,
                #                         # but `data` has length 100 and the vector passed to `hue` has length 3.
                #     # plot_name = format_title("hist.stacked", x)
                #     # plots[plot_name] = sns.displot(data = df, x = x, hue = hue, multiple = "stack", kind = "hist")

                #     logger.info("Generating plots for column: {}, split row-wise or column-wise.".format(x))
                #     # Histogram: Subplotted by color
                #     # Subplot by row if there are too many plots to do by column.
                #     plot_name = format_title("hist.subplots", x, hue)
                #     if df.shape[1] > 5:
                #         plots[plot_name] = sns.displot(data = df, x = x, hue = hue, col = hue, kind = "hist")
                #     else:
                #         plots[plot_name] = sns.displot(data = df, x = x, hue = hue, row = hue, kind = "hist")

    except Exception as e:
        logger.error("Encountered an error while generating plots for univariate distributions: {}".format(e))
        raise Exception("Encountered an error while generating plots for univariate distributions: {}".format(e))

    logger.info("Successfully generated plots for univariate distributions.")
    return plots


def generate_categorical_plots(df: pd.DataFrame, *hues: tuple[str]) -> defaultdict:
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
            plot_name = format_title("countplot", x)
            plots[plot_name] = sns.countplot(data = df, x = x)

            # TODO: Repair plotting by color
            # for hue in hues:
            #     # Countplot: Stacked & colored
            #     logger.info("Generating plots for column: {}, colored by {} and stacked.".format(x, hue))
            #     plot_name = format_title("countplot.stacked", x, hue)
            #     plots[plot_name] = sns.countplot(data = df, x = x, hue = hue, multiple = "stack", kind = "hist")

            #     # Histogram: Subplotted by color
            #     # Subplot by row if there are too many plots to do by column.
            #     logger.info("Generating plots for column: {}, row-wise or column-wise.".format(x))
            #     plot_name = format_title("countplot.subplots", x, hue)
            #     if df.shape[1] > 5:
            #         plots[plot_name] = sns.displot(data = df, x = x, hue = hue, col = hue, kind = "hist")
            #     else:
            #         plots[plot_name] = sns.displot(data = df, x = x, hue = hue, row = hue, kind = "hist")

    except Exception as e:
        logger.error("Encountered an error while generating categorical plots: {}".format(e))
        raise Exception("Encountered an error while generating categorical plots: {}".format(e))

    logger.info("Successfully generated categorical plots.")
    return plots


# Conductors -- High level functions
def generate_eda_plots(df: pd.DataFrame, hues: list[str]) -> defaultdict:
    """Iteratively plots all numerical columns against one another."""
    try:
        logger.info("Generating exploratory analysis plots.")
        plots = defaultdict()
        categorical_cols, numerical_cols = split_columns_by_type(df)
        cat_subset = df[categorical_cols].copy()
        plots = defaultdict()

        for pair in pairwise(numerical_cols):
            # Splitting for easier readability
            x, y = pair[0], pair[1]

            # Relational Plots -- for each x-y pair
            plots |= generate_relational_plots(df, x, y, hues)

        # Distribution Plots
        plots |= generate_distribution_plots(df, hues)

        # Categorical Plots
        plots |= generate_categorical_plots(cat_subset, hues)

    except Exception as e:
        logger.error("Encountered an error while generating exploratory analysis plots: {}".format(e))
        raise Exception("Encountered an error while generating exploratory analysis plots: {}".format(e))

    logger.info("Successfully generated exploratory analysis plots.")
    return plots


def get_save_method(plot):
    """
    Get the appropriate save method for the given plot object.

    Parameters:
    plot_object: Axes, Figure, or JointGrid object

    Returns:
    A callable function for saving the plot.
    """
    try:
        if isinstance(plot, plt.Figure):
            return plot.savefig
        elif isinstance(plot, sns.JointGrid):
            return plot.figure.savefig
        elif isinstance(plot, plt.Axes):
            return plot.get_figure().savefig
    except Exception as e:
            raise TypeError("Unsupported plot object type {}".format(e))


def save_plot(fig, plot_title: str, png: bool = True, pdf: bool = False):
    """Save plots to PDF or PNG image file formats."""
    logger.info("Saving an exploratory analysis plot.")
    try:
        save_method = get_save_method(fig)

        if png:
            save_method(f"./out/viz/{plot_title}.png")
        if pdf:
            save_method(f"./out/viz/{plot_title}.pdf")

    except Exception as e:
        logger.error("Encountered an error while saving plots: {}".format(e))
        raise Exception("Encountered an error while saving plots: {}".format(e))

    logger.info("Successfully saved an exploratory analysis plot.")
