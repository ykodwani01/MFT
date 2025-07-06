import pandas as pd

def calculate_profit_loss(
    data: pd.DataFrame,
    df_final: pd.DataFrame,
    take_profit_pct: float,
    stop_pct: float,
):
    """
    For each detected Marubozu pattern, enter next day's open.
      - If type == 'bullish', go LONG; else if 'bearish', go SHORT.
      - Exit when profit or loss threshold is hit (TP or SL).
    Returns total PnL and list of trades.
    """
    try:
        if data is None or data.empty:
            raise ValueError("Input price data is empty or invalid.")

        df = data.copy()
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)

        df.sort_index(inplace=True)
        total_pnl = 0
        trades = []
        date_list = df.index.strftime('%Y-%m-%d').tolist()

        for _, row in df_final.iterrows():
            signal_date = pd.to_datetime(row['date']).strftime('%Y-%m-%d')
            signal_type = row['type'].lower()

            if signal_date not in date_list:
                continue

            idx = date_list.index(signal_date)
            entry_idx = idx  # enter on same day

            if entry_idx >= len(df):
                continue  # No data available for entry

            entry_dt = df.index[entry_idx]
            entry_price = df.iloc[entry_idx]['Close']

            if signal_type == 'bullish':
                direction = 'long'
                tp = entry_price * (1 + take_profit_pct)
                sl = entry_price * (1 - stop_pct)
            elif signal_type == 'bearish':
                direction = 'short'
                tp = entry_price * (1 - take_profit_pct)
                sl = entry_price * (1 + stop_pct)
            else:
                continue  # Invalid type

            # Simulate each future day to find exit
            exit_price = None
            exit_dt = None
            for future_idx in range(entry_idx+1, len(df)):
                future_row = df.iloc[future_idx]
                future_dt = df.index[future_idx]
                high = future_row['High']
                low = future_row['Low']

                if direction == 'long':
                    if high >= tp:
                        exit_price = tp
                        exit_dt = future_dt
                        break
                    elif low <= sl:
                        exit_price = sl
                        exit_dt = future_dt
                        break
                else:
                    if low <= tp:
                        exit_price = tp
                        exit_dt = future_dt
                        break
                    elif high >= sl:
                        exit_price = sl
                        exit_dt = future_dt
                        break

            # fallback to last candle
            if exit_price is None:
                exit_dt = df.index[-1]
                exit_price = df.iloc[-1]['Close']

            pnl = (exit_price - entry_price) if direction == 'long' else (entry_price - exit_price)
            total_pnl += pnl

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
        return 0.0, []
