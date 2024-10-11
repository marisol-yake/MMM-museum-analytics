#!/usr/bin/python
from collections import defaultdict
from darts.statistics import check_seasonality, stationarity_tests, plot_residuals_analysis
import pandas as pd
import numpy as np
import math

# Time Series Functions
def gen_ts_features(df, date_column):
    # Generates Time Series Features based on date_column
    # Makes for easier analysis of operational (day-to-day) processes.
    df["day_of_week"] = df[date_column].dt.day_name()
    df["week_of_month"] = (df.date_column.day / 7).apply(lambda x: math.ceil(x))
    df["week_of_year"] = df[date_column].dt.isocalendar().week
    df["month_of_year"] = df[date_column].dt.month_name()
    df["year"] = df[date_column].dt.isocalendar().year

    return df

## Statistical Tests
def calc_trend_strength(series: pd.Series, order = 1) -> tuple[str, float]:
    # ref: https://stackoverflow.com/questions/55649356/how-can-i-detect-if-trend-is-increasing-or-decreasing-in-time-series
    index, data = series.index, series.values
    coeffs = np.polyfit(index, list(data), order)
    slope = float(coeffs[-2])
    
    # Qualitative measures of trend strength
    if slope >= 0.5:
        trend_strength = "Strong-Positive"
    elif slope < 0.5 and slope > 0:
        trend_strength = "Weak-Positive"
    elif slope <= -0.5:
        trend_strength = "Strong-Negative"
    elif slope > -0.5 and slope < 0:
        trend_strength = "Weak-Negative"

    return (trend_strength, slope)

def is_stationary(series, p_value: float = 0.05) -> bool:
    # Hypothesis Testing for Time Series data
    # Perform two separate stationarity tests
    result = stationarity_tests(series, p_value_threshold_adfuller = p_value, p_value_threshold_kpss = p_value)

    if result:
        print("The time series is stationary, p-value of {}".format(p_value))
    else:
        print("The time series is non-stationary.")

    return result

def has_seasonality(series, p_value: float = 0.05) -> tuple[bool, int]:
    result = check_seasonality(series, alpha = p_value)

    if result[0]:
        print("The time series has seasonality, with a period of {}".format(result[1]))
        print("P-value: {}".format(p_value))
    else:
        print("The time series does not have seasonality.")

    return result

def generate_model_recommendations(ts_test_results: defaultdict, intermittent: bool = False) -> defaultdict[str, darts.Model]:
    """
    Generates model recommendations based on statistical tests and knowledge about the dataset.
    
    Parameters
    ----------
    ts_test_results: defaultdict
        Results of time series statistical tests, used for determining time series model recommendations.
    intermittent: bool
        Describes external qualitative knowledge about the given data.
    """
    models = defaultdict()
    baseline_models = models.baseline_models
    
    # Intermittent Demand - No Seasonality and Difficult-to-Discern Trend
    if intermittent:
        # intermittent demand forecasting models
        models = models.id_models # CROSTON, SBA, TSB
    
    # Check for Stationarity
    if ts_test_results["Stationarity"] and not intermittent:
        models = models.auto_models
    
    elif not ts_test_results["Stationarity"] not intermittent:
        # Seasonality and Non-Negligible Trend
        if ts_test_results["Seasonality"] and np.abs(ts_test_results["Trend"][1]) >= 0.01:
            models = models.st_models
        
        # Seasonality and Negligible Trend
        elif ts_test_results["Seasonality"] and np.abs(ts_test_results["Trend"][1]) < 0.01:
            models = models.seasonal_models

    return baseline_models | models

def timeseries_stats_tests(series: pd.Series, model: str, p_value: float = 0.05) -> defaultdict:  
    return {
        "Stationarity": is_stationary(series, p_value = p_value), # returns a bool
        "Seasonality": has_seasonality(series, p_value = p_value)[0], # returns a bool
        "Trend": calc_trend_strength(series) # returns trend strength and slope
        }