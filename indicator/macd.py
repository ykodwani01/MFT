import pandas as pd

class MACD:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with a DataFrame (e.g. from yfinance) having
        columns: ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'].
        """
        self.data = data.copy()
        # Ensure 'Date' is a column, not just an index
        if 'Date' not in self.data.columns and isinstance(self.data.index, pd.DatetimeIndex):
            self.data = self.data.reset_index().rename(columns={'index': 'Date'})

    def calculate_macd(self, fast_period=12, slow_period=26, signal_period=9):
        """
        Calculate MACD, MACD Signal, and MACD Histogram.
        """
        df = self.data.copy()

        # Calculate the Fast and Slow EMAs
        fast_ema = df['Close'].ewm(span=fast_period, adjust=False).mean()
        slow_ema = df['Close'].ewm(span=slow_period, adjust=False).mean()

        # Calculate MACD
        df['macd'] = fast_ema - slow_ema

        # Calculate MACD Signal
        df['macd_signal'] = df['macd'].ewm(span=signal_period, adjust=False).mean()

        # Calculate MACD Histogram
        df['macd_hist'] = df['macd'] - df['macd_signal']

        # Determine signal
        df['type'] = 'neutral'
        df.loc[(df['macd'] > df['macd_signal']), 'type'] = 'bullish'
        df.loc[(df['macd'] < df['macd_signal']), 'type'] = 'bearish'

        out = df.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })[['date','type','open','high','low','close','volume','macd','macd_signal','macd_hist']]

        return out.dropna().reset_index(drop=True)
