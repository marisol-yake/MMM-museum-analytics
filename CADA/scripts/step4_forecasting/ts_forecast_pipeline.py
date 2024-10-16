#!/usr/bin/python
# A streamlined script of our generalized time series forecasting process
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from ts_statistics import timeseries_stats_tests, generate_tsmodel_recommendations
from utils import load_dataset
from config import setup_logging

logger = setup_logging("ts_forecast_pipeline")


def main(data_path):
    logger.info("Beginning time series forecasting pipeline.")
    # Cleaned dataset
    data = load_dataset(data_path)  # Load into darts.TimeSeries object
    target_series = TimeSeries(data, "adate_sum")

    logger.info("Splitting data into target (count) series and exogenous (external) variables.")
    logger.info("Setting aside data for CatBoost.")
    # Catboost performs better without categorical encoding
    catboost_exo_series = TimeSeries(data,
                                     # Custom Time Series Features
                                     ["lag_1", "lag_2", "lag_3", "lag_4",
                                      "lag_5", "lag_10", "lag_15", "lag_20",
                                      "day", "day_of_week", "day_of_month",
                                      "week_of_month", "week", "month_of_year",
                                      "month", "year"])

    logger.info("Encoding categorical variables for all other models.")
    # exogenous_series = data.copy().apply(CategoricalEncoder().transform())
    exogenous_series = TimeSeries(data,
                                  # Custom Time Series Features
                                  ["lag_1", "lag_2", "lag_3", "lag_4",
                                   "lag_5", "lag_10", "lag_15", "lag_20",
                                   "day", "day_of_week", "day_of_month",
                                   "week_of_month", "week", "month_of_year",
                                   "month", "year"])

    # Time Series Statistical Tests
    results = timeseries_stats_tests(series)

    logger.info("Generating Time Series Model Recommendations.")
    # Generate model recommendations based on statistical tests
    models = generate_tsmodel_recommendations(results,
                                              intermittent = True,
                                              forecast_type = "point")

    logger.info("Splitting time series data for cross-validation.")
    # Time Series Data Cross-Validation
    tscv = TimeSeriesSplit(n = 5)

    # Generate model metrics from fit (predictions against true data)

    # Select models based on any number of preferred metrics
    # (since there is no one-size fits all metric)

    # Check for overfitting and underfitting of models

    # Generate necessary predictions
    pass

if __name__ == "__main__":
    data_path = ...
    main(data_path)
