from indicator.trend import *
import pandas as pd

class EngulfingPattern:
    def __init__(self, data, trend_lookback=7, min_body_pct=0.7):
        """
        data: DataFrame with OHLCV (from yfinance)
        trend_lookback: candles to consider for trend check
        min_body_pct: minimum body size (as % of range) to be considered a strong candle
        """
        self.data = data.reset_index()
        self.trend_lookback = trend_lookback
        self.min_body_pct = min_body_pct

    def _body_pct(self, candle):
        body = abs(candle["Close"] - candle["Open"])
        rng = candle["High"] - candle["Low"]
        return (body / rng) * 100 if rng > 0 else 0

    def _is_bullish_engulfing(self, prev_candle, curr_candle):
        return (
            is_bearish(prev_candle['Open'], prev_candle['Close']) and
            is_bullish(curr_candle['Open'], curr_candle['Close']) and
            curr_candle['Open'] < prev_candle['Close'] and
            curr_candle['Close'] > prev_candle['Open']
        )

    def _is_bearish_engulfing(self, prev_candle, curr_candle):
        return (
            is_bullish(prev_candle['Open'], prev_candle['Close']) and
            is_bearish(curr_candle['Open'], curr_candle['Close']) and
            curr_candle['Open'] > prev_candle['Close'] and
            curr_candle['Close'] < prev_candle['Open']
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

    def detect_engulfing_patterns(self):
        results = []
        for i in range(self.trend_lookback + 1, len(self.data)):
            prev_candle = self.data.iloc[i - 1]
            curr_candle = self.data.iloc[i]

            # Skip if any body is too small (noise candle)
            if self._body_pct(prev_candle) < self.min_body_pct or self._body_pct(curr_candle) < self.min_body_pct:
                continue

            close_series = self.data["Close"].iloc[i - self.trend_lookback - 1 : i - 1]

            if self._is_bullish_engulfing(prev_candle, curr_candle) and is_downtrend(close_series):
                signal_type = "bullish"
            elif self._is_bearish_engulfing(prev_candle, curr_candle) and is_uptrend(close_series):
                signal_type = "bearish"
            else:
                continue

            results.append(self._extract_candle_details(curr_candle, signal_type))

        return pd.DataFrame(results)
