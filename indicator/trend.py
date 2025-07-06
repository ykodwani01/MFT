import numpy as np
import pandas as pd

def calculate_percentage_differences(val1, val2):
    return abs(val1 - val2) / val2 * 100


def calculate_candle_length_percentage(open_price, close_price):
    return abs(close_price - open_price) / open_price * 100

def is_downtrend(closes, threshold=0.03):
    """
    True if price dropped >= threshold AND at least 50% of candles are red (i.e., close[i] < close[i-1])
    """
    pct_change = (closes.iloc[-1] - closes.iloc[0]) / closes.iloc[0]

    # Count how many candles are red
    red_count = sum(closes.iloc[i] < closes.iloc[i - 1] for i in range(1, len(closes)))
    red_ratio = red_count / (len(closes) - 1)

    return pct_change <= -threshold and red_ratio >= 0.5

def is_uptrend(closes, threshold=0.03):
    """
    True if price rose >= threshold AND at least 50% of candles are green (i.e., close[i] > close[i-1])
    """
    pct_change = (closes.iloc[-1] - closes.iloc[0]) / closes.iloc[0]

    green_count = sum(closes.iloc[i] > closes.iloc[i - 1] for i in range(1, len(closes)))
    green_ratio = green_count / (len(closes) - 1)

    return pct_change >= threshold and green_ratio >= 0.5

def is_bearish(open_price,close_price):
    return close_price < open_price

def is_bullish(open_price,close_price):
    return close_price > open_price