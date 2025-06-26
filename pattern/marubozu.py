from indicator.trend import *
import pandas as pd

class Marubozu:
    def __init__(self, data):
        self.data = data

    def _is_marubozu(self, candle, candle_type, params):
        open_price = float(candle["1. open"])
        high_price = float(candle["2. high"])
        low_price = float(candle["3. low"])
        close_price = float(candle["4. close"])

        # Candle body length in %
        candle_length_pct = calculate_candle_length_percentage(open_price, close_price)
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

    def _extract_candle_details(self, date, candle, candle_type):
        return {
            "date": date,
            "type": candle_type,
            "open": float(candle["1. open"]),
            "high": float(candle["2. high"]),
            "low": float(candle["3. low"]),
            "close": float(candle["4. close"]),
            "volume": float(candle["5. volume"])
        }

    def _detect_by_type(self, candle_type, params):
        results = []
        for date, candle in self.data.items():
            if self._is_marubozu(candle, candle_type, params):
                results.append(self._extract_candle_details(date, candle, candle_type))
        return results

    def detect_all_marubozus(
        self,
        upper_wick_threshold=1.0,
        lower_wick_threshold=1.0,
        min_candle_length=1.0,
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
