import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.fetcher import Fetcher
from pattern.engulfing import EngulfingPattern
from pattern.marubozu import Marubozu
from pattern.shootingStars import ShootingStar
from pattern.spinningTop import SpinningTop
from indicator.rsi import RSI
from indicator.macd import MACD
from indicator.hull import HullMovingAverage
from indicator.stochastic import StochasticOscillator

def get_signal(symbol):
    fetcher = Fetcher()
    data = fetcher.fetch_data(symbol, period="5d")

    if data.empty:
        return None

    # Get the last two days of data
    last_two_days = data.tail(2)

    # Pass the last two days to the pattern detection classes
    engulfing = EngulfingPattern(last_two_days)
    engulfing_df = engulfing.detect_engulfing_patterns()
    if not engulfing_df.empty:
        return {"signal": engulfing_df.iloc[-1]['type'], "pattern": "engulfing"}

    marubozu = Marubozu(last_two_days)
    marubozu_df = marubozu.detect_all_marubozus()
    if not marubozu_df.empty:
        return {"signal": marubozu_df.iloc[-1]['type'], "pattern": "marubozu"}

    shooting_star = ShootingStar(last_two_days)
    shooting_star_df = shooting_star.detect_shooting_stars()
    if not shooting_star_df.empty:
        return {"signal": shooting_star_df.iloc[-1]['type'], "pattern": "shooting_star"}

    spinning_top = SpinningTop(last_two_days)
    spinning_top_df = spinning_top.detect_spinning_tops()
    if not spinning_top_df.empty:
        return {"signal": spinning_top_df.iloc[-1]['type'], "pattern": "spinning_top"}

    # Pass the full data to the indicator calculation classes
    rsi = RSI(data)
    rsi_df = rsi.calculate_rsi()
    if not rsi_df.empty:
        return {"signal": rsi_df.iloc[-1]['type'], "indicator": "rsi"}

    macd = MACD(data)
    macd_df = macd.calculate_macd()
    if not macd_df.empty:
        return {"signal": macd_df.iloc[-1]['type'], "indicator": "macd"}

    hull = HullMovingAverage(data)
    hull_df = hull.calculate_hull()
    if not hull_df.empty:
        return {"signal": hull_df.iloc[-1]['type'], "indicator": "hull"}

    stochastic = StochasticOscillator(data)
    stochastic_df = stochastic.calculate_stochastic()
    if not stochastic_df.empty:
        return {"signal": stochastic_df.iloc[-1]['type'], "indicator": "stochastic"}

    return None
