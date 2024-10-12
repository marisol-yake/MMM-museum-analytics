#!/usr/bin/python
# A streamlined script of our comprehensive exploratory data visualization process
from typing import Callable
import pandas as pd
import seaborn as sns
from itertools import permutations
from collections import defaultdict
from utils import format_title, split_columns_by_type, load_dataset


#
# Plots
def generate_relational_plots(df: pd.DataFrame, x: str, y: str, hues: list[str]) -> defaultdict[str, sns.object.Plot]:
    """
    Plot the relationship of each pair of columns using a linear regression fit to the jointplot.
    Optional hues argument allows for visualizing data along specific columns.
    """
    plots = defaultdict()

    # Jointplot: No split on hue -- Overall view
    plot_name = format_title("jointplot.", x, y)
    plots[plot_name] = sns.jointplot(data = df, x = x, y = y, kind = "reg")
    
    # Jointplot: Split on hue -- Comparative view
    # concat each new set of plots using python dictionary update operation
    plots |= generate_plots_by_hues(sns.jointplot, hues = hues, data = df, x = x, y = y, kind = "reg")
    return plots

def generate_distribution_plots(df: pd.DataFrame, *hues: tuple[str]) -> defaultdict[str, sns.objects.Plot]:
    """Plots univariate distributions and saves them in a dictionary."""
    plots = defaultdict()

    for x in df.columns:
        # Histogram: No split on hue -- Overall view
        plot_name = format_title("hist.", x)
        plots[plot_name] = sns.displot(data = df, x = x, kind = "hist")

        # ECDF: No split on hue -- Overall view
        plot_name = + format_title("ecdf.", x)
        plots[plot_name] = sns.displot(data = df, x = x, kind = "ecdf")

        for hue in hues:
            # Histogram: Stacked & colored
            plot_name = format_title("hist.stacked", x, y)
            plots[plot_name] = sns.displot(data = df, x = x, hue = hue, multiple = "stack", kind = "hist")
            
            # Histogram: Subplotted by color
            # Subplot by row if there are too many plots to do by column.
            plot_name = format_title("hist.subplots", x, hue)
            if df.shape[1] > 5:
                plots[plot_name] = sns.displot(data = df, x = x, hue = hue, col = hue, kind = "hist")
            else:
                plots[plot_name] = sns.displot(data = df, x = x, hue = hue, row = hue, kind = "hist")
    return plots

def generate_categorical_plots(df: pd.DataFrame, *hues: tuple[str]) -> defaultdict[str, sns.objects.Plot]:
    plots = defaultdict()
    
    for x in df.columns:
        # Countplot: No split on hue -- Overall view
        plot_name = format_title("countplot.", x)
        plots[plot_name] = sns.countplot(data = df, x = x)

        for hue in hues:
            # Countplot: Stacked & colored
            plot_name = format_title("countplot.stacked", x, hue)
            plots[plot_name] = sns.countplot(data = df, x = x, hue = hue, multiple = "stack", kind = "hist")

            # Histogram: Subplotted by color
            # Subplot by row if there are too many plots to do by column.
            plot_name = format_title("countplot.subplots", x, hue)
            if df.shape[1] > 5:
                plots[plot_name] = sns.displot(data = df, x = x, hue = hue, col = hue, kind = "hist")
            else:
                plots[plot_name] = sns.displot(data = df, x = x, hue = hue, row = hue, kind = "hist")
    return plots

# Conductors -- High level functions
def generate_eda_plots(df: pd.DataFrame, hues: list[str]) -> defaultdict[str, sns.objects.Plot]:
    """Iteratively plots all numerical columns against one another."""
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
    return plots

def generate_eda_tables(df: pd.DataFrame, hues: list[str]) -> defaultdict[str, pd.DataFrame]:
    """Iteratively plots all numerical columns against one another."""
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
    return tables

def main(data_path , export: bool) -> None:
    """Plots all planned exploratory visualizations and complementary tables."""
    
    print("Beginning exploratory data analysis...")
    # Load in data
    dataset = load_dataset(data_path)

    # specified categorical columns of interest
    # e.g. department, storage_group, etc.
    # these can include custom columns generated during data preprocessing.
    hue_categories = ["credit", "department", "storage_group"]

    print("Preparing EDA plots...")
    # Generate Plots
    plots = generate_eda_plots(dataset, hues = hue_categories)

    print("Preparing EDA tables...")
    # Generate Tables
    tables = generate_eda_tables(dataset, hues = hue_categories)

    if export:
        print("Saving plots and tables...")
        # Save Plots

        # Save Tables
    print("Completed generating descriptive statistics and data visualization!")


if __name__ == "__main__":
    data_path = ...
    main(data_path, export = False)