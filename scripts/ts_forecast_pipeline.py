#!/usr/bin/python
# A streamlined script of our generalized time series forecasting process
import darts
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

def main(data_path):
    # Analysis expectations formed after exploratory analysis
    # and client requirement gathering.
    suspected_stationarity = False
    suspected_seasonality = True
    suspected_trend = True

    # Time Series Statistical Tests 
    # stationarity?
    # seasonality?
    # trend?

    # if seasonality and trend:
        # ts models that I know about that are good for this.
    # elif not seasonality and not trend:
        # ts models that I know about that are good for this.

if __name__ == "__main__":
    data_path = ...
    main(data_path)