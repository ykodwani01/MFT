import numpy as np
import pandas as pd

def calculate_percentage_differences(val1, val2):
    return abs(val1 - val2) / val2 * 100


def calculate_candle_length_percentage(open_price, close_price):
    return abs(close_price - open_price) / open_price * 100

def is_downtrend(candles, threshold=0.02):
    closes = [float(c["4. close"]) for c in candles]
    return (closes[-1] - closes[0]) > 0

def is_uptrend(candles, threshold=0.02):
    closes = [float(c["4. close"]) for c in candles]
    return (closes[0] - closes[-1]) > 0