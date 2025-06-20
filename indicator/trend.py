import numpy as np
import pandas as pd

def calculate_percentage_differences(val1, val2):
    return abs(val1 - val2) / val2 * 100


def calculate_candle_length_percentage(open_price, close_price):
    return abs(close_price - open_price) / open_price * 100

def is_downtrend(candles, window=2):
    """Check for a downtrend using moving average of LOW prices"""
    low_prices =[float(c["3. low"]) for c in candles]

    if len(low_prices) < window:
        return True  # not enough data to form a trend

    moving_avg = [np.mean(low_prices[i:i+window]) for i in range(len(low_prices) - window + 1)]

    return all(earlier <= later for earlier, later in zip(moving_avg, moving_avg[1:]))

def is_uptrend(candles, window=2):
    """Check for an uptrend using moving average of LOW prices"""
    low_prices = [float(c["3. low"]) for c in candles]

    if len(low_prices) < window:
        return True  # not enough data to form a trend

    moving_avg = [np.mean(low_prices[i:i+window]) for i in range(len(low_prices) - window + 1)]

    return all(earlier >= later for earlier, later in zip(moving_avg, moving_avg[1:]))
