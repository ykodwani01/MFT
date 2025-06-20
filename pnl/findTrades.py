import pandas as pd
from indicator.trend import *
import numpy as np

def calculate_profit_loss(
    data: dict,
    df_final: pd.DataFrame,

    lookback,
    take_profit_pct,
    stop_pct,
    type
):
    """
    For each spinning top date, enter next day:
      - If prior lookback days form downtrend, go LONG; else SHORT.
      - Exit when profit or loss reaches stop_pct of entry price.
      - Simulate day-by-day until exit.
    Returns total P/L and list of trades.
    """
    ts = data.get('Time Series (Daily)', {})
    df = pd.DataFrame.from_dict(ts, orient='index').astype(float)
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df.index = pd.to_datetime(df.index)
    trades = []
    total_pnl=0

    dates = df_final['date']
    sorted_dates = [dt.strftime('%Y-%m-%d') for dt in df.index]
    # print(ts[sorted_dates[0]])
    # print(sorted_dates)
    for date in dates:
      idx = sorted_dates.index(date)
      prev_candle_str = sorted_dates[idx + 1 : idx + lookback]
      prev_candles = [ts[d] for d in prev_candle_str]

      if idx == 0:
            continue
      entry_idx   = idx - 1
      entry_dt    = df.index[entry_idx]
      entry_price = df.at[entry_dt, 'Open']
      close = df.at[entry_dt,'Close']
      # decide direction & thresholds
      if is_downtrend(prev_candles) and type == "reversal":
          direction       = 'long'
          profit_target   = entry_price * (1 + take_profit_pct)
          stop_loss_level = entry_price * (1 - stop_pct)
      elif is_downtrend(prev_candles) and type == "continuation":
          direction       = 'short'
          profit_target   = entry_price * (1 - take_profit_pct)
          stop_loss_level = entry_price * (1 + stop_pct)
    else :
      if type == "reversal":
            direction       = 'short'
            profit_target   = entry_price * (1 - take_profit_pct)
            stop_loss_level = entry_price * (1 + stop_pct)
      else :
            direction       = 'long'
            profit_target   = entry_price * (1 + take_profit_pct)
            stop_loss_level = entry_price * (1 - stop_pct)

      print(direction,entry_dt)
      # now scan only **future** days: these are at indices entry_idx-1, entry_idx-2, …, 0
      exit_dt    = None
      exit_price = None
      for future_idx in range(entry_idx, -1, -1):
          trade_dt = df.index[future_idx]
          high = df.at[trade_dt, 'High']
          low  = df.at[trade_dt, 'Low']
          open = df.at[trade_dt,'Open']


          if direction == 'long' :
              if high >= profit_target:
                  exit_price = profit_target
                  exit_dt    = trade_dt
                  break
              if low <= stop_loss_level:
                  exit_price = stop_loss_level
                  exit_dt    = trade_dt
                  break
          else:  # short
              if low <= profit_target:
                  exit_price = profit_target
                  exit_dt    = trade_dt
                  break
              if high >= stop_loss_level:
                  exit_price = stop_loss_level
                  exit_dt    = trade_dt
                  break

      # fallback: exit at last available close (chronologically oldest)
      if exit_dt is None:
          exit_dt    = df.index[-1]
          exit_price = entry_price

      pnl = (exit_price - entry_price) if direction == 'long' else (entry_price - exit_price)
      total_pnl += pnl

      trades.append({
          'entry_date':  entry_dt,
          'entry_price': entry_price,
          'exit_date':   exit_dt,
          'exit_price':  exit_price,
          'direction':   direction,
          'pnl':         pnl
      })
    return total_pnl, trades
