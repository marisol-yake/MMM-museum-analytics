#!/usr/bin/python
# A streamlined script of our time series forecasting process
# For time series data that can be characterized by having seasonality and trend.
from darts.models.forecasting import Croston, NaiveDrift, NaiveMovingAverage, ExponentialSmoothing


baseline_models = {
    "Naive": NaiveDrift(),
    # AR
    "Moving Average": NaiveMovingAverage(),
    "Exponential Smoothing": ExponentialSmoothing()
}

# Time Series Forecasting Models specializing in data
# with seasonality and trend.
st_models = {}

# Time Series Forecasting Models specializing in data
# with seasonality and negligible trend.
seasonal_models = {}

# Intermittent Demand Forecasting Models that I can currently support
id_models = {
    "CROSTON Method": Croston(version = "classic"),
    "SBA": Croston(version = "sba"),  # Syntetos-Boylan Approximation
    "TSB": Croston(version = "tsb")  # Teunter-Syntetos-Babai
}

# Models which I understand support forecasting
# on data with stationarity.
auto_models = {
    # ARIMA
    # SARIMA
    # SARIMAX
    # VARIMA
    # ETS
}

# TODO: Implement for forecasting windows.
# Darts: Automatically does proper tscv on data for free.
# def perform_gridsearchcv(*models, **kwargs):
#     for model in models:
#         model.gridsearchcv(*kwargs)