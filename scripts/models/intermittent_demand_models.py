#!/usr/bin/python
# A streamlined script of our time series forecasting process
# For time series data that can be characterized by having no values less than 0, no seasonality and no trend.
import darts
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

def main(data_path):
    # Analysis expectations formed after exploratory analysis
    # and client requirement gathering.
    suspected_stationarity = False
    suspected_seasonality = True
    suspected_trend = True


if __name__ == "__main__":
    data_path = ...
    main(data_path)