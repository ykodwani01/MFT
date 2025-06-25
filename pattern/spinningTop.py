import pandas as pd
from indicator.trend import calculate_percentage_differences, calculate_candle_length_percentage

def is_spinning_top(candle, 
                    body_ratio_threshold=0.3, 
                    shadow_diff_threshold=0.05):
    open_price = float(candle["1. open"])
    close_price = float(candle["4. close"])
    high_price = float(candle["2. high"])
    low_price = float(candle["3. low"])

    body = abs(open_price - close_price)
    total_range = high_price - low_price

    # Prevent division by zero
    if total_range == 0:
        return False

    upper_wick = high_price - max(open_price, close_price)
    lower_wick = min(open_price, close_price) - low_price

    # 1. Small body
    if body / total_range > body_ratio_threshold:
        return False

    # 2. Both wicks should be nearly equal
    wick_diff_ratio = abs(upper_wick - lower_wick) / total_range
    if wick_diff_ratio > shadow_diff_threshold:
        return False

    return True

def detect_spinning_tops(data,
                         body_ratio_threshold=0.3,
                         shadow_diff_threshold=0.05):
    time_series = data.get("Time Series (Daily)", {})
    results = []

    for date, candle in time_series.items():
        if is_spinning_top(candle, body_ratio_threshold, shadow_diff_threshold):
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
                              body_ratio_threshold=0.2,
                              shadow_diff_threshold=0.05):
    spinning_tops = detect_spinning_tops(
        data,
        body_ratio_threshold,
        shadow_diff_threshold
    )
    return pd.DataFrame(spinning_tops)
