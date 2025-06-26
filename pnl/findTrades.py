import pandas as pd
from indicator.trend import is_downtrend
import numpy as np

def calculate_profit_loss(
    data: dict,
    df_final: pd.DataFrame,
    lookback: int,
    take_profit_pct: float,
    stop_pct: float,
    trade_type: str
):
    """
    For each detected pattern date, enter the next day:
      - If prior lookback days form a downtrend, go LONG; else SHORT.
      - Exit when profit or loss reaches stop_pct of entry price.
      - Simulate day-by-day until exit.
    Returns total P/L and list of trades.
    """
    try:
        # Convert data to DataFrame
        if not data:
            raise ValueError("Data is empty or invalid.")

        df = pd.DataFrame.from_dict(data, orient='index')
        if df.empty:
            raise ValueError("DataFrame is empty after conversion.")

        df = df.astype(float)
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df.index = pd.to_datetime(df.index)

        trades = []
        total_pnl = 0

        # Ensure dates in df_final are sorted and valid
        dates = df_final['date']
        sorted_dates = [dt.strftime('%Y-%m-%d') for dt in df.index]

        for date in dates:
            if date not in sorted_dates:
                continue  # Skip invalid dates

            idx = sorted_dates.index(date)
            if idx == 0:
                continue  # Skip if no future data is available

            # Get previous candles for lookback period
            prev_candle_str = sorted_dates[max(0, idx - lookback):idx]
            prev_candles = [data[d] for d in prev_candle_str]

            # Entry details
            entry_idx = idx - 1
            entry_dt = df.index[entry_idx]
            entry_price = df.at[entry_dt, 'Open']

            # Determine trade direction and thresholds
            if is_downtrend(prev_candles) and trade_type == "reversal":
                direction = 'long'
                profit_target = entry_price * (1 + take_profit_pct)
                stop_loss_level = entry_price * (1 - stop_pct)
            elif is_downtrend(prev_candles) and trade_type == "continuation":
                direction = 'short'
                profit_target = entry_price * (1 - take_profit_pct)
                stop_loss_level = entry_price * (1 + stop_pct)
            else:
                if trade_type == "reversal":
                    direction = 'short'
                    profit_target = entry_price * (1 - take_profit_pct)
                    stop_loss_level = entry_price * (1 + stop_pct)
                else:
                    direction = 'long'
                    profit_target = entry_price * (1 + take_profit_pct)
                    stop_loss_level = entry_price * (1 - stop_pct)

            # Scan future days for exit
            exit_dt = None
            exit_price = None
            for future_idx in range(entry_idx, -1, -1):
                trade_dt = df.index[future_idx]
                high = df.at[trade_dt, 'High']
                low = df.at[trade_dt, 'Low']

                if direction == 'long':
                    if high >= profit_target:
                        exit_price = profit_target
                        exit_dt = trade_dt
                        break
                    if low <= stop_loss_level:
                        exit_price = stop_loss_level
                        exit_dt = trade_dt
                        break
                else:  # short
                    if low <= profit_target:
                        exit_price = profit_target
                        exit_dt = trade_dt
                        break
                    if high >= stop_loss_level:
                        exit_price = stop_loss_level
                        exit_dt = trade_dt
                        break

            # Fallback: exit at the last available close
            if exit_dt is None:
                exit_dt = df.index[0]
                exit_price = df.at[exit_dt, 'Close']

            # Calculate PnL
            pnl = (exit_price - entry_price) if direction == 'long' else (entry_price - exit_price)
            total_pnl += pnl

            # Record the trade
            trades.append({
                'entry_date': entry_dt,
                'entry_price': entry_price,
                'exit_date': exit_dt,
                'exit_price': exit_price,
                'direction': direction,
                'pnl': pnl
            })

        return total_pnl, trades

    except Exception as e:
        print(f"Error in calculate_profit_loss: {e}")
        return 0, []