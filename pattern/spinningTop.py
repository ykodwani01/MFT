from indicator.trend import *
import pandas as pd

class SpinningTop:
    def __init__(self, data, trend_lookback=7):
        """
        Initialize with yfinance DataFrame
        data: pandas DataFrame with columns [Open, High, Low, Close, Adj Close, Volume]
        """
        self.data = data.reset_index()
        self.trend_lookback = trend_lookback

    def _is_spinning_top(self, candle, params):
        open_price = candle['Open']
        high_price = candle['High']
        low_price = candle['Low']
        close_price = candle['Close']

        body_length = abs(close_price - open_price)
        total_range = high_price - low_price
        upper_wick = high_price - max(open_price, close_price)
        lower_wick = min(open_price, close_price) - low_price

        if total_range == 0:
            return False  # Avoid division by zero

        body_pct = (body_length / total_range) * 100
        upper_wick_pct = (upper_wick / total_range) * 100
        lower_wick_pct = (lower_wick / total_range) * 100

        return (
            body_pct <= params["max_body_pct"] and
            upper_wick_pct >= params["min_wick_pct"] and
            lower_wick_pct >= params["min_wick_pct"]
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

    def detect_spinning_tops(
        self,
        max_body_pct=30.0,
        min_wick_pct=30.0
    ):
        """
        Detect all trend-confirmed Spinning Top candles.

        Returns:
            pd.DataFrame: DataFrame of bullish/bearish spinning tops with trend context.
        """
        params = {
            "max_body_pct": max_body_pct,
            "min_wick_pct": min_wick_pct
        }

        results = []
        for i in range(self.trend_lookback, len(self.data)):
            candle = self.data.iloc[i]

            if not self._is_spinning_top(candle, params):
                continue

            # Determine trend based on close prices before the candle
            close_series = self.data["Close"].iloc[i - self.trend_lookback:i]
            dates = self.data["Date"].iloc[i - self.trend_lookback:i]
            # print(close_series)
            # print(dates)
            if is_downtrend(close_series):
                signal_type = "bullish"
            elif is_uptrend(close_series):
                signal_type = "bearish"
            else:
                continue  # Ignore if no clear trend

            results.append(self._extract_candle_details(candle, signal_type))

        return pd.DataFrame(results)
