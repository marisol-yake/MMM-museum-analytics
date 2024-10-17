#!/usr/bin/python
from collections import defaultdict
import darts
from darts.utils.statistics import check_seasonality, stationarity_tests, plot_residuals_analysis
import pandas as pd
import numpy as np
from .config import setup_logging


logger = setup_logging("ts_statistics")


# Time Series Functions
def generate_ts_features(df: pd.DataFrame, date_column: str, add_cols: list[str]) -> pd.DataFrame:
    """
    Generates times series features onto a new pd.DataFrame for a given date column. 
    Especially useful for analyzing data at the operational (day-to-day) level.

    Parameters
    ----------
    df: pd.DataFrame
        The dataset of interest, used for copying and subsetting, 
        before generating novel features.
    date_column: str
        The column, containing the Pandas datatype: `datetime[ns]`, used for 
        generating: *day_of_week*, *week_of_month*, *week_of_year*, *month_of_year*, *year*.
    *add_cols: str
        Additional columns for more thorough analysis. 
        Can be categorical or numerical.
        e.g. department, credit, backlog_count, etc.

        Initially intended for quantitative columns, 
        later generalized to include qualitative columns.

    Returns
    ----------
    table: pd.DataFrame
        A copy and subset of a pandas DataFrame containing new time series 
        features based on the specified date column.
    """
    # Generates Time Series Features based on date_column
    # Makes for easier analysis of operational (day-to-day) processes.
    try:
        logger.info("Generating operational time series features.")
        df = df[[date_column] + add_cols].copy()
        df[date_column] = pd.to_datetime(df[date_column], format = "%m/%d/%Y", errors = "coerce")

        df["day"] = df[date_column].dt.isocalendar().day
        df["day_of_week"] = df[date_column].dt.day_name()
        df["day_of_month"] = (df[date_column].dt.day / 30.5).apply(lambda x: np.ceil(x))
        df["week_of_month"] = (df[date_column].dt.day / 7).apply(lambda x: np.ceil(x))
        df["week"] = df[date_column].dt.isocalendar().week
        df["month"] = df[date_column].dt.month
        df["year"] = df[date_column].dt.isocalendar().year

    except Exception as e:
        logger.error("Encountered error when generating operational time series features: {}".format(e))
        raise Exception("Encountered error when generating operational time series features: {}".format(e))

    logger.info("Successfully generated operational time series features {}".format(df.columns[-7:].values))
    return df


# Statistical Tests
def calculate_trend_strength(series: pd.Series, degree: int = 1) -> tuple[str, float]:
    """
    Calculates the OLS fit of a series' data.
    Analytical shorthand for understanding the underlying trend of a series.

    Parameters
    ----------
    series: pd.Series
        pd.Series instance, especially a time series, containing an index and a quantity.
    degree: int
        The degrees of polynomial fit. 
        Uses numpy Polynomial implementation to fit a 1-degree least squares fit.
    """
    # REF: https://stackoverflow.com/questions/55649356/how-can-i-detect-if-trend-is-increasing-or-decreasing-in-time-series
    try:
        logger.info("Calculating the {}-degree Line of Best Fit.".format(degree))
        index, data = series.index, series.values
        coeffs = np.polynomial.polynomial.Polynomial.fit(index, list(data), degree = degree)
        slope = float(coeffs[-2])

        logger.info("Determining the strength of the trend.")
        # Qualitative measures of trend strength
        if slope >= 0.5:
            trend_strength = "Strong-Positive"
        elif slope < 0.5 and slope > 0:
            trend_strength = "Weak-Positive"
        elif slope <= -0.5:
            trend_strength = "Strong-Negative"
        elif slope > -0.5 and slope < 0:
            trend_strength = "Weak-Negative"

    except Exception as e:
        logger.error("Encountered an error while calculating the line of best fit: {}".format(e))
        raise Exception("Encountered an error while calculating the line of best fit: {}".format(e))

    logger.info("Successfully determined the line of best fit and its strength.")
    return (trend_strength, slope)


def is_stationary(series, p_value: float = 0.05) -> bool:
    """
    Uses the null-hypothesis to test for whether or not
    a given time series has stationarity.

    Parameters
    ----------
    series: pd.Series
        pd.Series instance, especially a time series,
        containing an index and a quantity.
    p_value: float
        Example writing.
    """
    # Hypothesis Testing for Time Series data
    # Perform two separate stationarity tests
    try:
        logger.info("Testing the time series data for stationarity.")
        result = stationarity_tests(series,
                                    p_value_threshold_adfuller=p_value,
                                    p_value_threshold_kpss=p_value)
        if result:
            logger.info("The time series exhibits stationarity, p-value of {}".format(p_value))
        else:
            logger.info("The time series does not exhibit stationarity, p-value of {}".format(p_value))

    except Exception as e:
        logger.error("Encountered an error while testing time series for stationarity: {}".format(e))
        raise Exception("Encountered an error while testing time series for stationarity: {}".format(e))

    logger.info("Successfully tested the time series for stationarity.")
    return result


