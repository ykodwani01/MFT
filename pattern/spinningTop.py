from indicator.trend import calculate_percentage_differences, calculate_candle_length_percentage, is_downtrend, is_uptrend
import pandas as pd
import numpy as np
def is_spinning(candle,
    upper_wick_threshold=1.0,
    lower_wick_threshold=1.0,
    min_candle_length=1.0,
    max_candle_length=10.0,
    body_percent=0.32,
    shadow_threshold=0.04):

    open_price = float(candle["1. open"])
    close_price = float(candle["4. close"])
    high_price = float(candle["2. high"])
    low_price = float(candle["3. low"])

    high_close_diff_pct = calculate_percentage_differences(high_price, close_price)
    open_low_diff_pct = calculate_percentage_differences(open_price, low_price)
    high_open_diff_pct = calculate_percentage_differences(high_price, open_price)
    close_low_diff_pct = calculate_percentage_differences(close_price, low_price)

    candle_length_pct = calculate_candle_length_percentage(open_price, close_price)

    total_range = abs(high_price-low_price)
    body_size = abs(open_price-close_price)
    upper_wick = high_price - max(open_price, close_price)
    lower_wick = min(open_price, close_price) - low_price

    upper_wick_pct = calculate_percentage_differences(high_price, max(open_price, close_price))
    lower_wick_pct = calculate_percentage_differences(min(open_price, close_price), low_price)
    # print(body_size,body_percent,total_range)
    if body_size > body_percent * total_range:
        return False

    if abs(upper_wick - lower_wick) > shadow_threshold*100:
        return False

    return True


def detect_spinningTop(data,
    upper_wick_threshold=1.0,
    lower_wick_threshold=1.0,
    min_candle_length=1.0,
    max_candle_length=10.0):
    time_series = data.get("Time Series (Daily)", {})
    results = []

    for date, candle in time_series.items():
        if is_spinning(
            candle,
            upper_wick_threshold,
            lower_wick_threshold,
            min_candle_length,
            max_candle_length
        ):
            results.append({
                "date": date,
                "open": float(candle["1. open"]),
                "high": float(candle["2. high"]),
                "low": float(candle["3. low"]),
                "close": float(candle["4. close"]),
                "volume": int(candle["5. volume"])
            })

    return results

def detect_all_spinning(data,
    upper_wick_threshold=1.0,
    lower_wick_threshold=1.0,
    min_candle_length=1.0,
    max_candle_length=10.0):
    print(data)
    results = detect_spinningTop(
        data,
        upper_wick_threshold,
        lower_wick_threshold,
        min_candle_length,
        max_candle_length
    )

    return pd.DataFrame(results)
