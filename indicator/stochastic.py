import pandas as pd

class StochasticOscillator:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with a DataFrame (e.g. from yfinance) having
        columns: ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'].
        """
        self.data = data.copy()
        # Ensure 'Date' is a column, not just an index
        if 'Date' not in self.data.columns and isinstance(self.data.index, pd.DatetimeIndex):
            self.data = self.data.reset_index().rename(columns={'index': 'Date'})

    def calculate_stochastic(self, k_period=14, d_period=3):
        """
        Calculate Stochastic Oscillator.
        """
        df = self.data.copy()

        # Calculate %K
        low_min = df['Low'].rolling(window=k_period).min()
        high_max = df['High'].rolling(window=k_period).max()
        df['percent_k'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))

        # Calculate %D
        df['percent_d'] = df['percent_k'].rolling(window=d_period).mean()

        # Determine signal
        df['type'] = 'neutral'
        df.loc[(df['percent_k'] > df['percent_d']) & (df['percent_d'] < 20), 'type'] = 'bullish'
        df.loc[(df['percent_k'] < df['percent_d']) & (df['percent_d'] > 80), 'type'] = 'bearish'

        out = df.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })[['date','type','open','high','low','close','volume','percent_k','percent_d']]


        return out.dropna().reset_index(drop=True)
