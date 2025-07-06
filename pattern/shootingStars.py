from indicator.trend import *
import pandas as pd

class ShootingStar:
    def __init__(self, data, trend_lookback=7):
        """
        Initialize with yfinance DataFrame
        data: pandas DataFrame with columns [Open, High, Low, Close, Adj Close, Volume]
        """
        self.data = data.reset_index()
        self.trend_lookback = trend_lookback

    def _is_shooting_star(self, candle, params):
        open_price = candle['Open']
        high_price = candle['High']
        low_price = candle['Low']
        close_price = candle['Close']

        body_length = abs(close_price - open_price)
        total_range = high_price - low_price
        upper_wick = high_price - max(open_price, close_price)
        lower_wick = min(open_price, close_price) - low_price

        if total_range == 0:
            return False  # Prevent division by zero

        body_pct = (body_length / total_range) * 100
        upper_wick_pct = (upper_wick / total_range) * 100
        lower_wick_pct = (lower_wick / total_range) * 100

        return (
            body_pct <= params["max_body_pct"] and
            upper_wick_pct >= params["min_upper_wick_pct"] and
            lower_wick_pct <= params["max_lower_wick_pct"] and
            is_bearish(open_price, close_price)
        )

    def _extract_candle_details(self, candle, signal_type):
        return {
            "date": candle['Date'],
            "open": candle['Open'],
            "high": candle['High'],
            "low": candle['Low'],
            "close": candle['Close'],
            "volume": candle['Volume'],
            "type": signal_type
        }

    def detect_shooting_stars(
        self,
        max_body_pct=30.0,
        min_upper_wick_pct=65.0,
        max_lower_wick_pct=15.0
    ):
        """
        Detect trend-confirmed Shooting Star candles.

        Returns:
            pd.DataFrame: DataFrame of shooting star signals with type: bullish/bearish
        """
        params = {
            "max_body_pct": max_body_pct,
            "min_upper_wick_pct": min_upper_wick_pct,
            "max_lower_wick_pct": max_lower_wick_pct
        }

        results = []
        for i in range(self.trend_lookback, len(self.data)):
            candle = self.data.iloc[i]

            if not self._is_shooting_star(candle, params):
                continue

            close_series = self.data["Close"].iloc[i - self.trend_lookback:i]
            dates = self.data["Date"].iloc[i - self.trend_lookback:i]
            # print(close_series)
            # print(dates)

            if is_downtrend(close_series):
                signal_type = "bullish"
            elif is_uptrend(close_series):
                signal_type = "bearish"
            else:
                continue  # No signal if trend is unclear

            results.append(self._extract_candle_details(candle, signal_type))

        return pd.DataFrame(results)
