import pandas as pd
import numpy as np

class HullMovingAverage:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with a DataFrame (e.g. from yfinance) having
        columns: ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'].
        """
        self.data = data.copy()
        # Ensure 'Date' is a column, not just an index
        if 'Date' not in self.data.columns and isinstance(self.data.index, pd.DatetimeIndex):
            self.data = self.data.reset_index().rename(columns={'index': 'Date'})

    def calculate_hull(self, window=16):
        """
        Calculate Hull Moving Average.
        """
        df = self.data.copy()

        # Calculate WMA for half and full window periods
        half_window = int(window / 2)
        sqrt_window = int(np.sqrt(window))

        wma_half = df['Close'].rolling(window=half_window).apply(lambda x: np.dot(x, np.arange(1, half_window + 1)) / np.sum(np.arange(1, half_window + 1)), raw=True)
        wma_full = df['Close'].rolling(window=window).apply(lambda x: np.dot(x, np.arange(1, window + 1)) / np.sum(np.arange(1, window + 1)), raw=True)

        # Calculate HMA
        df['hma'] = (2 * wma_half - wma_full).rolling(window=sqrt_window).mean()

        # Determine signal
        df['type'] = 'neutral'
        df.loc[df['Close'] > df['hma'], 'type'] = 'bullish'
        df.loc[df['Close'] < df['hma'], 'type'] = 'bearish'

        out = df.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })[['date','type','open','high','low','close','volume','hma']]

        return out.dropna().reset_index(drop=True)
