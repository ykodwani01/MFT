from indicator.trend import *
import pandas as pd

class Marubozu:
    def __init__(self, data):
        """
        Initialize with yfinance DataFrame
        data: pandas DataFrame with columns [Open, High, Low, Close, Adj Close, Volume]
        """
        self.data = data

    def _is_marubozu(self, candle, candle_type, params):
        # print(candle)
        open_price = candle['Open']
        high_price = candle['High']
        low_price = candle['Low']
        close_price = candle['Close']
        date = candle['Date']
        # Candle body length in %
        candle_length_pct = calculate_candle_length_percentage(open_price, close_price)
        # print(f"Candle /Length Percentage: {candle_length_pct}")
        if not (params["min_candle_length"] <= candle_length_pct <= params["max_candle_length"]):
            return False

        # Wick calculations
        if candle_type == "bullish":
            upper_wick = calculate_percentage_differences(high_price, close_price)
            lower_wick = calculate_percentage_differences(open_price, low_price)
            return upper_wick < params["upper_wick_threshold"] and \
                   lower_wick < params["lower_wick_threshold"] and \
                   is_bullish(open_price, close_price)

        elif candle_type == "bearish":
            upper_wick = calculate_percentage_differences(high_price, open_price)
            lower_wick = calculate_percentage_differences(low_price, close_price)
            return upper_wick < params["upper_wick_threshold"] and \
                   lower_wick < params["lower_wick_threshold"] and \
                   is_bearish(open_price, close_price)

        else:
            raise ValueError("candle_type must be either 'bullish' or 'bearish'")

    def _extract_candle_details(self, candle, candle_type):
        return {
            "date": candle['Date'],
            "type": candle_type,
            "open": candle['Open'],
            "high": candle['High'],
            "low": candle['Low'],
            "close": candle['Close'],
            "volume": candle['Volume']
        }

    def _detect_by_type(self, candle_type, params):
        results = []
        for index,candle in self.data.iterrows():
            if self._is_marubozu(candle, candle_type, params):
                results.append(self._extract_candle_details(candle, candle_type))
        return results

    def detect_all_marubozus(
        self,
        upper_wick_threshold=1.0,
        lower_wick_threshold=1.0,
        min_candle_length=1.5,
        max_candle_length=10.0
    ):
        """
        Detect all Marubozu Candles in the dataset.

        Returns:
            pd.DataFrame: DataFrame of detected Marubozu candles.
        """
        params = {
            "upper_wick_threshold": upper_wick_threshold,
            "lower_wick_threshold": lower_wick_threshold,
            "min_candle_length": min_candle_length,
            "max_candle_length": max_candle_length
        }

        bullish = self._detect_by_type("bullish", params)
        bearish = self._detect_by_type("bearish", params)
        return pd.DataFrame(bullish + bearish)
