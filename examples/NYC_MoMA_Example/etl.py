#!/usr/bin/python
import os
import re
import pandas as pd
import numpy as np


########################################################################################
# Overall Data Pipeline // Data Cleaning procedures
def start_pipeline(df):
    # Prevents overwriting data in the pipeline process
    return df.copy()

def sort_data(df):
    return df.sort_values(by = ["acquisition_date", "object_number"], ascending = True, axis = "rows")

def clean_column_names(df):
    # Prepares column names for easier analysis
    clean_column_name = lambda x: x.strip().lower().replace(" ", "_").replace("(", "").replace(")", "")
    df.columns = [clean_column_name(col) for col in df.columns]
    return df


def ensure_dataset_types(df):
    df["acquisition_date"] = pd.to_datetime(df["acquisition_date"], format = "%Y-%m-%d", errors = "coerce")
    df["date"] = pd.to_datetime(df["date"], format = "%Y", errors = "coerce", exact = False)
    return df


def fill_null_values(df):
    return df.assign(
        acquisition_date = df["acquisition_date"].ffill(),  # Client-approved: Forward-fill missing date values
        width_cm = df["width_cm"].fillna(df["length_cm"]),  # Client-sourced: length-to-width null-fill strategy
        depth_cm = df["depth_cm"].fillna(df["diameter_cm"]),  # Client-sourced: diameter-to-depth null-fill strategy
    )


def group_categorical_features(df):
    return df.assign(
        credit_group = df["credit"].astype(str).apply(credit_to_credit_group),  # ref:
        storage_group = df["classification"].apply(classification_to_storage_group),  # Client-sourced: storage group strategy
    )


def generate_spatial_features(df):
    cm_to_foot_conversion_factor = 0.0328084
    return df.assign(
        height_ft = df["height_cm"]* cm_to_foot_conversion_factor,  # Client-approved: converted to height (in feet)
        width_ft = df["width_cm"] * cm_to_foot_conversion_factor,  # Client-approved: converted to width (in feet)
        depth_ft = df["depth_cm"] * cm_to_foot_conversion_factor,  # Client-approved: converted to depth (in feet)
    )


def calculate_totals(df):
    df["cubic_ft"] = (df["height_ft"] * df["width_ft"] * df["depth_ft"])  # calculates total cubic_ft
    df["spatial_running_total"] = df["cubic_ft"].cumsum().astype(float)  # captures the total collection space-use over-time
    df["acq_total"] = df.groupby(["acquisition_date"])["acquisition_date"].transform("size")  # calculates the total records per accession date
    df["acq_gaps"] = df["acquisition_date"].diff()  # the gaps between acquisition dates
    return df


def drop_columns(df):
    return df.drop(
        columns=[
            "artwork_id",
            "artist_id",
            "catalogue",
            "title",
            "name",
            "medium",
            "circumference_cm",
            "weight_kg",
            "duration_s",
            "dimensions",
            "diameter_cm",
            "length_cm",
            "height_cm",
            "width_cm",
            "depth_cm",
        ]
    )


# Custom Null Value Fill Strategies
def fill_missing_by_dept_avg(df):
    fill_nulls_by_average = lambda x: x.fillna(x.mean())
    df.loc[:, "height_ft"] = df.groupby("department")["height_ft"].transform(fill_nulls_by_average)
    df.loc[:, "width_ft"] = df.groupby("department")["width_ft"].transform(fill_nulls_by_average)
    df.loc[:, "depth_ft"] = df.groupby("department")["depth_ft"].transform(fill_nulls_by_average)
    return df


def fill_missing_by_storage_group_avg(df):
    fill_nulls_by_average = lambda x: x.fillna(x.mean())
    df.loc[:, "height_ft"] = df.groupby("storage_group")["height_ft"].transform(fill_nulls_by_average)
    df.loc[:, "width_ft"] = df.groupby("storage_group")["width_ft"].transform(fill_nulls_by_average)
    df.loc[:, "depth_ft"] = df.groupby("storage_group")["depth_ft"].transform(fill_nulls_by_average)
    return df


########################################################################################
# Custom Data Cleaning // Grouping Functions
def credit_to_credit_group(credit: str):
    credit = credit.strip().lower()
    if re.search(r"purchase", credit): return "Purchase"
    elif re.search(r"gift|given|generrosity", credit): return "Gift"
    elif re.search(r"partial", credit): return "Partial Gift Partial Purchase"
    elif re.search(r"exchange", credit): return "Exchange"
    elif re.search(r"fund", credit): return "Fund"
    else: return "Other"


def classification_to_storage_group(classification: str):
    classification = classification.strip().lower()
    if re.search(r"print|draw|on paper|collage", classification): return "Works on Paper"
    elif re.search(r"photo|film", classification): return "Photo"
    elif re.search(r"illustrate|book|periodic|ephemera", classification): return "Archive"
    elif re.search(r"architecture|design|frank lloyd wright|Mies van der Rohe", classification): return "Architecture & Design"
    elif re.search(r"video|audio|media|performance|software", classification): return "Time-based"
    elif re.search(r"paint", classification): return "Painting"
    elif re.search(r"sculpture", classification): return "Sculpture"
    elif re.search(r"multiple", classification): return "Multiple"
    elif re.search(r"installation|production design", classification): return "Production Design"
    elif re.search(r"textile", classification): return "Textile"
    elif re.search(r"furniture", classification): return "Furniture"
    else: return "Other"


########################################################################################
# Data Pipeline
def clean_data(file_path):
    data = pd.read_csv(file_path)

    # Cleaning datasets for comparison
    cleaned_data = (
        data.pipe(start_pipeline)
        .pipe(clean_column_names)
        .pipe(ensure_dataset_types)
        .pipe(fill_null_values)
        .pipe(sort_data)
        .pipe(group_categorical_features)
        .pipe(generate_spatial_features)
        .pipe(calculate_totals)
        # missing value (imputation) strategy -- unmodified
        .pipe(drop_columns)
    )

    drop_all_nulls_data = (
        data.pipe(start_pipeline)
        .pipe(clean_column_names)
        .pipe(ensure_dataset_types)
        .pipe(fill_null_values)
        .pipe(sort_data)
        .pipe(group_categorical_features)
        .pipe(generate_spatial_features)
        .pipe(calculate_totals)
        .pipe(drop_columns)
        .dropna()  # missing value (imputation) strategy
    )

    dept_avg_fill_data = (
        data.pipe(start_pipeline)
        .pipe(clean_column_names)
        .pipe(ensure_dataset_types)
        .pipe(fill_null_values)
        .pipe(sort_data)
        .pipe(group_categorical_features)
        .pipe(generate_spatial_features)
        .pipe(fill_missing_by_dept_avg)  # missing value (imputation) strategy
        .pipe(calculate_totals)
        .pipe(drop_columns)
    )

    storage_group_avg_fill_data = (
        data.pipe(start_pipeline)
        .pipe(clean_column_names)
        .pipe(ensure_dataset_types)
        .pipe(fill_null_values)
        .pipe(sort_data)
        .pipe(group_categorical_features)
        .pipe(generate_spatial_features)
        .pipe(fill_missing_by_storage_group_avg)  # missing value (imputation) strategy
        .pipe(calculate_totals)
        .pipe(drop_columns)
    )

    return (
        cleaned_data,
        drop_all_nulls_data,
        dept_avg_fill_data,
        storage_group_avg_fill_data,
    )


if __name__ == "__main__":
    file_path = "./data/MoMA NYC artworks.csv"
    out = clean_data(file_path)
