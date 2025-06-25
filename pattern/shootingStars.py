import pandas as pd
import numpy as np
from indicator.trend import *

def is_shooting_star(date, candle,
                     body_ratio_threshold=0.25,
                     lower_wick_ratio_max=0.1,
                     upper_wick_body_ratio_min=2.5):

    open_price = float(candle["1. open"])
    close_price = float(candle["4. close"])
    high_price = float(candle["2. high"])
    low_price = float(candle["3. low"])

    high_body = high_price - max(open_price, close_price)
    body_low = min(open_price, close_price) - low_price
    body = abs(open_price - close_price)
    total_range = high_price - low_price

    # Sanity check to avoid division by zero
    if total_range == 0:
        return False

    # Conditions for a shooting star:
    # 1. Small real body near the low
    # 2. Long upper shadow (wick)
    # 3. Little to no lower shadow
    if body / total_range > body_ratio_threshold:
        return False  # Body is too large

    if body_low / total_range > lower_wick_ratio_max:
        return False  # Lower wick is too large

    if high_body / body < upper_wick_body_ratio_min:
        return False  # Upper wick not long enough

    return True

def detect_shooting_star(data,
                         body_ratio_threshold=0.25,
                         lower_wick_ratio_max=0.1,
                         upper_wick_body_ratio_min=2.5):
    time_series = data.get("Time Series (Daily)", {})
    results = []

    for date, candle in time_series.items():
        if is_shooting_star(date, candle,
                            body_ratio_threshold,
                            lower_wick_ratio_max,
                            upper_wick_body_ratio_min):
            results.append({
                "date": date,
                "open": float(candle["1. open"]),
                "high": float(candle["2. high"]),
                "low": float(candle["3. low"]),
                "close": float(candle["4. close"]),
                "volume": int(candle["5. volume"])
            })

    return results

def detect_all_shooting_stars(data,
                               body_ratio_threshold=0.25,
                               lower_wick_ratio_max=0.1,
                               upper_wick_body_ratio_min=2.5):
    results = detect_shooting_star(
        data,
        body_ratio_threshold,
        lower_wick_ratio_max,
        upper_wick_body_ratio_min
    )
    return pd.DataFrame(results)
