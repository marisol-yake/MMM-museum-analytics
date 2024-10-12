#!/usr/bin/python
# A streamlined script of our generalized time series forecasting process
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from ts_statistics import timeseries_stats_tests, generate_tsmodel_recommendations
from utils import load_dataset

def main(data_path):
    # Cleaned dataset
    data = load_dataset(data_path, )

    # Time Series Statistical Tests
    results = timeseries_stats_tests(series)

    # Generate model recommendations based on statistical tests
    models = generate_tsmodel_recommendations(results)
    
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