def has_seasonality(series, p_value: float = 0.05) -> tuple[bool, int]:
    """
    Employs statistical tests to determine whether or not
    a given time series has seasonality.

    Parameters
    ----------
    series: pd.Series
        pd.Series instance, especially a time series, containing an index and a quantity.
    p_value: float
        Example writing.
    """
    try:
        logger.info("Testing the time series data for seasonality.")
        result = check_seasonality(series, alpha = p_value)

        if result[0]:
            print("The time series has seasonality, with a period of {}".format(result[1]))
            print("P-value: {}".format(p_value))
        else:
            print("The time series does not have seasonality.")

    except Exception as e:
        logger.error("Encountered an error while testing the time series data for seasonality: {}".format(e))
        raise Exception("Encountered an error while testing the time series data for seasonality: {}".format(e))

    logger.info("Succesfully tested the time series data for seasonality.")
    return result


def generate_tsmodel_recommendations(ts_test_results: defaultdict, intermittent: bool = False, prediction_type: str = "point") -> defaultdict:
    """
    Generates model recommendations based on statistical tests and knowledge about the dataset.

    Parameters
    ----------
    ts_test_results: defaultdict
        Results of time series statistical tests, used for determining time series model recommendations.
    intermittent: bool
        Describes external qualitative knowledge about the given data.
    """
    try:
        logger.info("Generating forecasting model recommendations.")
        models = ts_models.baseline_models | defaultdict()

        # Intermittent Demand - No Seasonality and Difficult-to-Discern Trend
        if intermittent:
            # intermittent demand forecasting models
            models |= models.id_models  # CROSTON, SBA, TSB

        # Check for Stationarity
        if ts_test_results["Stationarity"] and not intermittent:
            models |= models.auto_models

        elif not ts_test_results["Stationarity"] and not intermittent:
            # Seasonality and Non-Negligible Trend
            if ts_test_results["Seasonality"] and np.abs(ts_test_results["Trend"][1]) >= 0.01:
                models |= models.st_models

            # Seasonality and Negligible Trend
            elif ts_test_results["Seasonality"] and np.abs(ts_test_results["Trend"][1]) < 0.01:
                models |= models.seasonal_models

        # Filter recommendations by prediction_type, useful for comparisons
        match prediction_type:
            case "point|deterministic":
                models = filter_models(models, lambda model: not model.supports_probabilistic_predictions)

            case "prob|probabilistic":
                models = filter_models(models, lambda model: model.supports_probabilistic_predictions)

    except Exception as e:
        logger.error("Encountered an error while generating forecasting model recommendations: {}".format(e))
        raise Exception("Encountered an error while generating forecasts model recommendations: {}".format(e))

    logger.info("Successfully generated forecasts model recommendations: {}".format(models))

    return models


def filter_models(models: defaultdict, condition) -> defaultdict:
    # deterministic | probabilistic/stochastic
    # Dev Note: hack to maintain defaultdict type
    models_out = defaultdict(darts.models.Model)
    return models_out | {
        model_name: models[model_name]
        for model_name in models
        if condition
        }


def timeseries_stats_tests(series: pd.Series, model: str, p_value: float = 0.05) -> defaultdict:
    """
    Uses statistical tests to get a critical high-level summary of
    the time series data characteristics, particularly useful for forecasting purposes.

    Parameters
    ----------
    series: pd.Series
        Example writing.
    model: str
        Example writing.
    p_value: float
        Example writing.
    """
    try:
        logger.info("Performing statistical time series tests.")
        stationarity = is_stationary(series, p_value=p_value),  # returns a bool
        seasonality = has_seasonality(series, p_value=p_value)[0],  # returns a bool
        trend = calculate_trend_strength(series)  # returns trend strength and slope

    except Exception as e:
        logger.error("Encountered an error when performing statistical tests on time series data: {}".format(e))
        raise Exception("Encountered an error when performing statistical tests on time series data: {}".format(e))

    logger.info("Successfully performed all statistical time series tests.")
    logger.info("Stationarity: {}\nSeasonality: {}\nTrend: {}".format(stationarity, seasonality, trend))
    return {
        "Stationarity": stationarity,
        "Seasonality": seasonality,
        "Trend": trend,
        }