"""
"""
from types import NoneType
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
plt.rcParams.update(plt.rcParamsDefault)
sns.set_style("whitegrid")


def generate_plots_by_hues(func: Callable, *hues: list[str], **kwargs) -> defaultdict:
    """
    Generates plots, by accepting plot calls for each hue in hues.
    """
    try:
        x, y = kwargs.get("x"), kwargs.get("y")

        for hue in hues:
            logger.info("Generating plots by color.".format(func.__name__.strip().lower()))
            plot_title = format_title(func.__name__.strip().lower(), x, y, hue)
            plot = func(kwargs, hue)
            plot.savefig(f"../CADA/out/viz/{plot_title}.png")
            plt.close()

    except Exception as e:
        logger.error("Encountered an error while generating plots by hues: {}".format(e))
        raise Exception("Encountered an error while generating plots by hues: {}".format(e))

    logger.info("Successfully generated {} plots by color.".format(func.__name__.strip().lower()))


def generate_relational_plots(df: pd.DataFrame, x: str, y: str, hues: list[str]) -> defaultdict:
    """
    Plot the relationship of each pair of columns using a linear regression fit to the jointplot.
    Optional hues argument allows for visualizing data along specific columns.
    """
    try:
        logger.info("Generating plots of pair-wise relationships".format(x, y))

        # Jointplot: No split on hue -- Overall view
        logger.info("Generating relational plots.")
        plot_title = format_title("jointplot", x, y)
        jointplot = sns.jointplot(data = df, x = x, y = y, kind = "reg")
        jointplot.savefig(f"../CADA/out/viz/{plot_title}.png")
        plt.close()

        # Jointplot: Split on hue -- Comparative view
        # concat each new set of plots using python dictionary update operation
        # plots |= generate_plots_by_hues(sns.jointplot, hues = hues,
        #                                 data = df, x = x, y = y, kind = "reg")

    except Exception as e:
        logger.error("Encountered an error while generating plots of pair-wise relationships: {}".format(e))
        raise Exception("Encountered an error while generating plots of pair-wise relationships: {}".format(e))

    logger.info("Succesfully generated plots of pair-wise relationships.")


def generate_distribution_plots(df: pd.DataFrame, hues: list[str]) -> defaultdict:
    """Plots univariate distributions and saves them in a dictionary."""
    try:
        logger.info("Generating plots for univariate distributions.")
        _, numerical_columns = split_columns_by_type(df)

        for x in numerical_columns:
            logger.info("Generating plots for column: {}".format(x))
            ci = calculate_confidence_intervals_95(df, x)

            # Histogram: No split on hue -- Overall view
            plot_title = format_title("hist", x)
            histplot = sns.displot(data = df, x = x, kind = "hist")
            plt.axvline(np.mean(df[x]), color="red")
            plt.axvline(ci[0], color="gray", linestyle = "--")
            plt.axvline(ci[1], color="gray", linestyle = "--")
            histplot.savefig(f"../CADA/out/viz/{plot_title}.png")
            plt.close()

            # ECDF: No split on hue -- Overall view
            plot_title = format_title("ecdf", x)
            ecdf_plot = sns.displot(data = df, x = x, kind = "ecdf")
            ecdf_plot.savefig(f"../CADA/out/viz/{plot_title}.png")
            plt.close()

            for hue in hues:
                if hue in df.columns:
                    logger.info("Generating plots for column: {}, colored and stacked.".format(x, hue))
                    # Histogram: Colored by hue & Stacked
                    # TODO: Figure out:: Length of list vectors must match length of `data` when both are used,
                                        # but `data` has length 100 and the vector passed to `hue` has length 3.
                    plot_title = format_title("hist.stacked", x)
                    histplot = sns.displot(data = df, x = x, hue = hue, multiple = "stack", kind = "hist")

                    for ax in histplot.axes.flat:
                        ax.axvline(np.mean(df[x]), color="red", label='Avg.', linestyle='-')
                        ax.axvline(ci[0], color="gray", linestyle="--", label='CI Lower')
                        ax.axvline(ci[1], color="gray", linestyle="--", label='CI Upper')
                    histplot.savefig(f"../CADA/out/viz/{plot_title}.png")
                    plt.close()

                    # logger.info("Generating plots for column: {}, split row-wise or column-wise.".format(x))
                    # # Histogram: Subplotted by color
                    # # Subplot by row if there are too many plots to do by column.
                    # plot_title = format_title("hist.subplots", x, hue)
                    # if df.shape[1] > 5:
                    #     plots[plot_title] = sns.displot(data = df, x = x, hue = hue, col = hue, kind = "hist")
                    # else:
                    #     plots[plot_title] = sns.displot(data = df, x = x, hue = hue, row = hue, kind = "hist")

    except Exception as e:
        logger.error("Encountered an error while generating plots for univariate distributions: {}".format(e))
        raise Exception("Encountered an error while generating plots for univariate distributions: {}".format(e))

    logger.info("Successfully generated plots for univariate distributions.")


def generate_categorical_plots(df: pd.DataFrame, hues: list[str]) -> defaultdict:
    """
    Generates countplots for each categorical (non-numerical) column in the specifed DataFrame.
    If a list of categorical columns is provided, in *hues, a countplot is produced for each hue.
    """
    try:
        logger.info("Generating categorical plots.")

        for x in df.columns:
            logger.info("Generating plots for column: {}".format(x))
            # Countplot: No split on hue -- Overall view
            plot_title = format_title("countplot", x)
            countplot = sns.countplot(data = df, x = x)
            countplot.get_figure().savefig(f"../CADA/out/viz/{plot_title}.png")
            plt.close()

            # TODO: Repair plotting by color
            for hue in hues:
                # Countplot: Stacked & colored
                logger.info("Generating plots for column: {}, colored by {} and stacked.".format(x, hue))
                plot_title = format_title("countplot.stacked", x, hue)
                countplot = sns.countplot(data = df, x = x, hue = hue)
                countplot.get_figure().savefig(f"../CADA/out/viz/{plot_title}.png")
                plt.close()

                # # Histogram: Subplotted by color
                # # Subplot by row if there are too many plots to do by column.
                # logger.info("Generating plots for column: {}, row-wise or column-wise.".format(x))
                # plot_title = format_title("countplot.subplots", x, hue)
                # if df.shape[1] > 5:
                #     plots[plot_title] = sns.displot(data = df, x = x, hue = hue, col = hue)
                # else:
                #     plots[plot_title] = sns.displot(data = df, x = x, hue = hue, row = hue)

    except Exception as e:
        logger.error("Encountered an error while generating categorical plots: {}".format(e))
        raise Exception("Encountered an error while generating categorical plots: {}".format(e))

    logger.info("Successfully generated categorical plots.")


# Conductors -- High level functions
def generate_eda_plots(df: pd.DataFrame, hues: list[str]) -> defaultdict:
    """Iteratively plots all numerical columns against one another."""
    try:
        logger.info("Generating exploratory analysis plots.")
        _, numerical_cols = split_columns_by_type(df)

        for pair in pairwise(numerical_cols):
            # Splitting for easier readability
            x, y = pair[0], pair[1]

            # Relational Plots -- for each x-y pair
            generate_relational_plots(df, x, y, hues)

        # Distribution Plots
        generate_distribution_plots(df, hues)

        # Categorical Plots
        generate_categorical_plots(df, hues)

    except Exception as e:
        logger.error("Encountered an error while generating exploratory analysis plots: {}".format(e))
        raise Exception("Encountered an error while generating exploratory analysis plots: {}".format(e))

    logger.info("Successfully generated exploratory analysis plots.")
