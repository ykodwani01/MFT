from indicator.trend import *
import pandas as pd

class EngulfingPattern:
    def __init__(self, data, trend_lookback=7, min_body_pct=0.5):
        """
        data: yfinance OHLCV DataFrame
        trend_lookback: candles to check trend context
        min_body_pct: % of range required to count candle body as valid
        """
        self.data = data.reset_index()
        self.trend_lookback = trend_lookback
        self.min_body_pct = min_body_pct

    def _body_pct(self, candle):
        body = abs(candle["Close"] - candle["Open"])
        rng = candle["High"] - candle["Low"]
        return (body / rng) * 100 if rng > 0 else 0

    def _is_bullish_engulfing(self, prev, curr):
        return (
            is_bearish(prev["Open"], prev["Close"]) and
            is_bullish(curr["Open"], curr["Close"]) and
            curr["Open"] < prev["Close"] and
            curr["Close"] > prev["Open"]
        )

    def _is_bearish_engulfing(self, prev, curr):
        return (
            is_bullish(prev["Open"], prev["Close"]) and
            is_bearish(curr["Open"], curr["Close"]) and
            curr["Open"] > prev["Close"] and
            curr["Close"] < prev["Open"]
        )

    def _extract_signal(self, candle, signal_type):
        return {
            "date": candle["Date"],
            "open": candle["Open"],
            "high": candle["High"],
            "low": candle["Low"],
            "close": candle["Close"],
            "volume": candle["Volume"],
            "type": signal_type
        }

    def detect_engulfing_patterns(self):
        results = []
        for i in range(self.trend_lookback + 1, len(self.data)):
            prev = self.data.iloc[i - 1]
            curr = self.data.iloc[i]

            # 1. Filter weak candles
            if self._body_pct(prev) < self.min_body_pct or self._body_pct(curr) < self.min_body_pct:
                continue

            # 2. Current body must be stronger (engulfing with conviction)
            prev_body = abs(prev["Close"] - prev["Open"])
            curr_body = abs(curr["Close"] - curr["Open"])
            if curr_body < 1.5 * prev_body:
                continue

            # 3. Volume filter (optional but recommended)
            if curr["Volume"] < self.data["Volume"].iloc[i - 5:i + 1].mean():
                continue

            # 4. Wick rejection (momentum confirmation)
            lower_wick = min(curr["Open"], curr["Close"]) - curr["Low"]
            upper_wick = curr["High"] - max(curr["Open"], curr["Close"])

            # 5. Check trend
            close_series = self.data["Close"].iloc[i - self.trend_lookback - 1 : i - 1]

            if self._is_bullish_engulfing(prev, curr) and is_downtrend(close_series):
                if lower_wick > upper_wick:  # Bullish wick rejection
                    results.append(self._extract_signal(curr, "bullish"))

            elif self._is_bearish_engulfing(prev, curr) and is_uptrend(close_series):
                if upper_wick > lower_wick:  # Bearish wick rejection
                    results.append(self._extract_signal(curr, "bearish"))

        return pd.DataFrame(results)
