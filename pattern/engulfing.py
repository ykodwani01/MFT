from indicator.trend import *
import pandas as pd

def is_bullish_engulfing(prev_candle, current_candle):
    prev_open = float(prev_candle["1. open"])
    prev_close = float(prev_candle["4. close"])
    current_open = float(current_candle["1. open"])
    current_close = float(current_candle["4. close"])

    return (prev_close < prev_open and current_close > current_open and
            current_open < prev_close and current_close > prev_open)

def is_bearish_engulfing(prev_candle, current_candle):
    prev_open = float(prev_candle["1. open"])
    prev_close = float(prev_candle["4. close"])
    current_open = float(current_candle["1. open"])
    current_close = float(current_candle["4. close"])

    return (prev_close > prev_open and current_close < current_open and
            current_open > prev_close and current_close < prev_open)

def detect_all_engulfing(data, lookback=5):
    time_series = data.get("Time Series (Daily)", {})
    if not time_series:
        raise ValueError("Missing 'Time Series (Daily)' in input data.")

    # Sort dates oldest to newest
    sorted_dates = sorted(time_series.keys())

    results = []

    for idx in range(lookback, len(sorted_dates)):
        date_prev = sorted_dates[idx - 1]
        date_curr = sorted_dates[idx]
        prev_candle = time_series[date_prev]
        current_candle = time_series[date_curr]

        # Ensure we have enough previous candles for trend check
        prev_candle_dates = sorted_dates[idx - lookback:idx]
        if len(prev_candle_dates) < lookback:
            continue
        prev_candles = [time_series[d] for d in prev_candle_dates]

        # Bullish engulfing after downtrend
        if is_downtrend(prev_candles) and is_bullish_engulfing(prev_candle, current_candle):
            results.append({
                "pattern": "Bullish Engulfing",
                "date": date_curr,
                "open": float(current_candle["1. open"]),
                "high": float(current_candle["2. high"]),
                "low": float(current_candle["3. low"]),
                "close": float(current_candle["4. close"]),
                "volume": int(current_candle["5. volume"]),
                "entry_price": float(current_candle["4. close"]),
                "stop_loss": min(float(prev_candle["3. low"]), float(current_candle["3. low"])),
                "prev_candle_close": float(prev_candle["4. close"])
            })

        # Bearish engulfing after uptrend
        if is_uptrend(prev_candles) and is_bearish_engulfing(prev_candle, current_candle):
            results.append({
                "pattern": "Bearish Engulfing",
                "date": date_curr,
                "open": float(current_candle["1. open"]),
                "high": float(current_candle["2. high"]),
                "low": float(current_candle["3. low"]),
                "close": float(current_candle["4. close"]),
                "volume": int(current_candle["5. volume"]),
                "entry_price": float(current_candle["4. close"]),
                "stop_loss": max(float(prev_candle["2. high"]), float(current_candle["2. high"])),
                "prev_candle_close": float(prev_candle["4. close"])
            })

    return pd.DataFrame(results)